跑一个批处理任务的时候，程序中途挂了，我却不知道，浪费了大量时间，如果程序跑完之后我能够及时知道该有多好啊！

如何让我知道？打电话、发短信太复杂了，需要接入第三方应用且天下没有免费的午餐。工作时大部分时间都对着电脑，所以只有当我在电脑前面的时候才通知我，所以通知器应该是一个客户端。

原理：ssh 的remote-forward可以把远程的请求单向转发到本地。

# 使用方法
在本地的~/.ssh添加(注意，如果多次ssh，每次ssh时都带上这个转发)
```bash
Host *
    RemoteForward 8090 localhost:8090
```

ssh到远程机器之后，执行如下代码`python haha.py ; tell game over`，表示当`python haha.py`执行完毕之后，调用tell命令把消息发送到本地。
