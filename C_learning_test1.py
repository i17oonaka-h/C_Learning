import tkinter as tk


program_type = {"int":1,"float":1,"double":1,"char":2} #型を持つ辞書
program_operator = {"=":1} #演算子を持つ辞書

#GUI周りの変数をまとめて定義
window = tk.Tk()
for i in range(3):
    window.rowconfigure(i, weight=1, minsize=50)
    window.columnconfigure(i, weight=1, minsize=75)


#def type_process(type_code:str): #型関係の処理を担当する関数
#def operator_process(process_code:str): #演算子関係の処理を担当する関数
def cell_set(row_f:int,column_f:int,program_list:list,frame):
    type_index:int #型を持つ配列のindexを格納
    variable_index:int #変数名を持つindexを格納
    value_index:int #変数の中身を指す部分のindexを格納
    for j in range(10):
        if program_list[j] == ";": #変数宣言，値の入力などの終了のチェック
            break
        if program_list[j] in program_type.keys(): #program_list[j]は型を表す？ 
            print("program_type={},variable={}".format(program_list[j],program_list[j+1]))
            type_index = j
            variable_index = j+1
        if program_list[j] in program_operator.keys(): #program_list[j]は演算子を表す？
            value_index = j+1
    frame.grid(row=row_f,column=column_f,padx=5,pady=5)
    label = tk.Label(master=frame,text=f"{program_list[variable_index]}[{program_list[type_index]}]\n {program_list[value_index]} ")
    label.pack(padx=5,pady=5)

def main():
    # プログラムのロード
    program_list = [["\end"]*10]*4
    program_list[0] = ["unsigned","char","age","=","25",";"]
    program_list[1] = ["double","height","=","166.7",";"]
    program_list[2] = ["float","weight","=","58.5",";"]

    #プログラムのチェック
    for i in range(3):
        frame = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1
        )
        cell_set(1,i,program_list[i],frame)
    window.mainloop()

if __name__ == "__main__":
    main()