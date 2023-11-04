import sys
sys.path.append(".")
from server.knowledge_base.migrate import (create_tables, reset_tables, import_from_db,
                                           folder2db, prune_db_docs, prune_folder_files)
from configs.model_config import NLTK_DATA_PATH, EMBEDDING_MODEL
import nltk
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path
from datetime import datetime
import sys


"""
-r --recreate-vs，重新创建向量知识库
--create-tables，建表（sqllite）
--clear-tables，删除再建表（sqllite）
--import-db，适用于版本升级时，info.db 结构变化，但无需重新向量化的情况。当前仅支持 sqlite
--update-in-db，重建向量库（向量数据库中和本地文件都存在的情况下更新，只有本地文件的时候不执行）
-i --increament，新增向量库（本地文件存在但是数据库不存在）
--prune-db，删除向量库（数据库有但是本地没文件）
--prune-folder，删除文件（本地有文件但是数据库没有记录）
--kb-name，所有操作支持指定操作的知识库，不指定则为所有本地知识库
--embed-model，指定向量模型
"""

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="please specify only one operate method once time.")

    parser.add_argument(
        "-r",
        "--recreate-vs",
        action="store_true",
        help=('''
            重新创建向量知识库 recreate vector store.
            use this option if you have copied document files to the content folder, but vector store has not been populated or DEFAUL_VS_TYPE/EMBEDDING_MODEL changed.
            '''
        )
    )
    parser.add_argument(
        "--create-tables",
        action="store_true",
        help=("建表（sqllite）create empty tables if not existed")
    )
    parser.add_argument(
        "--clear-tables",
        action="store_true",
        help=("删除再建表（sqllite） create empty tables, or drop the database tables before recreate vector stores")
    )
    parser.add_argument(
        "--import-db",
        help="适用于版本升级时，info.db 结构变化，但无需重新向量化的情况。当前仅支持 sqlite import tables from specified sqlite database"
    )
    parser.add_argument(
        "-u",
        "--update-in-db",
        action="store_true",
        help=('''
            重建向量库（向量数据库中和本地文件都存在的情况下更新，只有本地文件的时候不执行）
            update vector store for files exist in database.
            use this option if you want to recreate vectors for files exist in db and skip files exist in local folder only.
            '''
        )
    )
    parser.add_argument(
        "-i",
        "--increament",
        action="store_true",
        help=('''
            新增向量库（本地文件存在但是数据库不存在）
            update vector store for files exist in local folder and not exist in database.
            use this option if you want to create vectors increamentally.
            '''
        )
    )
    parser.add_argument(
        "--prune-db",
        action="store_true",
        help=('''
            删除向量库（数据库有但是本地没文件）
            delete docs in database that not existed in local folder.
            it is used to delete database docs after user deleted some doc files in file browser
            '''
        )
    )
    parser.add_argument(
        "--prune-folder",
        action="store_true",
        help=('''
            删除文件（本地有文件但是数据库没有记录）
            delete doc files in local folder that not existed in database.
            is is used to free local disk space by delete unused doc files.
            '''
        )
    )
    parser.add_argument(
        "-n",
        "--kb-name",
        type=str,
        nargs="+",
        default=[],
        help=("所有操作支持指定操作的知识库，不指定则为所有本地知识库 specify knowledge base names to operate on. default is all folders exist in KB_ROOT_PATH.")
    )
    parser.add_argument(
        "-e",
        "--embed-model",
        type=str,
        default=EMBEDDING_MODEL,
        help=("指定向量模型 specify embeddings model.")
    )

    args = parser.parse_args()
    start_time = datetime.now()

    if args.create_tables:
        create_tables()  # confirm tables exist

    if args.clear_tables:
        reset_tables()
        print("database talbes reseted")

    if args.recreate_vs:
        print("recreating all vector stores")
        folder2db(kb_names=args.kb_name, mode="recreate_vs", embed_model=args.embed_model)
    elif args.import_db:
        import_from_db(args.import_db)
    elif args.update_in_db:
        folder2db(kb_names=args.kb_name, mode="update_in_db", embed_model=args.embed_model)
    elif args.increament:
        folder2db(kb_names=args.kb_name, mode="increament", embed_model=args.embed_model)
    elif args.prune_db:
        prune_db_docs(args.kb_name)
    elif args.prune_folder:
        prune_folder_files(args.kb_name)

    end_time = datetime.now()
    print(f"总计用时： {end_time-start_time}")
