import numpy as np
import subprocess
from subprocess import PIPE
import re
import os
import glob


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

def create_charatoken(array_chara_list):
    new_arraylist = []
    for array_token in array_chara_list:
        value = array_token[0][1]
        value = list(value)
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
    print('GDB動作中．．．')

    # 使用する正規表現のパターン（正規表現のパターン見直し）
    # 1：
    # 正規表現のパターン
    pattern = r'([A-Za-z0-9_]*)\s*=\s*([A-Za-z1-9._][A-Za-z0-9._]*)'
    pattern1 = r'([A-Za-z0-9_]*)\s*=\s*{(.*)}'
    pattern2 = r'([A-Za-z0-9_]*)\s*=\s*\"(.*)\"'
    # 2：
    pattern_int = r'int\s+([A-Za-z0-9_]*)\s*=\s*[A-Za-z0-9_.]*'
    pattern_char = r'char\s+([A-Za-z-0-9_]*)\s*=\s*\'[A-Za-z0-9_.]*\''
    pattern_double = r'double\s+([A-Za-z0-9_]*)\s*=\s*[A-Za-z0-9_.]*'
    pattern_float = r'float\s+([A-Za-z0-9_]*)\s*=\s*[A-Za-z0-9_.]*'

    pattern_address = r'.*(0x[A-Za-z0-9]*).*'
    pattern_pointer = r'([A-Za-z0-9_]*)\s*=\s*(0x[A-Za-z0-9]*)'

    # アドレス対応表作成用変数
    variable_list = []
    address_dictionary = {}
    pointer_list = []

    # 変数、配列獲得用リスト
    local_list = []
    array_number_list = []
    array_chara_list = []

    # 実行ファイル生成
    proc = subprocess.run(['gcc', '-g', '-O0', filename])

    if os.name == 'nt':  # windows
        exe_name = 'a.exe'
    elif os.name == 'posix':  # linux/mac
        exe_name = 'a.out'

    # 対象ファイルを開いて文字列を取得
    with open(filename) as f:
        contents = f.read()

    # 実行行数獲得
    cls = contents.splitlines()
    cnt = 0

    for content in cls:
        cnt += 1
        if 'int main()' in content:
            first = cnt
    last = cnt

    # ローカル変数取得
    result = re.findall(pattern_int, contents)
    for res in result:
        variable_list.append(res)
    result = re.findall(pattern_char, contents)
    for res in result:
        variable_list.append(res)
    result = re.findall(pattern_double, contents)
    variable_list.append(result)
    result = re.findall(pattern_float, contents)
    variable_list.append(result)

    variable_list = list(filter(lambda a: len(a) != 0, variable_list))

    for l in variable_list:
        # 出力ファイル初期化
        with open('ex_out.txt', 'w') as output_file:
            pass

        input_data = 'set logging file ex_out.txt\nb main\nrun\nset logging on\n' + \
            'p &'+l[0]+'\nset logging off\ncontinue\nquit\n'
        proc = subprocess.run(['gdb', exe_name], input=input_data,
                              stdout=PIPE, stderr=PIPE, text=True)

        with open('ex_out.txt') as output_file:
            contents = output_file.read()

        contents = contents.replace('(gdb) ', '')

        result = re.findall(pattern_address, contents)
        address_dictionary.setdefault(l[0], result[0])

    # 回数分のローカル変数のリストを作成
    for i in range(first, last+1):

        # 出力ファイルのクリア
        with open('output.txt', 'w') as output_file:
            pass

        input_data = 'set logging file output.txt\nb ' + \
            str(i) + '\nrun\nset logging on\ninfo locals\nset logging off\ncontinue\nquit\n'
        proc = subprocess.run(
            ['gdb', exe_name], input=input_data, stdout=PIPE, stderr=PIPE, text=True)

        # 不要な部分を除く処理
        with open('output.txt') as output_file:
            contents = output_file.read()

        contents = contents.replace('(gdb) ', '')

        if contents == '':
            continue
        result = re.findall(pattern, contents)
        if len(result) != 0:
            local_list.append(result)
        result = re.findall(pattern1, contents)
        if len(result) != 0:
            array_number_list.append(result)
        result = re.findall(pattern2, contents)
        if len(result) != 0:
            array_chara_list.append(result)
        result = re.findall(pattern_pointer, contents)
        if len(result) != 0:
            for l in result:
                for key in address_dictionary:
                    if l[1] == address_dictionary[key]:
                        pointer_list.append(tuple([l[0], key]))

    if len(local_list) != 0:    
        ret_list = create_token(local_list)
    if len(array_number_list) != 0:
        array_number_list = create_arraytoken(array_number_list)
    if len(array_chara_list) != 0:
        array_chara_list = create_charatoken(array_chara_list)
    ret_list = list(np.array(ret_list) + np.array(array_number_list) + np.array(array_chara_list))
    print(ret_list)
    print(array_chara_list)
    print('完了！')


get_token('Test3.c')
