跑一个批处理任务的时候，程序中途挂了，我却不知道，浪费了大量时间，如果程序跑完之后我能够及时知道该有多好啊！

如何让我知道？打电话、发短信太复杂了，需要接入第三方应用且天下没有免费的午餐。工作时大部分时间都对着电脑，所以只有当我在电脑前面的时候才通知我，所以通知器应该是一个客户端。

原理：
ssh 的remote-forward可以把远程的请求单向转发到本地。

# 使用方法
在本地的~/.ssh添加
```bash
Host *
    RemoteForward 8090 localhost:8090
```

python3 setup.py --install

rlaunch -- tell;zsh

python haha.py ; tell

