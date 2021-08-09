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
    highlight_position:int = 0
    token_position:int = highest_view+highlight_position
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

    def view_move(self,move):
        self.highest_view += move
        self.lowest_view += move
        self.token_position = self.highest_view+self.highlight_position

    def highlight_move(self,move):
        self.highlight_position += move
        self.token_position = self.highest_view+self.highlight_position
    
    def trace_list_set(self,row,col):
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
        self.trace_list.append(type_label) #0
        self.trace_list.append(name_label) #1
        self.trace_list.append(input_value_label) #2
        self.trace_list.append(initial_value_label) #3
        self.trace_list.append(arrowConst) #4
    
    def exist_list_set(self,row,col):
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
                self.exist_list.append(c)
        




def main():
    #### rootフレームの設定
    root = frk.FormK(24,20,0)
    root.title("C-Learning")
    root.geometry("1000x600")
    root.result = tk.StringVar()
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
    tc.trace_list_set(row=12,col=5)
    tc.exist_list_set(row=12,col=10)
    
    
    
    ### 不変なオブジェクトの設定 ###
    # 再生ボタンの設定
    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = down_highlight(tc)
    btnPlay.layout = "7,21,1,2"
    # 巻き戻しボタンの設定
    btn_play_back = frk.ButtonK()
    btn_play_back["text"] = "◀︎"
    btn_play_back["command"] = up_highlight(tc)
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
def down_trace_change(tc):
    if tc.token[tc.token_position][1] != " ": #highlightされた部分が代入文ならば...
        tc.trace_list[2]["relief"] = "groove"
        tc.trace_list[3]["relief"] = "groove"
        tc.trace_list[4]["text"] = "⇦"
        tc.trace_list[0]["text"] = tc.token[tc.token_position][0]
        tc.trace_list[1]["text"] = tc.token[tc.token_position][1]
        tc.trace_list[2]["text"] = tc.token[tc.token_position][2]

        for i in range(len(tc.exist_list)):
            if tc.exist_list[i][2] == 0:
                tc.exist_list[i][0]["text"] = tc.token[tc.token_position][1]
                tc.exist_list[i][1]["text"] = tc.token[tc.token_position][2]
                tc.exist_list[i][2] = 1
                return
        for i in range(len(tc.exist_list)):
            tc.exist_list[i][2] = 0
        tc.exist_list[0][2] = 1
        tc.exist_list[0][0]["text"] = tc.token[tc.token_position][1]
        tc.exist_list[0][1]["text"] = tc.token[tc.token_position][2]
    else:
        tc.trace_list[2]["relief"] = "flat"
        tc.trace_list[3]["relief"] = "flat"
        tc.trace_list[4]["text"] = " "
        tc.trace_list[0]["text"] = tc.token[tc.token_position][0]
        tc.trace_list[1]["text"] = tc.token[tc.token_position][1]
        tc.trace_list[2]["text"] = tc.token[tc.token_position][2]

def down_highlight(tc):
    def x():
        if tc.highlight_position != 19:
            tc.labels[tc.highlight_position]["bg"] = "#ffffff"
            tc.highlight_move(1)
            tc.labels[tc.highlight_position]["bg"] = "#ffff6d"
            if tc.token_position < len(tc.code):
                down_trace_change(tc)
    return x

def down_code(tc):
    """
    表示範囲を超える行数のプログラムの行を管理します．
    """
    def x():
        #tc.labelsの最下部がプログラムの終行でないか．
        if tc.lowest_view != len(tc.code)-1:
            tc.view_move(1)
            for i in range(20):
                tc.labels[i]["text"] = tc.code[tc.highest_view+i]
            if tc.token_position < len(tc.code):
                down_trace_change(tc)
            
    return x

def up_trace_change(tc):
    if tc.token[tc.token_position][1] != " ": #highlightされた部分が代入文ならば...
        tc.trace_list[2]["relief"] = "groove"
        tc.trace_list[3]["relief"] = "groove"
        tc.trace_list[4]["text"] = "⇦"
        tc.trace_list[0]["text"] = tc.token[tc.token_position][0]
        tc.trace_list[1]["text"] = tc.token[tc.token_position][1]
        tc.trace_list[2]["text"] = tc.token[tc.token_position][2]
    else:
        tc.trace_list[2]["relief"] = "flat"
        tc.trace_list[3]["relief"] = "flat"
        tc.trace_list[4]["text"] = " "
        tc.trace_list[0]["text"] = tc.token[tc.token_position][0]
        tc.trace_list[1]["text"] = tc.token[tc.token_position][1]
        tc.trace_list[2]["text"] = tc.token[tc.token_position][2]
    
    if tc.token[tc.token_position+1][1] != " ": #現在の行より下にexist_valueが含まれるなら，対象となるexist_valueを消去する．
        for i in range(len(tc.exist_list)):
            if tc.exist_list[i][0]["text"] == tc.token[tc.token_position+1][1]:
                tc.exist_list[i][2] = 0
                tc.exist_list[i][0]["text"] = " "
                tc.exist_list[i][1]["text"] = " "

def up_highlight(tc):
    def x():
        if tc.highlight_position != 0:
            tc.labels[tc.highlight_position]["bg"] = "#ffffff"
            tc.highlight_move(-1)
            tc.labels[tc.highlight_position]["bg"] = "#ffff6d"
            if tc.token_position+1 < len(tc.code):
                up_trace_change(tc)          
    return x

def up_code(tc):
    """
    表示範囲を超える行数のプログラムの行を管理します．
    """
    def x():
        #tc.labelsの最上部がプログラムの1行目でないか．
        if tc.highest_view != 0:
            tc.view_move(-1)
            for i in range(20):
                tc.labels[i]["text"] = tc.code[tc.highest_view+i]
            if tc.token_position+1 < len(tc.code):
                up_trace_change(tc)

    return x

"""
def token_check(tc,program):
    equal_idx = program.find('=')
    if(equal_idx != -1): # 「=」を含む文章である時
        input_value = program[equal_idx+1:].replace(' ','').replace(';','')

        left_equal = program[:equal_idx].strip()
        left_equals = left_equal.split()
        if len(left_equals) > 1: # 変数の宣言
            hensu_name = left_equals[-1]
            type_name = ''.join(left_equals[0:len(left_equals)-1])
        else: # 代入処理
            test(x)# ここから
"""

        





def open_file(tc):
    """
    ファイルの読み取りと，いくつかのデータの取得．
    tc.code：listの1要素を1行としてソースコードを取得．
    tc.labels：codeに格納された情報を基にGUI表示する部分を設定．
    tc.token：ソースコード1行ごとに定めた形式で必要なトークンを取り出し．
            　1行めのトークン：token[0]=[変数の型,変数名,代入する値] //空行や代入処理を行わない行では[ , , ]とする
    """
    def x():
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
            #token_check(tc,program)
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
