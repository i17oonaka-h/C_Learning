# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from typing import Text
import Framework as frk
from tkinter import ttk
from dataclasses import dataclass, field
from tkinter.filedialog import askopenfilename, asksaveasfilename

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
    trace_label = frk.LabelK()
    trace_label["text"] = "program progress"
    trace_label.layout = "11,1,3,1"
    trace_label["relief"] = "groove"
    trace_label["bg"] = "#d7d7ff"

    btnPlay = frk.ButtonK()
    btnPlay["text"] = "▶︎"
    btnPlay["command"] = test(trace_label)
    btnPlay.layout = "7,21,1,2"