import os
import tkinter as tk
import tkinter.ttk as ttk
import openpyxl as px
import subprocess

import Framework as frk

from tkinter import ttk

class Constant:
    type_label = frk.LabelK()
    name_label = frk.LabelK()
    initial_value_label = frk.LabelK()
    input_value_label = frk.LabelK()
    arrowConst = frk.LabelK()
    arrowConst["text"] = "⇦"
    hide_label = frk.LabelK()
    hide_pos = None

    def __init__(self, type, name, initial_value, input_value, position, hide = 1):
        """
        type:型の変数
        name:変数名
        initial_value:現在の値
        input_value:代入される値
        position:表示ブロックの左上，position = [行，列，行の結合数，列の結合数]
        hide:初期状態として1なら非表示で，0なら表示
        """
        self.type_label.layout = "{},{},{},{}".format(position[0]+1,position[1],position[2],position[3])
        self.name_label.layout = "{},{},{},{}".format(position[0],position[1]+1,position[2],position[3])
        self.initial_value_label.layout = "{},{},{},{}".format(position[0]+1,position[1]+1,position[2],position[3])
        self.input_value_label.layout = "{},{},{},{}".format(position[0]+1,position[1]+3,position[2],position[3])
        self.arrowConst.layout = "{},{},{},{}".format(position[0]+1,position[1]+2,position[2],position[3])
        self.hide_pos = "{},{},{},{}".format(position[0],position[1],4,2)

        self.type_label["text"] = type
        self.name_label["text"] = name
        self.initial_value_label["text"] = initial_value
        self.input_value_label["text"] = input_value

    def set_position(self,position):
        self.type_label.layout = "{},{},{},{}".format(position[0]+1,position[1],position[2],position[3])
        self.name_label.layout = "{},{},{},{}".format(position[0],position[1]+1,position[2],position[3])
        self.initial_value_label.layout = "{},{},{},{}".format(position[0]+1,position[1]+1,position[2],position[3])
        self.input_value_label.layout = "{},{},{},{}".format(position[0]+1,position[1]+3,position[2],position[3])
        self.arrowConst.layout = "{},{},{},{}".format(position[0]+1,position[1]+2,position[2],position[3])