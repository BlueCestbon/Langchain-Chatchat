from typing import List, Dict, Optional

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import Document
from langchain.vectorstores.milvus import Milvus

from configs import kbs_config, LLM_MODELS, TEMPERATURE, GET_KEY_FILENAME_PROMPT

from server.knowledge_base.kb_service.base import KBService, SupportedVSType, EmbeddingsFunAdapter, \
    score_threshold_process
from server.knowledge_base.utils import KnowledgeFile

import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from server.utils import get_ChatOpenAI

class MilvusKBService(KBService):
    milvus: Milvus

    @staticmethod
    def get_collection(milvus_name):
        from pymilvus import Collection
        return Collection(milvus_name)

    # def save_vector_store(self):
    #     if self.milvus.col:
    #         self.milvus.col.flush()

    def get_doc_by_ids(self, ids: List[str]) -> List[Document]:
        result = []
        if self.milvus.col:
            data_list = self.milvus.col.query(expr=f'pk in {ids}', output_fields=["*"])
            for data in data_list:
                text = data.pop("text")
                result.append(Document(page_content=text, metadata=data))
        return result

    @staticmethod
    def search(milvus_name, content, limit=3):
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        c = MilvusKBService.get_collection(milvus_name)
        return c.search(content, "embeddings", search_params, limit=limit, output_fields=["content"])

    def do_create_kb(self):
        pass

    def vs_type(self) -> str:
        return SupportedVSType.MILVUS

    def _load_milvus(self):
        self.milvus = Milvus(embedding_function=EmbeddingsFunAdapter(self.embed_model),
                             collection_name=self.kb_name, connection_args=kbs_config.get("milvus"))

    def do_init(self):
        self._load_milvus()

    def do_drop_kb(self):
        if self.milvus.col:
            self.milvus.col.release()
            self.milvus.col.drop()

    def do_search(self, query: str, top_k: int, score_threshold: float):
        self._load_milvus()
        embed_func = EmbeddingsFunAdapter(self.embed_model)
        embeddings = embed_func.embed_query(query)

        logging.info(f"针对 {query} 使用LLM来获得所属文件的关键信息")
        # keyword_filename = "安全会议管理"  # 这个值是大模型从query里提取出来的文件名
        model = get_ChatOpenAI(
            model_name=LLM_MODELS[0],
            temperature=1e-8,
        )
        human_prompt = GET_KEY_FILENAME_PROMPT.format(query=query)
        chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
        chain = LLMChain(prompt=chat_prompt, llm=model, verbose=True)
        response_key = chain({"query": query})
        try:
            keyword_filename = response_key["text"]
        except Exception as e:
            logging.error(f"异常 {e}")
            keyword_filename = "NULL"
        logging.info(f"{query} 获取到的关键信息是 {keyword_filename}")

        # 判断元数据 key_filename 是不是在用户输入中出现过，出现过那就缩小范围，没出现那就像之前一样全库搜索
        # 定义一个布尔表达式，用于过滤出出现 key_filename 的记录
        expr = f"key_filename in ['{keyword_filename}']"

        # key_filename in ['安全测试管理']
        try:
            docs = self.milvus.similarity_search_with_score_by_vector(embeddings, top_k, expr=expr)
            _ = docs[0]
            logging.info(f"expr:{expr} 检索出来的docs[0](total={len(docs)}):{_}")
        except Exception as e:
            # 如果异常或者没匹配到，那就全库搜索
            logging.error(f"根据 keyword_filename {keyword_filename} 查询文件出现异常，没查询到符合的文档 {e}")
            docs = self.milvus.similarity_search_with_score_by_vector(embeddings, top_k)


        return score_threshold_process(score_threshold, top_k, docs)

    def do_add_doc(self, docs: List[Document], **kwargs) -> List[Dict]:
        # TODO: workaround for bug #10492 in langchain
        for doc in docs:
            for k, v in doc.metadata.items():
                doc.metadata[k] = str(v)
            for field in self.milvus.fields:
                doc.metadata.setdefault(field, "")
            doc.metadata.pop(self.milvus._text_field, None)
            doc.metadata.pop(self.milvus._vector_field, None)

        ids = self.milvus.add_documents(docs)
        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]
        return doc_infos

    def do_delete_doc(self, kb_file: KnowledgeFile, **kwargs):
        if self.milvus.col:
            filepath = kb_file.filepath.replace('\\', '\\\\')
            delete_list = [item.get("pk") for item in
                           self.milvus.col.query(expr=f'source == "{filepath}"', output_fields=["pk"])]
            self.milvus.col.delete(expr=f'pk in {delete_list}')

    def do_clear_vs(self):
        if self.milvus.col:
            self.do_drop_kb()
            self.do_init()


if __name__ == '__main__':
    # 测试建表使用
    from server.db.base import Base, engine

    Base.metadata.create_all(bind=engine)
    milvusService = MilvusKBService("test")
    # milvusService.add_doc(KnowledgeFile("README.md", "test"))

    print(milvusService.get_doc_by_ids(["444022434274215486"]))
    # milvusService.delete_doc(KnowledgeFile("README.md", "test"))
    # milvusService.do_drop_kb()
    # print(milvusService.search_docs("如何启动api服务"))
