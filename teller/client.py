import socket
import sys

import requests

from teller import config


def is_port_open(ip: str, port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        # 利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
        # 该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
        return True
    except:
        return False


if not is_port_open("127.0.0.1", config.port):
    print(f"port {config.port} is not open !")
    exit(-1)
args = " ".join(sys.argv[1:])
resp = requests.get(f"http://localhost:{config.port}", params={"content": args})
if resp.text:
    print(resp.text)
