import os
import queue
import subprocess as sp
import sys
import threading
import tkinter as tk
from tkinter import font as tk_font

import flask
from PIL import ImageTk, Image
from flask import request

from teller import config
from teller import util

""" 
ubuntu后台服务运行方式
自动获取当前程序的名称

窗口程序是主进程，web服务是子进程，因为tkinter比较奇葩，tkinter不能在子线程中运行。  
如果涉及到可视化，还是不要用tkinter比较好，坑比较多。  
"""


def get_path(relative_path):
    return os.path.join(os.path.dirname(config.__file__), relative_path)


def set_win_center(root, width=None, height=None):
    """
    设置窗口大小，并居中显示
    :param root:主窗体实例
    :param width:窗口宽度，非必填，默认200
    :param height:窗口高度，非必填，默认200
    :return:无
    """
    if not width:
        width = root.winfo_width()
    if not height:
        height = root.winfo_height()

    # 获取屏幕宽度和高度
    screen_width, screen_height = root.maxsize()
    # 计算中心坐标
    cen_x = (screen_width - width) / 2
    cen_y = (screen_height - height) / 2
    # 设置窗口初始大小和位置
    size_xy = "%dx%d+%d+%d" % (width, height, cen_x, cen_y)
    root.geometry(size_xy)


def play_music():
    sp.Popen(["play", get_path(config.music_path)])


def show_window(q: queue.Queue):
    window = tk.Tk()
    img = Image.open(get_path(config.icon_path))
    photo = ImageTk.PhotoImage(img)
    ft = tk_font.Font(family=config.font, size=20, weight=tk_font.BOLD)
    window.wm_iconphoto(window, photo)
    window.resizable(0, 0)
    window.attributes("-topmost", 1)
    set_win_center(window, config.window_width, config.window_height)

    def on_closing():
        msgList.delete(0, tk.END)
        window.withdraw()

    def wait_message():
        if not q.empty():
            msg = q.get()
            print(msg)
            msgList.insert(tk.END, msg)
            window.title(msg)
            window.deiconify()
            window.focus()
            window.update()
            window.lift()
            if config.play_music:
                play_music()
        window.after(1000, wait_message)

    def on_focus_in(e):
        pass

    def on_focus_out(e):
        pass

    msgList = tk.Listbox(window, font=ft)
    button = tk.Button(window, text="Close", font=ft, command=on_closing)
    msgList.pack(fill=tk.BOTH)
    button.pack(fill=tk.BOTH)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.bind("<FocusIn>", on_focus_in)
    window.bind("<FocusOut>", on_focus_out)
    window.after(1000, wait_message)
    window.mainloop()


app = flask.Flask(__name__)
q = queue.Queue()


@app.route("/")
def haha():
    content = request.args.get("content", "Got Message")
    q.put(content)
    return ""


def run_app():
    print("now will run")
    app.run(debug=False, port=config.port)


def main():
    if util.is_port_open('127.0.0.1', config.port):
        # 检查是不是teller在运行
        cmd = util.get_cmd_of_port(config.port)
        cmd_string = ' '.join(cmd)
        if 'tell' not in cmd_string:
            print(f"""端口{config.port}已经被占用了，占用此端口的命令为{','.join(cmd)}""", file=sys.stderr)
            print(cmd_string)
            exit(0)
        else:
            print("teller已经启动")
            exit(0)

    ui_process = threading.Thread(target=run_app, name="teller-gui-process")  # GUI进程
    ui_process.daemon = True  # 主进程退出时，子进程必须及时退出
    ui_process.start()
    show_window(q)


if __name__ == "__main__":
    main()
