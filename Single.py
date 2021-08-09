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

@dataclass
class Trace:
    labels: list = field(default_factory=list)
    code: list = field(default_factory=list)
    token: list = field(default_factory=list)
    highest_view: int = 0
    lowest_view: int = 19
    highlight_position:int = 0
    token_position:int = highest_view+highlight_position
    trace_list: list = field(default_factory=list)
    exist_list: list = field(default_factory=list)
    type_color: dict = field(default_factory=dict)

    def view_move(self,move):
        self.highest_view += move
        self.lowest_view += move
        self.token_position = self.highest_view+self.highlight_position

    def highlight_move(self,move):
        self.highlight_position += move
        self.token_position = self.highest_view+self.highlight_position
    
    def labels_set(self):
        for i in range(20):
            self.labels.append(frk.LabelK())
            self.labels[i]["font"] = ("Arial", 16)
            self.labels[i]["text"] = "\n"
            if i == 0:
                self.labels[i]["bg"] = "#ffff6d"
            else:
                self.labels[i]["bg"] = "#ffffff"
            self.labels[i]["anchor"] = "nw"
            self.labels[i].layout = "1,{},10,1".format(i+1)

    def trace_list_set(self,row=12,col=3):
        """
        trace_list has 3 values.
        0:type
        1:name
        2:initial_value
        """
        type_label = frk.LabelK()
        name_label = frk.LabelK()
        initial_value_label = frk.LabelK()
        type_label.layout = "{},{},{},{}".format(row,col+2,4,1)
        name_label.layout = "{},{},{},{}".format(row+4,col,2,1)
        initial_value_label.layout = "{},{},{},{}".format(row+4,col+1,2,2)
        initial_value_label["relief"] = 'flat'
        type_label["anchor"] = "se"
        self.trace_list.append(type_label) #0
        self.trace_list.append(name_label) #1
        self.trace_list.append(initial_value_label) #2
    
    def exist_list_set(self,row=12,col=10):
        """
        exist_list has 3 values.
        0:name_label
        1:initial_value_label
        2:used_flag(occupied is 1. empty is 0.)
        """
        for y in range(3):
            for x in range(4):
                a = frk.LabelK()
                a.layout = "{},{},1,1".format(row+2*x,col+4*y)
                b = frk.LabelK()
                b.layout = "{},{},1,2".format(row+2*x,col+1+4*y)
                used_flag = 0
                c = []
                c.append(a)
                c.append(b)
                c.append(used_flag)
                self.exist_list.append(c)
    
    def token_append(self,type_,name_,value_):
        temporal = []
        temporal.append(type_)
        temporal.append(name_)
        temporal.append(value_)
        self.token.append(temporal)

    def token_set(self,sourcedata):
        main_flag = 0
        sourcedata_index = 1
        dict_exist = {}
        for i in range(len(self.code)):
            if main_flag == 0:
                self.token_append('','','')
                if 'int main()' in self.code[i]:
                    main_flag = 1
            else: # main_flag == 1
                """
                 source:[[], [('age ', "25 '\\031'")], [('height ', '166.69999999999999')], [('weight ', '58.5')], [], [], [], [], [], []]
                """
                print('code:{} \ source:{}'.format(self.code[i],sourcedata[sourcedata_index]))
                if len(sourcedata[sourcedata_index]) == 0:
                    self.token_append('','','')
                else:
                    name_ = sourcedata[sourcedata_index][0][0]
                    value_ = sourcedata[sourcedata_index][0][1]

                    equal_idx = self.code[i].find('=')
                    if equal_idx != -1: # イコールを含むなら...
                        type_andName = ''.join(list(self.code[i])[:equal_idx])
                        space_split = type_andName.strip(' ').replace(';','')
                        space_split = space_split.split(' ')
                        if len(space_split) > 1: # イコールの左側に2つ以上のトークンがある時，初期化処理
                            type_ = ''.join(space_split[0:len(space_split)-1])
                            print("type={},name={},value={}".format(type_,name_,value_))
                            if type_ == 'float' or type_ == 'double':
                                value_ = float(value_)
                                value_ = str(value_ )
                            self.token_append(type_, name_, value_)
                            dict_exist[name_] = type_

                        else: # イコールの左に1つだけトークンがある時，計算処理
                            type_ = dict_exist[name_]
                            self.token_append(type_, name_, value_)
                    else: # イコールを含まない初期化処理
                        type_andName = ''.join(list(self.code[i])[:equal_idx])
                        space_split = type_andName.strip(' ').replace(';','')
                        space_split = space_split.split(' ')
                        type_ = ''.join(space_split[0:len(space_split)-1])
                        self.token_append(type_, name_, '')
                sourcedata_index += 1
        
        print('finaltoken:{}'.format(self.token))




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
    tc.trace_list_set(row=12,col=3)
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
        tc.trace_list[0]["text"] = tc.token[tc.token_position][0]
        tc.trace_list[1]["text"] = tc.token[tc.token_position][1]
        tc.trace_list[2]["text"] = tc.token[tc.token_position][2]
    else:
        tc.trace_list[2]["relief"] = "flat"
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

def open_file(tc):
    def x():
        filepath = askopenfilename(
            filetypes=[("C Files", "*.c"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        sourcedata = get_token(filepath)
        with open(filepath, "r") as input_f:
            text = input_f.readlines()
            for i in range(len(text)):
                tc.code.append(text[i])
                if i < 20:
                    tc.labels[i]["text"] = text[i]
        
        tc.token_set(sourcedata)
    return x

if __name__ == "__main__":
    main()

