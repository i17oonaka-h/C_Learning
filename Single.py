# -*- coding: utf-8 -*-
from os import name
import tkinter as tk
import tkinter.ttk as ttk
from typing import Text
import Framework as frk
from tkinter import ttk
from dataclasses import dataclass, field
from source_read import get_token
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Trace_manage import Trace



def main():
    root = frk.FormK(24,20,0)
    root.title("C-Learning")
    root.geometry("1000x600")
    root.result = tk.StringVar()
    style = ttk.Style() 
    style.configure('TButton', font = 
               ('calibri', 20, 'bold'),
                    borderwidth = '4') 
    style.map('Button'
         , foreground = [('active', '!disabled', 'green')]
         , background = [('active', 'black')]
         ) 

    tc = Trace()
    tc.labels_set()
    tc.trace_object_set(row=12,col=3)
    tc.exist_object_set(row=12,col=10)
    
    ### 不変なオブジェクトの設定 ###
    # 再生ボタンの設定
    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = tc.down_highlight()
    btnPlay.layout = "7,21,1,2"
    # 巻き戻しボタンの設定
    btn_play_back = frk.ButtonK()
    btn_play_back["text"] = "◀︎"
    btn_play_back["command"] = tc.up_highlight()
    btn_play_back.layout = "5,21,1,2"
    # プログラム上昇ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▲"
    btn_play_stop["command"] = tc.up_code()
    btn_play_stop.layout = "6,21,1,1"
    # プログラム下降ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▼"
    btn_play_stop["command"] = tc.down_code()
    btn_play_stop.layout = "6,22,1,1"
    # ファイル読み込みボタンの設定
    btn_file_open = frk.ButtonK()
    btn_file_open["text"] = "file open"
    btn_file_open["command"] = tc.open_file()
    btn_file_open.layout = "1,21,3,1"
    # exist value の表示
    exist_label = frk.LabelK()
    exist_label["text"] = "exist variable"
    exist_label.layout = "11,9,3,1"
    exist_label["relief"] = "groove"
    exist_label["bg"] = "#c0c0c0"
    # program progress　の表示
    trace_label = frk.LabelK()
    trace_label["text"] = "program progress"
    trace_label.layout = "11,1,3,1"
    trace_label["relief"] = "groove"
    trace_label["bg"] = "#d7d7ff"

    #オブジェクトをレイアウト通りに配置する
    root.set_layout()
    # メインループ
    root.mainloop()

#### 関数セット



if __name__ == "__main__":
    main()

