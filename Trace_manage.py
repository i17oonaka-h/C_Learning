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
    labels: list = field(default_factory=list) # program labels( len(labels) == 20 )
    code: list = field(default_factory=list) # code information
    token: list = field(default_factory=list) # token information(len(code) == len(token))
    change_timing: dict = field(default_factory=dict) # 変数が変更(定義)されるタイミング( 行数：変更あり(変数名)/変更なし('') )
    highest_view: int = 0 # program labelsの最も上の表示位置
    lowest_view: int = 19 # program labelsの最も下の表示位置
    highlight_position:int = 0 # ハイライトの位置
    token_position:int = highest_view+highlight_position # トレース表示の絶対位置
    trace_object: list = field(default_factory=list) # トレース図のオブジェクトのまとまり
    exist_object: list = field(default_factory=list) # 定義済み変数のオブジェクトのまとまり
    type_color: dict = field(default_factory=dict) # 型<->色の辞書

    def view_move(self,move): # highest_viewの変更とそれに応じたhighlight_positionの変更
        self.highest_view += move
        self.lowest_view += move
        self.token_position = self.highest_view+self.highlight_position

    def highlight_move(self,move): # highlight_positionの変更とそれに応じたhighlight_positionの変更
        self.highlight_position += move
        self.token_position = self.highest_view+self.highlight_position
    
    def labels_set(self): # labelsの初期設定
        """
        labels[0~19]:プログラムを表示する
        """
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

    def trace_object_set(self,row=12,col=3):
        """
        左上のrow,colを指定して3つのオブジェクトを自動で配置
        trace_object has 3 values.
        0:変数の型の表示
        1:変数の名前の表示
        2:変数のvalueの表示
        """
        type_label = frk.LabelK()
        name_label = frk.LabelK()
        initial_value_label = frk.LabelK()
        type_label.layout = "{},{},{},{}".format(row,col+2,4,1)
        name_label.layout = "{},{},{},{}".format(row+4,col,2,1)
        initial_value_label.layout = "{},{},{},{}".format(row+4,col+1,2,2)
        initial_value_label["relief"] = 'flat'
        type_label["anchor"] = "se"
        self.trace_object.append(type_label) #0
        self.trace_object.append(name_label) #1
        self.trace_object.append(initial_value_label) #2
    
    def exist_object_set(self,row=12,col=10):
        """
        左上のrow,colを指定して( 3x4=12 )個のオブジェクトを自動で配置
        exist_object has 3 values.
        0:変数名
        1:変数のvalue
        2:そのオブジェクトが使用されているか(使用済み is 1. 空 is 0.)
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
                self.exist_object.append(c)
    
    def token_timing_append(self, type_, name_, value_, code_num, declare_flag = 0, prior_value = ''): # token_setで使用
        """
        self.tokenは4つの要素をプログラムの行の数だけ持ちます．
        0:変数の型
        1:変数の名前
        2:変数のvalue
        3:フラグ / 変数の宣言を行う行なら1，それ以外0(down_trace_change用)
        4:以前，保持していた値を保持する(up_trace_change用)
        """
        temporal = []
        temporal.append(type_)
        temporal.append(name_)
        temporal.append(value_)
        temporal.append(declare_flag)
        temporal.append(prior_value)
        self.token.append(temporal)
        self.change_timing[code_num] = name_

    def token_set(self,sourcedata):
        """
        { 変数の型，変数の名前，変数のvalue }の塊をプログラムの行の数だけ生成
        """
        self.type_color = {'int':'#008000','float':'#1e90ff','double':'#0000cd','char':'#ffa500','unsignedchar':'#ffa500'}
        main_flag = 0
        sourcedata_index = 1
        dict_name2type = {}
        dict_name2prior_value = {}
        for i in range(len(self.code)):
            if main_flag == 0:
                self.token_timing_append('','','',i)
                if 'int main()' in self.code[i]:
                    main_flag = 1
            else: # main_flag == 1
                if len(sourcedata[sourcedata_index]) == 0:
                    self.token_timing_append('','','',i)
                else:
                    name_ = sourcedata[sourcedata_index][0][0]
                    value_ = sourcedata[sourcedata_index][0][1]

                    equal_idx = self.code[i].find('=')
                    if equal_idx != -1: # イコールを含むなら...
                        type_andName = ''.join(list(self.code[i])[:equal_idx])
                        space_split = type_andName.strip(' ').replace(';','')
                        space_split = space_split.split(' ')
                        if len(space_split) > 1: # イコールの左側に2つ以上のトークンがある時，宣言+初期化処理                           
                            type_ = ''.join(space_split[0:len(space_split)-1])
                            if type_ == 'float' or type_ == 'double':
                                value_ = float(value_)
                                value_ = str(value_ )
                            self.token_timing_append(type_, name_, value_,i,declare_flag=1)
                            dict_name2type[name_] = type_
                            dict_name2prior_value[name_] = value_

                        else: # イコールの左に1つだけトークンがある時，計算処理
                            type_ = dict_name2type[name_]
                            prior_value = dict_name2prior_value[name_]
                            self.token_timing_append(type_, name_, value_,i,prior_value=prior_value)
                            dict_name2prior_value[name_] = value_
                    else: # イコールを含まない宣言のみの処理
                        type_andName = ''.join(list(self.code[i])[:equal_idx])
                        space_split = type_andName.strip(' ').replace(';','')
                        space_split = space_split.split(' ')
                        type_ = ''.join(space_split[0:len(space_split)-1])
                        dict_name2type[name_] = type_
                        dict_name2prior_value[name_] = value_
                        self.token_timing_append(type_, name_, '',i,declare_flag=1)
                sourcedata_index += 1

    

    def down_trace_change(self):
        now_pos = self.token_position
        now_token = self.token[now_pos]
        self.trace_object[0]["text"] = now_token[0]
        self.trace_object[1]["text"] = now_token[1]
        self.trace_object[2]["text"] = now_token[2]

        if now_token[1] != '': #highlightされた部分が宣言文・代入文ならば...
            self.trace_object[2]["relief"] = "groove"

            if now_token[3] == 0: # 代入処理
                for i in range(len(self.exist_object)):
                    if now_token[1] == self.exist_object[i][0]["text"]: # 今の行の変数と一致する定義済み変数がある時，valueのみ変更する
                        self.exist_object[i][1]["text"] = now_token[2]
                        return # 関数の終了
            else: # 変数の宣言    
                # 以下はまだexist_objectに変数がない == 未定義の時の処理
                for i in range(len(self.exist_object)): # exist_objectの空きを検索し，空きがあれば入れる
                    if self.exist_object[i][2] == 0:
                        self.exist_object[i][0]["text"] = self.token[now_pos][1]
                        self.exist_object[i][0]["fg"] = self.type_color[self.token[now_pos][0]]
                        self.exist_object[i][1]["text"] = self.token[now_pos][2]
                        self.exist_object[i][2] = 1
                        return
                for i in range(len(self.exist_object)): # 全てが埋まっていた時，空き状態をリセットする
                    self.exist_object[i][2] = 0
                self.exist_object[0][2] = 1
                self.exist_object[0][0]["text"] = self.token[self.token_position][1]
                self.exist_object[0][1]["text"] = self.token[self.token_position][2]

        else: # 宣言・代入文でない...
            self.trace_object[2]["relief"] = "flat"

    def down_highlight(self):
        def x():
            if self.highlight_position != 19:
                self.labels[self.highlight_position]["bg"] = "#ffffff"
                self.highlight_move(1)
                self.labels[self.highlight_position]["bg"] = "#ffff6d"
                if self.token_position < len(self.code):
                    self.down_trace_change()
        return x

    def down_code(self):
        """
        labelsのプログラム表示を1つ下へ遷移する
        """
        def x():
            #self.labelsの最下部がプログラムの終行でないか．
            print('lowest_view:{}'.format(self.lowest_view))
            if self.lowest_view < len(self.code)-1:
                self.view_move(1)
                for i in range(20):
                    if self.highest_view+i >= len(self.code):
                        self.labels[i]["text"] = ''
                    else:
                        self.labels[i]["text"] = self.code[self.highest_view+i]
                if self.token_position < len(self.code):
                    self.down_trace_change()
        return x



    def up_trace_change(self):
        """
        highlight_positionが上に更新された時に呼び出し
        trace_object has 3 values.
        0:変数の型の表示
        1:変数の名前の表示
        2:変数のvalueの表示
        """
        self.trace_object[0]["text"] = self.token[self.token_position][0]
        self.trace_object[1]["text"] = self.token[self.token_position][1]
        self.trace_object[2]["text"] = self.token[self.token_position][2]
        if self.token[self.token_position][1] != '': #highlightされた部分が代入文ならば...
            self.trace_object[2]["relief"] = "groove" # value表示に枠線を追加
        else:
            self.trace_object[2]["relief"] = "flat"
        
        prior_pos = self.token_position+1
        prior_token = self.token[prior_pos]
        if prior_token[1] != '': #prior_tokenが宣言or代入
            if prior_token[3] == 1: #現在の行の一つ下が変数の宣言の時，exist_objectからその変数をexist_objectから消去する．
                for i in range(len(self.exist_object)): #exist_objectを探索
                    if self.exist_object[i][0]["text"] == prior_token[1]: # 名前が一致した部分を消去
                        self.exist_object[i][2] = 0
                        self.exist_object[i][0]["text"] = ""
                        self.exist_object[i][1]["text"] = ""
                        return
            else: # 代入処理の時prior_valueを参照し，exist_objectの値を変更
                for i in range(len(self.exist_object)): #exist_objectを探索
                    if self.exist_object[i][0]["text"] == prior_token[1]: # 名前が一致した部分のvalueを変更
                        self.exist_object[i][1]["text"] = prior_token[4]
                        return

    def up_highlight(self):
        def x():
            if self.highlight_position != 0: # highlight_position = 0 の時,上にこれ以上上がらない
                self.labels[self.highlight_position]["bg"] = "#ffffff" # 今のhighlight_positionの背景を白に
                self.highlight_move(-1) # highlight_position・token_positionを更新
                self.labels[self.highlight_position]["bg"] = "#ffff6d" # 更新後のhighlight_positionの背景を黄色に
                if self.token_position+1 < len(self.code): 
                    self.up_trace_change()   
        return x
    
    def up_code(self):
        """
        表示範囲を超える行数のプログラムの行を管理します．
        """
        def x():
            #self.labelsの最上部がプログラムの1行目でないか．
            if self.highest_view != 0:
                self.view_move(-1)
                for i in range(20):
                    if self.highest_view+i >= len(self.code):
                        self.labels[i]["text"] = ''
                    else:
                        self.labels[i]["text"] = self.code[self.highest_view+i]
                if self.token_position+1 < len(self.code):
                    self.up_trace_change()

        return x

    def open_file(self):
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
                    self.code.append(text[i])
                    if i < 20:
                        self.labels[i]["text"] = text[i]
            
            self.token_set(sourcedata)
        return x