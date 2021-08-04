# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from typing import Text
import Framework as frk
from tkinter import ttk
from dataclasses import dataclass, field
from tkinter.filedialog import askopenfilename, asksaveasfilename

@dataclass
class Trace:
    labels: list = field(default_factory=list)
    code: list = field(default_factory=list)
    token: list = field(default_factory=list)
    highest_view: int = 0
    lowest_view: int = 19
    """
    trace_list has 5 values.
    0:type
    1:name
    2:input_value
    3:initial_value
    4:arrow
    """
    trace_list: list = field(default_factory=list)
    """
    exist_list has 3 values.
    0:name_label
    1:initial_value_label
    2:used_flag(occupied is 1. empty is 0.)
    """
    exist_list: list = field(default_factory=list)

#### rootフレームの設定
root = frk.FormK(24,20,0)
root.title("C-Learning")
root.geometry("1000x600")
root.result = tk.StringVar()

def main():
    ### スタイル設定 ###
    style = ttk.Style() 
    style.configure('TButton', font = 
               ('calibri', 20, 'bold'),
                    borderwidth = '4') 
    style.map('Button'
         , foreground = [('active', '!disabled', 'green')]
         , background = [('active', 'black')]
         ) 
    ### プログラム表示部分の生成 ###
    tc = Trace()
    for i in range(20):
        tc.labels.append(frk.LabelK())
        tc.labels[i]["font"] = ("Arial", 16)
        tc.labels[i]["text"] = "\n"
        if i == 0:
            tc.labels[i]["bg"] = "#ffff6d"
        else:
            tc.labels[i]["bg"] = "#ffffff"
        tc.labels[i]["anchor"] = "nw"
        tc.labels[i].layout = "1,{},10,1".format(i+1)
    ### トレース図の生成(program progress) ###
    row = 12
    col = 5
    type_label = frk.LabelK() 
    name_label = frk.LabelK()
    initial_value_label = frk.LabelK()
    input_value_label = frk.LabelK()
    arrowConst = frk.LabelK()
    type_label.layout = "{},{},{},{}".format(row,col+2,3,1)
    name_label.layout = "{},{},{},{}".format(row+3,col,1,1)
    initial_value_label.layout = "{},{},{},{}".format(row+3,col+1,1,2)
    input_value_label.layout = "{},{},{},{}".format(row+5,col+1,1,2)
    arrowConst.layout = "{},{},{},{}".format(row+4,col+2,1,1)
    initial_value_label["relief"] = 'flat'
    input_value_label["relief"] = 'flat'
    type_label["anchor"] = "se"
    arrowConst["text"] = " "
    tc.trace_list.append(type_label) #0
    tc.trace_list.append(name_label) #1
    tc.trace_list.append(input_value_label) #2
    tc.trace_list.append(initial_value_label) #3
    tc.trace_list.append(arrowConst) #4
    for i in range(1):
        for j in range(4):
            a = frk.LabelK()
            a.layout = "{},10,1,1".format(12+2*j)
            b = frk.LabelK()
            b.layout = "{},11,1,2".format(12+2*j)
            used_flag = 0
            c = []
            c.append(a)
            c.append(b)
            c.append(used_flag)
            tc.exist_list.append(c)
    
    ### 不変なオブジェクトの設定 ###
    # 再生ボタンの設定
    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = down_syntax(tc)
    btnPlay.layout = "7,21,1,2"
    # 巻き戻しボタンの設定
    btn_play_back = frk.ButtonK()
    btn_play_back["text"] = "◀︎"
    btn_play_back["command"] = up_syntax(tc)
    btn_play_back.layout = "5,21,1,2"
    # プログラム上昇ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▲"
    btn_play_stop["command"] = up_code(tc)
    btn_play_stop.layout = "6,21,1,1"
    # プログラム下降ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▼"
    btn_play_stop["command"] = down_code(tc)
    btn_play_stop.layout = "6,22,1,1"
    # ファイル読み込みボタンの設定
    btn_file_open = frk.ButtonK()
    btn_file_open["text"] = "file open"
    btn_file_open["command"] = open_file(tc)
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
def up_code(tc):
    """
    表示範囲を超える行数のプログラムの行を管理します．(未実装)
    """
    def x():
        #tc.labelsの最上部がプログラムの1行目でないか．
        if tc.highest_view != 0:
            if len(tc.code)!=0:
                tc.highest_view -= 1
                tc.lowest_view -= 1
                for i in range(20):
                    tc.labels[i]["text"] = tc.code[tc.highest_view+i]
    return x

def down_code(tc):
    """
    表示範囲を超える行数のプログラムの行を管理します．(未実装)
    """
    def x():
        #tc.labelsの最下部がプログラムの終行でないか．
        if tc.lowest_view != len(tc.code)-1 and len(tc.code)!=0:
            tc.highest_view += 1
            tc.lowest_view += 1
            for i in range(20):
                tc.labels[i]["text"] = tc.code[tc.highest_view+i]
    return x

def label_cng(tc,index,clear_flag):
    """
    trace_listのテキストを変更します．
    index: プログラムの行に対応したindex
    clear_flag: 1の場合非表示(何も表示しない状態)にします．(空行などで使用)

    !!! !!!
    trace_list has 4 values.
    0:type_label
    1:name_label
    2:input_value_label
    3:initial_value_label
    !!! !!!
    """
    if clear_flag == 0:
        tc.trace_list[2]["relief"] = "groove"
        tc.trace_list[3]["relief"] = "groove"
        tc.trace_list[4]["text"] = "⇦"
        tc.trace_list[0]["text"] = tc.token[index][0]
        tc.trace_list[1]["text"] = tc.token[index][1]
        tc.trace_list[2]["text"] = tc.token[index][2]
    elif clear_flag == 1:
        tc.trace_list[2]["relief"] = "flat"
        tc.trace_list[3]["relief"] = "flat"
        tc.trace_list[4]["text"] = " "
        tc.trace_list[0]["text"] = tc.token[index][0]
        tc.trace_list[1]["text"] = tc.token[index][1]
        tc.trace_list[2]["text"] = tc.token[index][2]

def exist_cng(tc,index,clear_flag):
    """
    定義済みの変数の管理を行います．
    label_cngと同じ要領．
    """
    if clear_flag == 0:
        for i in range(len(tc.exist_list)):
            if tc.exist_list[i][2] == 0:
                tc.exist_list[i][0]["text"] = tc.token[index][1]
                tc.exist_list[i][1]["text"] = tc.token[index][2]
                tc.exist_list[i][2] = 1
                return
        for i in range(len(tc.exist_list)):
            tc.exist_list[i][2] = 0
        tc.exist_list[0][2] = 1
        tc.exist_list[0][0]["text"] = tc.token[index][1]
        tc.exist_list[0][1]["text"] = tc.token[index][2]
    elif clear_flag == 1:
        for i in range(len(tc.exist_list)):
            if tc.exist_list[i][0]["text"] == tc.token[index][1]:
                tc.exist_list[i][2] = 0
                tc.exist_list[i][0]["text"] = " "
                tc.exist_list[i][1]["text"] = " "



### syntaxの遷移を行います． ###
### down_syntax:program_labelのhighlightを1つ下へ変更します． ###
### up_syntax:program_labelのhighlightを1つ上へ変更します． ###
def down_syntax(tc):
    def x():
        for i in range(20):
            if (tc.labels[i]["bg"] == "#ffff6d") & (i != 19):
                tc.labels[i]["bg"] = "#ffffff"
                tc.labels[i+1]["bg"] = "#ffff6d"
                if i+1 < len(tc.token):
                    if tc.token[i+1][1] != " ":
                        label_cng(tc,i+1,0)
                        exist_cng(tc,i+1,0)
                    else:
                        label_cng(tc,i+1,1)
                break
    return x

def up_syntax(tc):
    def x():
        for i in range(20):
            if (tc.labels[i]["bg"] == "#ffff6d") & (i != 0):
                tc.labels[i]["bg"] = "#ffffff"
                tc.labels[i-1]["bg"] = "#ffff6d"
                if i < len(tc.token):
                    if tc.token[i-1][1] != " ":
                        label_cng(tc,i-1,0)
                    else:
                        label_cng(tc,i-1,1)
                    if tc.token[i][1] != " ":
                        exist_cng(tc,i,1)
                break
    return x


def open_file(tc):
    """
    ファイルを読み取り，
    program_labelのテキストの設定とコードの簡易な解析を行います(テスト用)．
    """
    def x():
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("C Files", "*.c"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        with open(filepath, "r") as input_file:
            text = input_file.readlines()
            for i in range(len(text)):
                tc.code.append(text[i])
                if i < 20:
                    tc.labels[i]["text"] = text[i]
                
        
        for i in range(len(tc.code)):
            idx = tc.code[i].find('=')
            a = []
            if(idx != -1):
                type_andName = ''.join(list(tc.code[i])[:idx])
                space_split = type_andName.strip(' ').replace(';','')
                space_split = space_split.split(' ')
                hensu_name = space_split[len(space_split)-1]
                type_name = ''.join(space_split[0:len(space_split)-1])
                value = ''.join(list(tc.code[i])[idx+1:]).strip(' ').replace(';','')
                a.append(type_name)
                a.append(hensu_name)
                a.append(value)
            else:
                a.append(" ")
                a.append(" ")
                a.append(" ")
            tc.token.append(a)
    return x



if __name__ == "__main__":
    main()

