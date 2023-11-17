"""Usage
调用默认模型：
python server/api_allinone.py

加载多个非默认模型：
python server/api_allinone.py --model-path-address model1@host1@port1 model2@host2@port2 

多卡启动：
python server/api_allinone.py --model-path-address model@host@port --num-gpus 2 --gpus 0,1 --max-gpu-memory 10GiB


启动控制器
nohup python -m fastchat.serve.controller  --host 0.0.0.0  --port 21001  --dispatch-method shortest_queue  >/mnt/22xiaowei/Lchat/Langchain-Chatchat/logs/controller.log 2>&1 &

启动工作器
python -m fastchat.serve.model_worker  --host 0.0.0.0  --port 21002  --controller-address http://0.0.0.0:21001  --model-path /model/chatglm2-6b-32k  --revision main  --device cuda  --gpus 0,1  --num-gpus 2  --max-gpu-memory 20GiB  --gptq-wbits 16  --gptq-groupsize -1  --limit-worker-concurrency 5  --stream-interval 2  --worker-address http://0.0.0.0:21002  >/mnt/22xiaowei/Lchat/Langchain-Chatchat/logs/worker_chatglm2_6b_32k_0_0_0_0_21002.log

python -m fastchat.serve.model_worker  --host 0.0.0.0  --port 20003  --controller-address http://0.0.0.0:20001 \
 --model-path /model/chatglm2-6b-32k  --revision main  --device cuda  --gpus 0,1  --num-gpus 2  --max-gpu-memory 20GiB \
   --gptq-wbits 16  --gptq-groupsize -1  --limit-worker-concurrency 5  --stream-interval 2  \
   --worker-address http://0.0.0.0:20003  >/mnt/Lchat/Langchain-Chatchat-dev/logs/worker_chatglm2_6b_32k_0_0_0_0_20003.log


启动openai方式的api
python -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 7861

以cli模式启动
python -m fastchat.serve.cli --model-path /model/chatglm3-6b-32k --num-gpus 2 --gpus 0,1

python server/api_allinone_stale.py --num-gpus 2 --gpus 0,1

"""
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm_api_stale import launch_all, parser, controller_args, worker_args, server_args
from api import create_app
import uvicorn

parser.add_argument("--api-host", type=str, default="0.0.0.0")
parser.add_argument("--api-port", type=int, default=7861)
parser.add_argument("--ssl_keyfile", type=str)
parser.add_argument("--ssl_certfile", type=str)

api_args = ["api-host", "api-port", "ssl_keyfile", "ssl_certfile"]


def run_api(host, port, **kwargs):
    app = create_app()
    if kwargs.get("ssl_keyfile") and kwargs.get("ssl_certfile"):
        uvicorn.run(app,
                    host=host,
                    port=port,
                    ssl_keyfile=kwargs.get("ssl_keyfile"),
                    ssl_certfile=kwargs.get("ssl_certfile"),
                    )
    else:
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    print("Luanching api_allinone，it would take a while, please be patient...")
    print("正在启动api_allinone，LLM服务启动约3-10分钟，请耐心等待...")
    # 初始化消息
    args = parser.parse_args()
    args_dict = vars(args)
    launch_all(args=args, controller_args=controller_args, worker_args=worker_args, server_args=server_args)
    run_api(
        host=args.api_host,
        port=args.api_port,
        ssl_keyfile=args.ssl_keyfile,
        ssl_certfile=args.ssl_certfile,
    )
    print("Luanching api_allinone done.")
    print("api_allinone启动完毕.")
