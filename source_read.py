import subprocess
from subprocess import PIPE
import re 
import os
import glob
import numpy as np

def create_token(local_list):
    ret_list = []
    for i in range(len(local_list)):
        if i == 0:
            set_prior = set(local_list[i])
        else:
            set_ = set(local_list[i])
            set_in = set_ - set_prior
            ret_list.append(list(set_in))
            set_prior = set_
    ret_list.append([])
    return ret_list

def create_arraytoken(array_list):
    new_arraylist = []
    for array_token in array_list:
        value = array_token[0][1]
        value = value.strip().split(',')
        num_list = [array_token[0][0]]
        new_tuple = tuple(num_list+value)
        input_token = [new_tuple]
        new_arraylist.append(input_token)
    ret_list = create_token(new_arraylist)
    return ret_list

        


def get_token(filepath):
    filename = None
    for f in glob.glob(filepath):
        filename = os.path.split(f)[1]

    pattern = r'([A-Za-z0-9].*)\s*=\s*([A-Za-z0-9].*)' #正規表現のパターン
    pattern1 = r'([A-Za-z0-9].*)\s*=\s*{([A-Za-z0-9, ].*)}'

    #対象ファイルを開いて文字列を取得
    with open(filepath) as f:
        contents = f.read()

    #main関数から最後の行まで
    cls = contents.splitlines()
    cnt = 0
    s = 'int main()'

    #実行ファイル生成
    proc = subprocess.run(['gcc', '-g', '-O0',filename])

    if os.name == 'nt': #windows
        exe_name = 'a.exe'
    elif os.name == 'posix': #linux/mac
        exe_name = 'a.out'

    for content in cls:
        cnt += 1
        if s in content:
            first = cnt
    last = cnt

    #回数分ローカル変数のリストを作成
    local_list = []
    array_list = []
    for i in range(first, last+1):
        #出力ファイルのクリア
        with open('output.txt', 'w') as output_file:
            pass
        
        #入力ファイルの作成
        with open('input.txt', 'w') as input_file:
            input_file.write('set logging file output.txt\n')
            input_file.write('b '+str(i)+'\n')
            input_file.write('run\nset logging on\ninfo locals\nset logging off\ncontinue\nquit\n')

        #GDBに処理を依頼
        with open('input.txt') as input_file:
            proc = subprocess.run(['gdb', exe_name], stdin=input_file, text=True)

        #不要な部分を除く処理
        with open('output.txt') as output_file:
            contents = output_file.read()
        
        contents = contents.replace('(gdb) ', '')
        with open('output.txt', 'w') as output_file:
            output_file.write(contents)
        if contents=='':
            break
        result = re.findall(pattern.replace(' ',''), contents)
        if len(result)!=0:
            local_list.append(result)
        result = re.findall(pattern1, contents)
        if len(result)!=0:
            array_list.append(result)
        
    ret_list = create_token(local_list)
    array_list = create_arraytoken(array_list)
    ret_list = list(np.array(ret_list) + np.array(array_list))
    return ret_list