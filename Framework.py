#### インポート
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

class FormK(tk.Tk):
    pass

    def __init__(self, p_max_row, p_max_col, p_padding):
        super(FormK, self).__init__()

        ## レイアウト用プロパティ
        self.MAX_ROW = p_max_row
        self.MAX_COL = p_max_col
        self.PAD_OUT = p_padding
        self.PAD_IN  = p_padding

        # 定数設定
        self.CONST_MSG_ICON_INFO = 1
        self.CONST_MSG_ICON_ALERT = 2
        self.CONST_MSG_ICON_ERROR = 3

        self.CONST_MSG_QUES_YES_NO = 1
        self.CONST_MSG_QUES_OK_CANCEL = 2
        self.CONST_MSG_QUES_RETRY_CANCEL = 4

    ## 定義時の画面サイズ設定
    def geometry(self,newGeometry=None):
        super(FormK, self).geometry(newGeometry)
        sp = newGeometry.split("x")
        self.WIDTH  = int(sp[0])
        self.HEIGHT = int(sp[1])


    ## メッセージボックス
    def MsgBox(self,p_msg,p_title,p_icon,p_ques):

        # 返却値初期値
        o_res = None

        if (p_ques == None):
            if (p_icon == self.CONST_MSG_ICON_INFO):
                messagebox.showinfo(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ALERT):
                messagebox.showwarning(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ERROR):
                messagebox.showerror(p_title,p_msg)
        if (p_ques == self.CONST_MSG_QUES_YES_NO):
            if (p_icon == self.CONST_MSG_ICON_INFO):
                o_res = messagebox.askyesno(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ALERT):
                o_res = messagebox.askyesno(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ERROR):
                o_res = messagebox.askyesno(p_title,p_msg)
        if (p_ques == self.CONST_MSG_QUES_OK_CANCEL):
            if (p_icon == self.CONST_MSG_ICON_INFO):
                o_res = messagebox.askokcancel(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ALERT):
                o_res = messagebox.askokcancel(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ERROR):
                o_res = messagebox.askokcancel(p_title,p_msg)
        if (p_ques == self.CONST_MSG_QUES_RETRY_CANCEL):
            if (p_icon == self.CONST_MSG_ICON_INFO):
                o_res = messagebox.askretrycancel(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ALERT):
                o_res = messagebox.askretrycancel(p_title,p_msg)
            if (p_icon == self.CONST_MSG_ICON_ERROR):
                o_res = messagebox.askretrycancel(p_title,p_msg)
        return o_res

    ## オブジェクトを配置する
    def set_layout(self):

        n_height_in = self.HEIGHT - (self.PAD_OUT * 2)
        n_height_one = (n_height_in - ((self.MAX_ROW - 1) * self.PAD_IN)) / self.MAX_ROW

        n_width_in = self.WIDTH - (self.PAD_OUT * 2)
        n_width_one = (n_width_in  - ((self.MAX_COL - 1) * self.PAD_IN)) / self.MAX_COL
        for v in self.children:
            try:
                if self.children[v].layout != None:
                    sp = self.children[v].layout.split(",")

                    self.children[v].place_configure(
                        relx     =round((float(self.PAD_OUT) + ((int(sp[0])-1) * n_width_one)  + ((int(sp[0]) - 1) * self.PAD_IN)) / self.WIDTH ,4)
                       ,rely     =round((float(self.PAD_OUT) + ((int(sp[1])-1) * n_height_one) + ((int(sp[1]) - 1) * self.PAD_IN)) / self.HEIGHT ,4)
                       ,relwidth =round(((int(sp[2]) * n_width_one)  + ((int(sp[2]) - 1) * self.PAD_IN)) / self.WIDTH ,4)
                       ,relheight=round(((int(sp[3]) * n_height_one) + ((int(sp[3]) - 1) * self.PAD_IN)) / self.HEIGHT ,4)
                    )
            except:
                print("No TkinterK Object(" + v +").")
                pass


        pass

class ButtonK(tk.Button):
    pass

    def __init__(self):
        super(ButtonK, self).__init__()
        self.layout = None


class EntryK(tk.Entry):
    pass

    def __init__(self):
        super(EntryK, self).__init__()
        self.layout = None
        self["highlightthickness"] = 1
        self.config(highlightcolor= "red")

class ProgressbarK(ttk.Progressbar):
    pass

    def __init__(self):
        super(ProgressbarK, self).__init__()
        self.layout = None

class LabelK(tk.Label):
    pass

    def __init__(self):
        super(LabelK, self).__init__()
        self.layout = None

class TreeviewK(ttk.Treeview):
    pass

    def __init__(self):
        super(TreeviewK, self).__init__()
        self.layout = None

class LabelFrameK(ttk.LabelFrame):
    pass

    def __init__(self):
        super(LabelFrameK,self).__init__()
        self.layout = None