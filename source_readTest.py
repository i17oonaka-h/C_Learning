import subprocess
from subprocess import PIPE
import re 
import os

'''
やること：ポインタへの対応
'''

print('GDB動作中．．．')

###使用する正規表現のパターン（正規表現のパターン見直し）
#1：
pattern = r'([A-Za-z0-9_]*)\s*=\s*([A-Za-z0-9._]+)' #正規表現のパターン
pattern1 = r'([A-Za-z0-9_]*)\s*=\s*{(.*)}'
pattern2 = r'([A-Za-z0-9_]*)\s*=\s*\"(.*)\"'
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
proc = subprocess.run(['gcc', '-g', '-O0', 'Test4.c'])

if os.name == 'nt': #windows
    exe_name = 'a.exe'
elif os.name == 'posix': #linux/mac
    exe_name = 'a.out'

###対象ファイルを開いて文字列を取得
with open('Test4.c') as f:
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

    input_data = 'set logging file ex_out.txt\nb main\nrun\nset logging on\n'+'p &'+l[0]+'\nset logging off\ncontinue\nquit\n'
    proc = subprocess.run(['gdb', exe_name], input=input_data, stdout=PIPE, stderr=PIPE, text=True)

    with open('ex_out.txt') as output_file:
        contents = output_file.read()   
        
    contents = contents.replace('(gdb) ', '')

    result = re.findall(pattern_address, contents)
    if len(result) != 0:
        address_dictionary.setdefault(l, result[0])

###回数分のローカル変数のリストを作成
for i in range(first, last+1):

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
    result = re.findall(pattern, contents)
    if len(result)!=0:
        local_list.append(result)
    result = re.findall(pattern1, contents)
    if len(result)!=0:
        array_list.append(result)
    result = re.findall(pattern2, contents)
    if len(result)!=0:
        array_list.append(result)
    result = re.findall(pattern_pointer, contents)
    if len(result)!=0:
        for l in result:
            flag = False
            for key in address_dictionary:
                if l[1] == address_dictionary[key]:
                    flag = True
                    pointer_list.append(tuple([l[0],key]))
            if flag == False:
                pointer_list.append(tuple([l[0],'']))
                
print('\n')
print(local_list)
print('\n')
print(array_list)
print('\n')
print(address_dictionary)
print('\n')
print(pointer_list)

print('完了！')