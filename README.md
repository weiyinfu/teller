# DEPRECATED: Use IM webhook is the best practice

在远程服务器上跑一个批处理任务的时候，程序中途挂了，我却不知道。如果我知道了，肯定会立马查看原因。而现在却耽误了一些时间，如果程序跑完之后我能够及时知道该有多好啊！例如，我只需要执行`python main.py ; tell 程序跑完啦`这个命令就可以。    

如何让我知道？打电话、发短信实现起来比较复杂，需要接入第三方应用且天下没有免费的午餐。工作时大部分时间都对着电脑，所以只有当我在电脑前面的时候才通知我，所以通知器应该是一个客户端。当任务在远程服务器上执行完毕之后，向我的电脑发起网络请求。原理很简单：ssh 的remote-forward可以把远程的请求单向转发到本地。

于是，就有了本程序。 

# 使用方法
首先安装依赖：
* mac上`brew install sox`
* ubuntu上`apt-get install sox`

使用pip安装本程序`pip3 install git+https://github.com/weiyinfu/teller`.    
在本地`./bashrc`中添加`nohup telld  > /dev/null  2>&1   &
`  
在本地的~/.ssh添加以下片段：
```bash
Host *
    RemoteForward 8090 localhost:8090
```
注意：
* 如果多次ssh，每次ssh时都带上这个转发。
* 如果想要更改端口号，请直接修改teller/config.py然后再安装（或者安装之后再更改config.py）。

在本地使用telld命令启动本地服务。  
ssh到远程机器之后，执行如下代码`python haha.py ; tell game over`，表示当`python haha.py`执行完毕之后，调用tell命令把消息发送到本地。

注意，server程序不能在服务端运行，也不需要在服务端运行。
* server程序不能在服务端运行：server程序只能在本地通过命令来运行，不能通过gunicorn和supervisor进行管理，因为那种后台环境没有可视化库。  
* server程序不需要在服务端运行：因为server的作用是在本地运行，用于通知自己。  
