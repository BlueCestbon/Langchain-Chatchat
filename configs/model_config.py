import os


# 可以指定一个绝对路径，统一存放所有的Embedding和LLM模型。
# 每个模型可以是一个单独的目录，也可以是某个目录下的二级子目录。
# 如果模型目录名称和 MODEL_PATH 中的 key 或 value 相同，程序会自动检测加载，无需修改 MODEL_PATH 中的路径。
MODEL_ROOT_PATH = "/model"
# MODEL_ROOT_PATH = "/model"

# 选用的 Embedding 名称
EMBEDDING_MODEL = "bge-large-zh-v1.5"  # bge-large-zh

# Embedding 模型运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
EMBEDDING_DEVICE = "auto"

# 如果需要在 EMBEDDING_MODEL 中增加自定义的关键字时配置
EMBEDDING_KEYWORD_FILE = "keywords.txt"
EMBEDDING_MODEL_OUTPUT_PATH = "output"

# 要运行的 LLM 名称，可以包括本地模型和在线模型。
# 第一个将作为 API 和 WEBUI 的默认模型
# LLM_MODELS = ["chatglm2-6b-32k"]
LLM_MODELS = ["baichuan2-7b"]
# LLM_MODELS = ["baichuan2-13b-4bits"]

# AgentLM模型的名称 (可以不指定，指定之后就锁定进入Agent之后的Chain的模型，不指定就是LLM_MODELS[0])
Agent_MODEL = None

# LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
LLM_DEVICE = "auto"

# 历史对话轮数
HISTORY_LEN = 1

# 大模型最长支持的长度，如果不填写，则使用模型默认的最大长度，如果填写，则为用户设定的最大长度
MAX_TOKENS = None

# LLM通用对话参数
TEMPERATURE = 0.1
# TOP_P = 0.95 # ChatOpenAI暂不支持该参数

ONLINE_LLM_MODEL = {}

# 在以下字典中修改属性值，以指定本地embedding模型存储位置。支持3种设置方法：
# 1、将对应的值修改为模型绝对路径
# 2、不修改此处的值（以 text2vec 为例）：
#       2.1 如果{MODEL_ROOT_PATH}下存在如下任一子目录：
#           - text2vec
#           - GanymedeNil/text2vec-large-chinese
#           - text2vec-large-chinese
#       2.2 如果以上本地路径不存在，则使用huggingface模型
MODEL_PATH = {
    "embed_model": {
        "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
    },

    "llm_model": {
        # 以下部分模型并未完全测试，仅根据fastchat和vllm模型的模型列表推定支持
        "chatglm2-6b-32k": "THUDM/chatglm2-6b-32k",
        "chatglm3-6b-32k": "THUDM/chatglm3-6b-32k",
        "baichuan2-7b": "baichuan-inc/Baichuan2-7B-Chat",
        "baichuan2-13b": "baichuan-inc/Baichuan2-13B-Chat",
        "Qwen-7B-Chat": "Qwen/Qwen-7B-Chat",
        "Qwen-14B-Chat": "Qwen/Qwen-14B-Chat",
    },
}


# 通常情况下不需要更改以下内容

# nltk 模型存储路径
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

VLLM_MODEL_DICT = {
    "aquila-7b": "BAAI/Aquila-7B",
    "aquilachat-7b": "BAAI/AquilaChat-7B",

    "baichuan-7b": "baichuan-inc/Baichuan-7B",
    "baichuan-13b": "baichuan-inc/Baichuan-13B",
    'baichuan-13b-chat': 'baichuan-inc/Baichuan-13B-Chat',
    # 注意：bloom系列的tokenizer与model是分离的，因此虽然vllm支持，但与fschat框架不兼容
    # "bloom":"bigscience/bloom",
    # "bloomz":"bigscience/bloomz",
    # "bloomz-560m":"bigscience/bloomz-560m",
    # "bloomz-7b1":"bigscience/bloomz-7b1",
    # "bloomz-1b7":"bigscience/bloomz-1b7",

    "internlm-7b": "internlm/internlm-7b",
    "internlm-chat-7b": "internlm/internlm-chat-7b",
    "falcon-7b": "tiiuae/falcon-7b",
    "falcon-40b": "tiiuae/falcon-40b",
    "falcon-rw-7b": "tiiuae/falcon-rw-7b",
    "gpt2": "gpt2",
    "gpt2-xl": "gpt2-xl",
    "gpt-j-6b": "EleutherAI/gpt-j-6b",
    "gpt4all-j": "nomic-ai/gpt4all-j",
    "gpt-neox-20b": "EleutherAI/gpt-neox-20b",
    "pythia-12b": "EleutherAI/pythia-12b",
    "oasst-sft-4-pythia-12b-epoch-3.5": "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
    "dolly-v2-12b": "databricks/dolly-v2-12b",
    "stablelm-tuned-alpha-7b": "stabilityai/stablelm-tuned-alpha-7b",
    "Llama-2-13b-hf": "meta-llama/Llama-2-13b-hf",
    "Llama-2-70b-hf": "meta-llama/Llama-2-70b-hf",
    "open_llama_13b": "openlm-research/open_llama_13b",
    "vicuna-13b-v1.3": "lmsys/vicuna-13b-v1.3",
    "koala": "young-geng/koala",
    "mpt-7b": "mosaicml/mpt-7b",
    "mpt-7b-storywriter": "mosaicml/mpt-7b-storywriter",
    "mpt-30b": "mosaicml/mpt-30b",
    "opt-66b": "facebook/opt-66b",
    "opt-iml-max-30b": "facebook/opt-iml-max-30b",

    "Qwen-7B": "Qwen/Qwen-7B",
    "Qwen-14B": "Qwen/Qwen-14B",
    "Qwen-7B-Chat": "Qwen/Qwen-7B-Chat",
    "Qwen-14B-Chat": "Qwen/Qwen-14B-Chat",

    "agentlm-7b": "THUDM/agentlm-7b",
    "agentlm-13b": "THUDM/agentlm-13b",
    "agentlm-70b": "THUDM/agentlm-70b",

}

# 你认为支持Agent能力的模型，可以在这里添加，添加后不会出现可视化界面的警告
# 经过我们测试，原生支持Agent的模型仅有以下几个
SUPPORT_AGENT_MODEL = [
    "azure-api",
    "openai-api",
    "qwen-api",
    "Qwen",
    "chatglm3",
    "xinghuo-api",
]
