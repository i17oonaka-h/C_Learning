# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import Framework as frk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

### global hensu ###
program_codelist = [] # open_file内でのみ値は変更されます．
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
    ### プログラム表示部分のラベルの生成 ###
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
    ### トレース図の生成(program progress) ###
    """
    trace_list has 4 values.
    0:type_label
    1:name_label
    2:input_value_label
    3:initial_value_label
    """
    trace_list = []
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
    trace_list.append(type_label) #0
    trace_list.append(name_label) #1
    trace_list.append(input_value_label) #2
    trace_list.append(initial_value_label) #3
    trace_list.append(arrowConst) #4
    for j in range(4):
        trace_list[j]["font"] = ("Arial", 16)
    ### 定義済みの関数を保管するラベルの定義 ###
    """
    exist_list has 3 values.
    0:name_label
    1:initial_value_label
    2:used_flag(occupied is 1. empty is 0.)
    """
    exist_list = []
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
            exist_list.append(c)
    ### 不変なオブジェクトの設定 ###
    # 再生ボタンの設定
    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = down_syntax(program_labels,trace_list,exist_list)
    btnPlay.layout = "7,21,1,2"
    # 巻き戻しボタンの設定
    btn_play_back = frk.ButtonK()
    btn_play_back["text"] = "◀︎"
    btn_play_back["command"] = up_syntax(program_labels,trace_list,exist_list)
    btn_play_back.layout = "5,21,1,2"
    # プログラム上昇ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▲"
    btn_play_stop["command"] = root.destroy
    btn_play_stop.layout = "6,21,1,1"
    # プログラム下降ボタンの設定
    btn_play_stop = frk.ButtonK()
    btn_play_stop["text"] = "▼"
    btn_play_stop["command"] = root.destroy
    btn_play_stop.layout = "6,22,1,1"
    # ファイル読み込みボタンの設定
    btn_file_open = frk.ButtonK()
    btn_file_open["text"] = "file open"
    btn_file_open["command"] = open_file(program_labels,trace_list)
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
def up_code(program_labels_trace_fig):
    """
    表示範囲を超える行数のプログラムの行を管理します．(未実装)
    """
    for i in range(20):
        if len(program_codelist) > 20:
            program_labels_trace_fig[i]["text"] = program_codelist[i]


def label_cng(trace_list,index,clear_flag):
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
        trace_list[2]["relief"] = "groove"
        trace_list[3]["relief"] = "groove"
        trace_list[4]["text"] = "⇦"
        trace_list[0]["text"] = program_codelist[index][0]
        trace_list[1]["text"] = program_codelist[index][1]
        trace_list[2]["text"] = program_codelist[index][2]
    elif clear_flag == 1:
        trace_list[2]["relief"] = "flat"
        trace_list[3]["relief"] = "flat"
        trace_list[4]["text"] = " "
        trace_list[0]["text"] = program_codelist[index][0]
        trace_list[1]["text"] = program_codelist[index][1]
        trace_list[2]["text"] = program_codelist[index][2]

def exist_cng(exist_list,index,clear_flag):
    """
    定義済みの変数の管理を行います．
    label_cngと同じ要領．
    """
    if clear_flag == 0:
        for i in range(len(exist_list)):
            if exist_list[i][2] == 0:
                exist_list[i][0]["text"] = program_codelist[index][1]
                exist_list[i][1]["text"] = program_codelist[index][2]
                exist_list[i][2] = 1
                return
        for i in range(len(exist_list)):
            exist_list[i][2] = 0
        exist_list[0][2] = 1
        exist_list[0][0]["text"] = program_codelist[index][1]
        exist_list[0][1]["text"] = program_codelist[index][2]
    elif clear_flag == 1:
        for i in range(len(exist_list)):
            if exist_list[i][0]["text"] == program_codelist[index][1]:
                exist_list[i][2] = 0
                exist_list[i][0]["text"] = " "
                exist_list[i][1]["text"] = " "



### syntaxの遷移を行います． ###
### down_syntax:program_labelのhighlightを1つ下へ変更します． ###
### up_syntax:program_labelのhighlightを1つ上へ変更します． ###
def down_syntax(program_labels,trace_list,exist_list):
    def x():
        for i in range(20):
            if (program_labels[i]["bg"] == "#ffff6d") & (i != 19):
                program_labels[i]["bg"] = "#ffffff"
                program_labels[i+1]["bg"] = "#ffff6d"
                if i+1 < len(program_codelist):
                    if program_codelist[i+1][1] != " ":
                        label_cng(trace_list,i+1,0)
                        exist_cng(exist_list,i+1,0)
                    else:
                        label_cng(trace_list,i+1,1)
                break
    return x

def up_syntax(program_labels,trace_list,exist_list):
    def x():
        for i in range(20):
            if (program_labels[i]["bg"] == "#ffff6d") & (i != 0):
                program_labels[i]["bg"] = "#ffffff"
                program_labels[i-1]["bg"] = "#ffff6d"
                if i < len(program_codelist):
                    if program_codelist[i-1][1] != " ":
                        label_cng(trace_list,i-1,0)
                    else:
                        label_cng(trace_list,i-1,1)
                    if program_codelist[i][1] != " ":
                        exist_cng(exist_list,i,1)
                break
    return x


def open_file(program_labels,trace_list):
    """
    ファイルを読み取り，
    program_labelのテキストの設定とコードの簡易な解析を行います(テスト用)．
    """
    code = []
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
                program_labels[i]["text"] = text[i]
                code.append(text[i])
        
        for i in range(len(code)):
            idx = code[i].find('=')
            a = []
            if(idx != -1):
                type_andName = ''.join(list(code[i])[:idx])
                space_split = type_andName.strip(' ').replace(';','')
                space_split = space_split.split(' ')
                hensu_name = space_split[len(space_split)-1]
                type_name = ''.join(space_split[0:len(space_split)-1])
                value = ''.join(list(code[i])[idx+1:]).strip(' ').replace(';','')
                a.append(type_name)
                a.append(hensu_name)
                a.append(value)
            else:
                a.append(" ")
                a.append(" ")
                a.append(" ")
            program_codelist.append(a)     
    return x


if __name__ == "__main__":
    main()

