# -*- coding: utf-8 -*-

#### インポート
import os
import tkinter as tk
import tkinter.ttk as ttk
import openpyxl as px
import subprocess

import Framework as frk

from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# global program_codelist

def main():

    #### rootフレームの設定
    root = frk.FormK(24,20,0)
    root.title("C-Learning")
    root.geometry("1000x600")
    root.bg = '#B7E899'
    root.configure(background=root.bg)
    root.result = tk.StringVar()

    # スタイル設定
    style = ttk.Style() 
    style.configure('TButton', font = 
               ('calibri', 20, 'bold'),
                    borderwidth = '4') 

    # Changes will be reflected 
    # by the movement of mouse. 
    style.map('Button'
         , foreground = [('active', '!disabled', 'green')]
         , background = [('active', 'black')]
         ) 

    # プログラム表示部分のラベルの生成
    program_labels = []
    for i in range(20):
        program_labels.append(frk.LabelK())
        program_labels[i]["font"] = ("Arial", 16)
        program_labels[i]["text"] = "\n"
        if i == 0:
            program_labels[i]["bg"] = "#ffff6d"
        else:
            program_labels[i]["bg"] = "#ffffff"
        program_labels[i]["anchor"] = "nw"
        program_labels[i].layout = "1,{},10,1".format(i+1)

    # プログラムトレース図部分のラベルの生成
    Trace_data = []
    Change_data = []
    for i in range(20):
        Trace_data.append(frk.LabelK())
        Change_data.append(frk.LabelK())  

    # 1.1 再生ボタンの設定
    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = down_syntax(program_labels)
    btnPlay.layout = "7,21,1,2"

    # 1.2 巻き戻しボタンの設定
    btn_play_back = frk.ButtonK()
    btn_play_back["text"] = "◀︎"
    btn_play_back["command"] = up_syntax(program_labels)
    btn_play_back.layout = "5,21,1,2"

    # 1.3 停止ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "‖"
    btn_play_stop["command"] = root.destroy
    btn_play_stop.layout = "6,21,1,2"

    # ファイル読み込みボタンの設定
    btn_file_open = frk.ButtonK()
    btn_file_open["text"] = "file open"
    btn_file_open["command"] = open_file(program_labels,Trace_data,Change_data)
    btn_file_open.layout = "1,21,3,1"

    # トレース図表示部分のラベルの生成（仮のもの）
    picture_place = frk.LabelK() 
    picture_place["text"] = "トレース図表示部分"
    picture_place["bg"] = "#eeeeee"
    picture_place["anchor"] = "nw"
    picture_place["relief"] = "ridge"
    picture_place.layout = "11,1,10,24"
    #オブジェクトをレイアウト通りに配置する
    root.set_layout()
    # メインループ
    root.mainloop()

#### コードセット

def make_trace_fig(Trace_data,Change_data,type_name,hensu_name,value):
    #Trace_data
    Trace_data["text"] = "{} {}\n {}",format(type_name,hensu_name,value)
    Trace_data.layout = ""
    
        

## コード表示のsyntax遷移
def down_syntax(program_labels):
    def x():
        #program_point:int
        for i in range(20):
            if (program_labels[i]["bg"] == "#ffff6d") & (i != 19):
                program_labels[i]["bg"] = "#ffffff"
                program_labels[i+1]["bg"] = "#ffff6d"
                #program_point = i+1
                break
    return x

def up_syntax(program_labels):
    def x():
        #program_point:int
        for i in range(20):
            if (program_labels[i]["bg"] == "#ffff6d") & (i != 0):
                program_labels[i]["bg"] = "#ffffff"
                program_labels[i-1]["bg"] = "#ffff6d"
                #program_point = i-1
                break
    return x

#### 画面オブジェクト作成
def open_file(program_labels,Trace_data,Change_data):
    code = []
    def x():
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("C Files", "*.c"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        with open(filepath, "r") as input_file:
            program_codelist = input_file.readlines()
            for i in range(len(program_codelist)):
                program_labels[i]["text"] = program_codelist[i]
                code.append(program_codelist[i])
        
        for i in range(len(code)):
            idx = code[i].find('=')
            if(idx != -1):
                type_andName = ''.join(list(code[i])[:idx])
                space_split = type_andName.strip(' ').strip(';')
                space_split = space_split.split(' ')
                hensu_name = space_split[len(space_split)-1]
                type_name = ''.join(space_split[0:len(space_split)-1])
                value = ''.join(list(code[i])[idx+1:]).strip(' ').strip(';')
                #Trace_dataとChange_dataの設定
                make_trace_fig(Trace_data[i+1],Change_data[i],type_name,hensu_name,value)

    return x


if __name__ == "__main__":
    main()

