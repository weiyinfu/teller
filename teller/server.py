import multiprocessing as mp
import os
import threading
import tkinter as tk
from tkinter import font as tk_font

import flask
import pygame
from PIL import ImageTk, Image
from flask import request

from teller import config

"""  
ubuntu后台服务运行方式
自动获取当前程序的名称
"""


def get_path(relative_path):
    return os.path.join(os.path.dirname(config.__file__), relative_path)


def play_music():
    """播放音乐"""
    pygame.mixer.init()  # 初始化
    pygame.mixer.music.load(get_path(config.music_path))  # 加载音乐
    pygame.mixer.music.play()


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


def show_window(q: mp.Queue):
    window = tk.Tk()
    img = Image.open(get_path(config.icon_path))
    photo = ImageTk.PhotoImage(img)
    ft = tk_font.Font(family=None, size=20, weight=tk_font.BOLD)
    window.wm_iconphoto(window, photo)
    window.resizable(0, 0)
    window.attributes("-topmost", 1)
    set_win_center(window, config.window_width, config.window_height)

    def on_closing():
        msgList.delete(0, tk.END)
        window.withdraw()

    def wait_message():
        while 1:
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
    threading.Thread(target=wait_message).start()
    window.mainloop()


app = flask.Flask(__name__)
q = mp.Queue()


@app.route("/")
def haha():
    content = request.args.get("content", "Got Message")
    q.put(content)
    return ""


if __name__ == "__main__":
    mp.Process(
        target=show_window, name="teller-gui-process", args=(q,)
    ).start()  # GUI进程
    app.run(debug=False, port=config.port)
