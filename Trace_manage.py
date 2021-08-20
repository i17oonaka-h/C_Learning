from os import name
import tkinter as tk
import math
import tkinter.ttk as ttk
from typing import Text
import Framework as frk
from tkinter import ttk
from dataclasses import dataclass, field
from source_read import get_token
from tkinter.filedialog import askopenfilename, asksaveasfilename


@dataclass
class Trace:

    program_labels: list = field(default_factory=list)
    labels_highest_view: int = 0
    labels_lowest_view: int = 19
    highlight_position:int = 0
    token_position:int = labels_highest_view+highlight_position
    array_position:int = 0

    code_info: list = field(default_factory=list)
    token: list = field(default_factory=list)
    variable_change_timing: dict = field(default_factory=dict)
       
    trace_object: list = field(default_factory=list) # trace_object_initializeを参照
    exist_object: list = field(default_factory=list) # exist_object_initializeを参照

    type_color: dict = field(default_factory=dict) # 型<->色の辞書



    # 汎用的なメソッド
    def code_pos_move(self,move):
        self.labels_highest_view += move
        self.labels_lowest_view += move
        self.token_position = self.labels_highest_view+self.highlight_position
        self.array_position = 0

    def highlight_move(self,move):
        self.highlight_position += move
        self.token_position = self.labels_highest_view+self.highlight_position
        self.array_position = 0
    


    # 初期化メソッド
    def program_labels_initialize(self): # program_labelsの初期設定
        """
        program_labels[0~19]:プログラムを表示する
        """
        for i in range(20):
            self.program_labels.append(frk.LabelK())
            self.program_labels[i]["font"] = ("Arial", 16)
            self.program_labels[i]["text"] = "\n"
            if i == 0:
                self.program_labels[i]["bg"] = "#ffff6d"
            else:
                self.program_labels[i]["bg"] = "#ffffff"
            self.program_labels[i]["anchor"] = "nw"
            self.program_labels[i].layout = "1,{},10,1".format(i+1)

    def trace_object_initialize(self,row=12,col=3):
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
           
    def exist_object_initialize(self,row=12,col=10):
        """
        左上のrow,colを指定して( 3x4=12 )個のオブジェクトを自動で配置
        exist_object has 3 values.
        0:変数名
        1:変数のvalue
        2:そのオブジェクトが使用されているか(使用済み is 1. 空 is 0.)
        """
        for y in range(3):
            for x in range(4):
                tmp_name_label = frk.LabelK()
                tmp_name_label.layout = "{},{},1,1".format(row+2*x,col+4*y)
                tmp_value_label = frk.LabelK()
                tmp_value_label.layout = "{},{},1,2".format(row+2*x,col+1+4*y)
                used_flag = 0
                tmp_list_inList = []
                tmp_list_inList.append(tmp_name_label)
                tmp_list_inList.append(tmp_value_label)
                tmp_list_inList.append(used_flag)
                self.exist_object.append(tmp_list_inList)


    # token_initializeで使用される関数群
    """

    # token_initialize <tokenの初期設定>
    |
    |- # sd_use_set <sourcedataを使用した設定>
    |  |
       |- # variable_set <変数時の設定>
       |  |
       |  |- # token_andTiming_set <トークンの作成と値の変更タイミングの保存>
       |  |
       |  |- # only_declare <宣言のみを行う行の時の設定>
       |     |
       |     |- # token_andTiming_set
       |
       |- # array_set <配列時の設定>
       |  |
       |  |- # token_andTiming_set
       |  |
       |  |- # only_declare
       |     |
       |     |- # token_andTiming_set

    """
    def token_initialize(self,sourcedata):
        """
        self.tokenは4つの要素をプログラムの行の数だけ持ちます．
        0:宣言代入フラグ→ 宣言文のとき1を持ちそれ以外で0
        1:値が上書きされた際に，古い値を保持する
        2:扱う変数の種類，変数(variable) or 配列(array) or ポインタ(pointer)
        3:変数の型を保持
        4:変数名を保持
        5~:変数の値を保持．配列の場合には後ろにさらに値が追加される
        """
        self.type_color = {'int':'#008000','float':'#1e90ff','double':'#0000cd','char':'#ffa500','unsignedchar':'#ffa500','double*':'#0000cd'}
        main_flag = 0
        sd_i = 1
        dict_name2type = {}
        dict_name2prior_value = {}
        for code_i in range(len(self.code_info)):
            if main_flag == 0:
                self.token_andTiming_set('','','',code_i)
                if 'int main()' in self.code_info[code_i]:
                    main_flag = 1           
            else:
                dict_name2type,dict_name2prior_value = self.sd_use_set(
                    sourcedata=sourcedata,
                    sd_i=sd_i,
                    code_i=code_i,
                    dict_name2type=dict_name2type,
                    dict_name2prior_value=dict_name2prior_value
                )
                sd_i += 1

        print(f'token:{self.token}')

    def sd_use_set(self,sourcedata,sd_i,code_i,dict_name2type,dict_name2prior_value):
        if len(sourcedata[sd_i]) == 0:
            self.token_andTiming_set('','','',code_i)
        else:
            token_type = sourcedata[sd_i][1]
            if token_type == 'variable' or token_type == 'pointer': # 配列でない...
                name_ = sourcedata[sd_i][0][0]
                value_ = sourcedata[sd_i][0][1]
                dict_name2type,dict_name2prior_value = self.variable_set(
                    name_=name_,
                    value_=value_,
                    code_i=code_i,
                    dict_name2type=dict_name2type,
                    dict_name2prior_value=dict_name2prior_value,
                    val_type=token_type
                    )   
            elif token_type == 'array':
                name_ = sourcedata[sd_i][0][0]
                value_len = len(sourcedata[sd_i][0])
                values_ = sourcedata[sd_i][0][1:value_len]
                dict_name2type,dict_name2prior_value = self.array_set(
                    name_=name_,
                    values_=values_,
                    code_i=code_i,
                    dict_name2type=dict_name2type,
                    dict_name2prior_value=dict_name2prior_value,
                    val_type=token_type
                )
        return dict_name2type,dict_name2prior_value

    def variable_set(self,name_,value_,code_i,dict_name2type,dict_name2prior_value,val_type):
        equal_i = self.code_info[code_i].find('=')
        if equal_i != -1:
            type_andName = ''.join(list(self.code_info[code_i])[:equal_i])
            type_andName = type_andName.strip(' ').replace(';','')
            type_andName_list = type_andName.split(' ')

            if len(type_andName_list) > 1: # イコールの左側に2つ以上のトークンがある時，宣言+初期化処理                  
                type_ = ''.join(type_andName_list[0:len(type_andName_list)-1])
                if ( type_ == 'float' or type_ == 'double' ) and ( not('*' in type_) ):
                    value_ = float(value_)
                    value_ = round(value_,2)
                    value_ = str(value_ )
                self.token_andTiming_set(type_, name_, value_,code_i,declare_flag=1,val_type=val_type)
                dict_name2type[name_] = type_
                dict_name2prior_value[name_] = value_
            
            else: # イコールの左に1つだけトークンがある時，計算処理
                type_ = dict_name2type[name_]
                prior_value = dict_name2prior_value[name_]
                if type_ == 'float' or type_ == 'double':
                    value_ = float(value_)
                    value_ = round(value_,2)
                    value_ = str(value_ )
                self.token_andTiming_set(type_, name_, value_,code_i,prior_value=prior_value,val_type=val_type)
                dict_name2prior_value[name_] = value_

        else: # イコールを含まない宣言のみの処理 
            dict_name2type,dict_name2prior_value = self.only_declare(
                name_=name_,
                value_=value_,
                code_i=code_i,
                equal_i=equal_i,
                dict_name2type=dict_name2type,
                dict_name2prior_value=dict_name2prior_value
                )
        return dict_name2type,dict_name2prior_value

    def array_set(self,name_,values_,code_i,dict_name2type,dict_name2prior_value,val_type):
        equal_i = self.code_info[code_i].find('=')
        name_ = name_ + '[0]'
        if equal_i != -1: # イコールを含むなら...
            type_andName = ''.join(list(self.code_info[code_i])[:equal_i])
            space_split = type_andName.strip(' ').replace(';','')
            space_split = space_split.split(' ')
            if len(space_split) > 1: # イコールの左側に2つ以上のトークンがある時，宣言+初期化処理                       
                type_ = ''.join(space_split[0:len(space_split)-1])
                self.token_andTiming_sets(type_, name_, values_,code_i,declare_flag=1,val_type='array')
                dict_name2type[name_] = type_
                dict_name2prior_value[name_] = values_
        else: # イコールを含まない宣言のみの処理
            dict_name2type,dict_name2prior_value = self.only_declare(
                name_=name_,
                value_=values_,
                code_i=code_i,
                equal_i=equal_i,
                dict_name2type=dict_name2type,
                dict_name2prior_value=dict_name2prior_value
                )
        return dict_name2type,dict_name2prior_value

    def token_andTiming_set(self, type_, name_, value_, code_num, declare_flag = 0, prior_value = '', val_type='variable'):
        temporal = []
        temporal.append(declare_flag) #0
        temporal.append(prior_value) #1
        temporal.append(val_type) #2
        temporal.append(type_) #3
        temporal.append(name_) #4
        temporal.append(value_) #5
        self.token.append(temporal)
        self.variable_change_timing[code_num] = name_

    def token_andTiming_sets(self, type_, name_, values_, code_num, declare_flag = 0, prior_value = '', val_type='variable'):
        temporal = []
        temporal.append(declare_flag) #0
        temporal.append(prior_value) #1
        temporal.append(val_type) #2
        temporal.append(type_) #3
        temporal.append(name_) #4
        for value_ in values_:
            if type_ == 'float' or type_ == 'double':
                    value_ = float(value_)
                    value_ = round(value_,2)
                    value_ = str(value_)
            temporal.append(value_) #5~
        self.token.append(temporal)
        self.variable_change_timing[code_num] = name_

    def only_declare(self,name_,value_,code_i,equal_i,dict_name2type,dict_name2prior_value):
        type_andName = ''.join(list(self.code_info[code_i])[:equal_i])
        type_andName = type_andName.strip(' ').replace(';','')
        type_andName_list = type_andName.split(' ')
        type_ = ''.join(type_andName_list[0:len(type_andName_list)-1])
        dict_name2type[name_] = type_
        dict_name2prior_value[name_] = value_
        self.token_andTiming_set(type_, name_, '',code_i,declare_flag=1)
        return dict_name2type,dict_name2prior_value


    # ボタン紐付け処理(一番上の処理)
    """
    
    # 表示の下降処理
    |
    |- # down_highlight
    |  |
    |  |- # down_trace_change
    |
    |- # down_code
    |  |
       |- # down_trace_change
    

    # 表示の上昇処理
    |
    |- # up_highlight
    |  |
    |  |- # up_trace_change
    |
    |- # up_code
    |  |
       |- # up_trace_change

    """
    def down_trace_change(self):
        now_pos = self.token_position
        now_token = self.token[now_pos]
        self.trace_object[0]["text"] = now_token[3]
        self.trace_object[1]["text"] = now_token[4]
        self.trace_object[2]["text"] = now_token[5]

        if now_token[4] != '': #highlightされた部分が宣言文・代入文ならば...
            self.trace_object[2]["relief"] = "groove"

            if now_token[0] == 0: # 代入処理
                for i in range(len(self.exist_object)):
                    if now_token[4] == self.exist_object[i][0]["text"]: # 今の行の変数と一致する定義済み変数がある時，valueのみ変更する
                        self.exist_object[i][1]["text"] = now_token[5]
                        return # 関数の終了
            else: # 変数の宣言    
                # 以下はまだexist_objectに変数がない == 未定義の時の処理
                for i in range(len(self.exist_object)): # exist_objectの空きを検索し，空きがあれば入れる
                    if self.exist_object[i][2] == 0:
                        self.exist_object[i][0]["text"] = self.token[now_pos][4]
                        self.exist_object[i][0]["fg"] = self.type_color[self.token[now_pos][3]]
                        self.exist_object[i][1]["text"] = self.token[now_pos][5]
                        self.exist_object[i][2] = 1
                        return
                for i in range(len(self.exist_object)): # 全てが埋まっていた時，空き状態をリセットする
                    self.exist_object[i][2] = 0
                self.exist_object[0][2] = 1
                self.exist_object[0][0]["text"] = self.token[self.token_position][4]
                self.exist_object[0][1]["text"] = self.token[self.token_position][5]

        else: # 宣言・代入文でない...
            self.trace_object[2]["relief"] = "flat"

    def down_highlight(self):
        def x():
            if self.highlight_position != 19:
                self.program_labels[self.highlight_position]["bg"] = "#ffffff"
                self.highlight_move(1)
                self.program_labels[self.highlight_position]["bg"] = "#ffff6d"
                if self.token_position < len(self.code_info):
                    self.down_trace_change()
        return x

    def down_code(self):
        """
        program_labelsのプログラム表示を1つ下へ遷移する
        """
        def x():
            #self.program_labelsの最下部がプログラムの終行でないか．
            print('labels_lowest_view:{}'.format(self.labels_lowest_view))
            if self.labels_lowest_view < len(self.code_info)-1:
                self.code_pos_move(1)
                for i in range(20):
                    if self.labels_highest_view+i >= len(self.code_info):
                        self.program_labels[i]["text"] = ''
                    else:
                        self.program_labels[i]["text"] = self.code_info[self.labels_highest_view+i]
                if self.token_position < len(self.code_info):
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
        self.trace_object[0]["text"] = self.token[self.token_position][3]
        self.trace_object[1]["text"] = self.token[self.token_position][4]
        self.trace_object[2]["text"] = self.token[self.token_position][5]
        if self.token[self.token_position][1] != '': #highlightされた部分が代入文ならば...
            self.trace_object[2]["relief"] = "groove" # value表示に枠線を追加
        else:
            self.trace_object[2]["relief"] = "flat"
        
        prior_pos = self.token_position+1
        prior_token = self.token[prior_pos]
        if prior_token[4] != '': #prior_tokenが宣言or代入
            if prior_token[0] == 1: #現在の行の一つ下が変数の宣言の時，exist_objectからその変数をexist_objectから消去する．
                for i in range(len(self.exist_object)): #exist_objectを探索
                    if self.exist_object[i][0]["text"] == prior_token[4]: # 名前が一致した部分を消去
                        self.exist_object[i][2] = 0
                        self.exist_object[i][0]["text"] = ""
                        self.exist_object[i][1]["text"] = ""
                        return
            else: # 代入処理の時prior_valueを参照し，exist_objectの値を変更
                for i in range(len(self.exist_object)): #exist_objectを探索
                    if self.exist_object[i][0]["text"] == prior_token[4]: # 名前が一致した部分のvalueを変更
                        self.exist_object[i][1]["text"] = prior_token[1]
                        return

    def up_highlight(self):
        def x():
            if self.highlight_position != 0: # highlight_position = 0 の時,上にこれ以上上がらない
                self.program_labels[self.highlight_position]["bg"] = "#ffffff" # 今のhighlight_positionの背景を白に
                self.highlight_move(-1) # highlight_position・token_positionを更新
                self.program_labels[self.highlight_position]["bg"] = "#ffff6d" # 更新後のhighlight_positionの背景を黄色に
                if self.token_position+1 < len(self.code_info): 
                    self.up_trace_change()   
        return x
    
    def up_code(self):
        """
        表示範囲を超える行数のプログラムの行を管理します．
        """
        def x():
            #self.program_labelsの最上部がプログラムの1行目でないか．
            if self.labels_highest_view != 0:
                self.code_pos_move(-1)
                for i in range(20):
                    if self.labels_highest_view+i >= len(self.code_info):
                        self.program_labels[i]["text"] = ''
                    else:
                        self.program_labels[i]["text"] = self.code_info[self.labels_highest_view+i]
                if self.token_position+1 < len(self.code_info):
                    self.up_trace_change()

        return x


    def up_array_view(self):
        def x():
            now_view_type = self.token[self.token_position][2]
            now_token = self.token[self.token_position]
            print(f'now_token{now_token}')
            print(f'now_view_type:{now_view_type}')
            if now_view_type == 'array':
                array_length = len(now_token[5:])
                if self.array_position+1 < array_length:
                    self.array_position += 1
                    self.trace_object[2]["text"] = now_token[5+self.array_position]
                    array_num = f'[{self.array_position}]'
                    self.trace_object[1]["text"] = now_token[4] + array_num
        return x
    
    def down_array_view(self):
        def x():
            now_view_type = self.token[self.token_position][2]
            now_token = self.token[self.token_position]
            print(f'now_token{now_token}')
            print(f'now_view_type:{now_view_type}')
            if now_view_type == 'array':
                if self.array_position-1 >= 0:
                    self.array_position -= 1
                    self.trace_object[2]["text"] = now_token[5+self.array_position]
                    array_num = f'[{self.array_position}]'
                    self.trace_object[1]["text"] = now_token[4] + array_num
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
                    self.code_info.append(text[i])
                    if i < 20:
                        self.program_labels[i]["text"] = text[i]
            
            self.token_initialize(sourcedata)
        return x