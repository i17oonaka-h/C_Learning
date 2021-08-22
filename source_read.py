from typing import NewType
import numpy as np
import subprocess
from subprocess import PIPE
import re
import os
import glob
from copy import deepcopy


def create_token(local_list, token_type='variable'):
    ret_list = []
    for i in range(len(local_list)):
        if i == 0:
            set_prior = set(local_list[i])
        else:
            set_ = set(local_list[i])
            set_in = set_ - set_prior
            set_in2list_in = list(set_in)
            if len(set_in2list_in) != 0:
                set_in2list_in.append(token_type)
            ret_list.append(set_in2list_in)
            set_prior = set_
    ret_list.append([])
    return ret_list


def create_arraytoken(array_list, token_type='array'):
    new_arraylist = []
    for array_token in array_list:
        input_token = []
        for array_single in array_token:
            value = array_single[1]
            if ',' in value:
                value = value.strip().split(',')
            else:
                value = list(value)
            num_list = [array_single[0]]
            new_tuple = tuple(num_list+value)
            input_token.append(new_tuple)
        new_arraylist.append(input_token)
    print(new_arraylist)
    ret_list = create_token(new_arraylist, token_type=token_type)
    return ret_list


def get_token(filepath):
    filename = os.path.basename(filepath)

    print('GDB動作中．．．')

    ###使用する正規表現のパターン（正規表現のパターン見直し）
    #1：
    pattern_local = r'([A-Za-z0-9_]*)\s*=\s*([A-Za-z0-9._]+)' #正規表現のパターン
    pattern_except = r'([A-Za-z0-9_]*)\s*=\s*(0x[A-Za-z0-9._]*)'
    pattern_array = r'([A-Za-z0-9_]*)\s*=\s*{(.*)}'
    pattern_array_char = r'([A-Za-z0-9_]*)\s*=\s*\"(.*)\"'
    #2：
    #通常変数
    pattern_variable_list = []
    pattern_variable_list.append(r'int\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')     #int
    pattern_variable_list.append(r'long\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')    #long
    pattern_variable_list.append(r'short\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')   #short
    pattern_variable_list.append(r'char\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')    #char1
    pattern_variable_list.append(r'char\s+([A-Za-z-0-9_]*)\s*=*\s*\'.*\';')           #char2
    pattern_variable_list.append(r'double\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')  #double
    pattern_variable_list.append(r'float\s+([A-Za-z0-9_]*)\s*=*\s*[A-Za-z0-9_.]*;')   #float
    #配列変数
    pattern_variable_list.append(r'int\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #int
    pattern_variable_list.append(r'long\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #long
    pattern_variable_list.append(r'short\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #short
    pattern_variable_list.append(r'char\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #char
    pattern_variable_list.append(r'double\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #double
    pattern_variable_list.append(r'float\s+([A-Za-z0-9_]*)\[.*\]\s*=*\s*.*;')       #float

    pattern_address = r'.*(0x[A-Za-z0-9]*).*'
    pattern_pointer = r'([A-Za-z0-9_]*)\s*=\s*(0x[A-Za-z0-9]*)'

    ###アドレス対応表作成用変数
    variable_list = []
    address_dictionary = {}
    pointer_list = []

    ###変数、配列獲得用リスト
    local_list = []
    array_list = []

    ###通常変数
    flag = False

    ###実行ファイル生成
    proc = subprocess.run(['gcc', '-g', '-O0', filename])

    if os.name == 'nt': #windows
        exe_name = 'a.exe'
    elif os.name == 'posix': #linux/mac
        exe_name = 'a.out'

    ###対象ファイルを開いて文字列を取得
    with open(filename) as f:
        contents = f.read()

    ###実行行数獲得
    cls = contents.splitlines()
    cnt = 0

    for content in cls:
        cnt += 1
        if 'int main()' in content:
            first = cnt
    last = cnt

    ###ローカル変数取得
    for p in pattern_variable_list:
        result = re.findall(p, contents)
        if len(result) != 0:
            for x in result:
                variable_list.append(x)

    variable_list = list(filter(lambda a: len(a)!=0, variable_list))

    for l in variable_list:
        #出力ファイル初期化
        with open('ex_out.txt', 'w') as output_file:
            pass

        input_data = 'set logging file ex_out.txt\nb main\nrun\nset logging on\n'+'p &'+l+'\nset logging off\ncontinue\nquit\n'
        proc = subprocess.run(['gdb', exe_name], input=input_data, stdout=PIPE, stderr=PIPE, text=True)

        with open('ex_out.txt') as output_file:
            contents = output_file.read()   

        contents = contents.replace('(gdb) ', '')

        result = re.findall(pattern_address, contents)
        if len(result) != 0:
            address_dictionary.setdefault(l, result[0])

    ###回数分のローカル変数のリストを作成
    for i in range(first, last+1):

        #初期化
        tmp_list = []
        except_list = []

        #出力ファイルのクリア
        with open('output.txt', 'w') as output_file:
            pass

        input_data = 'set logging file output.txt\nb ' + str(i) + '\nrun\nset logging on\ninfo locals\nset logging off\ncontinue\nquit\n'
        proc = subprocess.run(['gdb', exe_name], input=input_data, stdout=PIPE, stderr=PIPE, text=True)

        #不要な部分を除く処理
        with open('output.txt') as output_file:
            contents = output_file.read()
        
        contents = contents.replace('(gdb) ', '')

        if contents=='':
            continue
        #通常変数
        result = re.findall(pattern_except, contents)
        if len(result)!=0:
            except_list = deepcopy(result)
        result = re.findall(pattern_local, contents)
        if len(result)!=0:
            for x in result:
                for y in except_list:
                    if x == y:
                        result.remove(x)
            local_list.append(result)
        #配列
        result = re.findall(pattern_array, contents)
        if len(result)!=0:
            for x in result:
                tmp_list.append(x)
        result = re.findall(pattern_array_char, contents)
        if len(result)!=0:
            for x in result:
                tmp_list.append(x)
        array_list.append(tmp_list)
        #ポインター
        result = re.findall(pattern_pointer, contents)
        if len(result)!=0:
            for l in result:
                flag = False
                for key in address_dictionary:
                    if l[1] == address_dictionary[key]:
                        flag = True
                        pointer_list.append([tuple([l[0],key])])
                if flag == False:
                    pointer_list.append([tuple([l[0],''])])

    local_flag=False
    array_flag=False
    pointer_flag=False
    if len(local_list) != 0:    
        local_list = create_token(local_list, token_type='variable')
        local_flag=True
    if len(array_list) != 0:
        array_list = create_arraytoken(array_list, token_type='array')
        array_flag=True
    if len(pointer_list) != 0:
        pointer_list = create_token(pointer_list, token_type='pointer')
        pointer_flag=True
    
    first_flag=True
    ret_list = None
    if local_flag:
        if first_flag:
            local_list.append([0])
            ret_list = np.array(local_list)
            print(f'ret_list:{ret_list}')
            first_flag=False
    if array_flag:
        if first_flag:
            ret_list = np.array(array_list)
            first_flag=False
        else:
            array_list.append([0])
            print(f'ret_list:{ret_list}')
            print(f'array_list:{array_list}')
            ret_list = ret_list + np.array(array_list)
    if pointer_flag:
        if first_flag:
            ret_list = np.array(pointer_list)
            first_flag=False
        else:
            pointer_list.append([0])
            ret_list = ret_list + np.array(pointer_list)
    ret_list = ret_list[0:ret_list.shape[0]-1]
    print(f'ret_list:{ret_list}')
    print(address_dictionary)
    print('完了！')
    return ret_list,address_dictionary

if __name__ == '__main__':
    filepath = '/Users/i17oonaka/workspace/souzouEnsyu/Test4.c'
    get_token(filepath=filepath)
    