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
    root.geometry("1500x900")
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
    tc.program_labels_initialize()
    tc.trace_object_initialize(row=12,col=3)
    tc.exist_object_initialize(row=12,col=10)
    
    ### 不変なオブジェクトの設定 ###
    # 配列の表示遷移
    btn_value_down = frk.ButtonK()
    btn_value_down["text"] = "◀︎"
    btn_value_down["command"] = tc.down_array_view()
    btn_value_down.layout = "16,6,1,1"

    btn_value_up = frk.ButtonK()
    btn_value_up["text"] = "▶︎"
    btn_value_up["command"] = tc.up_array_view()
    btn_value_up.layout = "17,6,1,1"

    # 再生ボタンの設定
    btn_highlight_down = frk.ButtonK()
    btn_highlight_down["text"] = "▶︎"
    btn_highlight_down["command"] = tc.down_highlight()
    btn_highlight_down.layout = "7,21,1,2"
    # 巻き戻しボタンの設定
    btn_highlight_up = frk.ButtonK()
    btn_highlight_up["text"] = "◀︎"
    btn_highlight_up["command"] = tc.up_highlight()
    btn_highlight_up.layout = "5,21,1,2"
    # プログラム上昇ボタンの設定
    btn_code_up = frk.ButtonK()
    btn_code_up["text"] = "▲"
    btn_code_up["command"] = tc.up_code()
    btn_code_up.layout = "6,21,1,1"
    # プログラム下降ボタンの設定
    btn_code_down = frk.ButtonK()
    btn_code_down["text"] = "▼"
    btn_code_down["command"] = tc.down_code()
    btn_code_down.layout = "6,22,1,1"
    # ファイル読み込みボタンの設定
    btn_file_open = frk.ButtonK()
    btn_file_open["text"] = "file open"
    btn_file_open["command"] = tc.open_file()
    btn_file_open.layout = "1,21,3,1"
    # exist value の表示
    constView_exist = frk.LabelK()
    constView_exist["text"] = "exist variable"
    constView_exist.layout = "11,9,3,1"
    constView_exist["relief"] = "groove"
    constView_exist["bg"] = "#c0c0c0"
    # program progress　の表示
    constView_progress = frk.LabelK()
    constView_progress["text"] = "program progress"
    constView_progress.layout = "11,1,3,1"
    constView_progress["relief"] = "groove"
    constView_progress["bg"] = "#d7d7ff"

    #オブジェクトをレイアウト通りに配置する
    root.set_layout()
    # メインループ
    root.mainloop()

#### 関数セット



if __name__ == "__main__":
    main()

