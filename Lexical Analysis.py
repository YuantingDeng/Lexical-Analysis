# coding=utf-8
import string
import sys
import codecs
keywords = {}

keywords['and'] = 1
keywords['array'] = 2
keywords['begin'] = 3
keywords['bool'] = 4
keywords['call'] = 5
keywords['case'] = 6
keywords['char'] = 7
keywords['constant'] = 8
keywords['dim'] = 9
keywords['do'] = 10
keywords['else'] = 11
keywords['end'] = 12
keywords['false'] = 13
keywords['for'] = 14
keywords['if'] = 15
keywords['input'] = 16
keywords['integer'] = 17
keywords['not'] = 18
keywords['of'] = 19
keywords['or'] = 20
keywords['output'] = 21
keywords['procedure'] = 22
keywords['program'] = 23
keywords['read'] = 24
keywords['real'] = 25
keywords['repeat'] = 26
keywords['set'] = 27
keywords['stop'] = 28
keywords['then'] = 29
keywords['to'] = 30
keywords['true'] = 31
keywords['until'] = 32
keywords['var'] = 33
keywords['while'] = 34
keywords['write'] = 35
keywords['标识符'] = 36
keywords['整数'] = 37
keywords['字符常数'] = 38
keywords['('] = 39
keywords[')'] = 40
keywords['*'] = 41
keywords['*/'] = 42
keywords['+'] = 43
keywords[','] = 44
keywords['-'] = 45
keywords['.'] = 46
keywords['..'] = 47
keywords['/'] = 48
keywords['/*'] = 49
keywords[':'] = 50
keywords[':='] = 51
keywords[';'] = 52
keywords['<'] = 53
keywords['<='] = 54
keywords['<>'] = 55
keywords['='] = 56
keywords['>'] = 57
keywords['>='] = 58
keywords['['] = 59
keywords[']'] = 60

# 变量
# keywords['var'] = 301

# 常量
# keywords['const'] = 401

# Error
# keywords['const'] = 501

signdict = {} #signdict是无用的
signlist = []
keylist = []

# 预处理函数，将文件中的空格，换行等无关字符处理掉
def pretreatment(file_name):
    try:
        #fp_read = open(file_name).read()
        fp_read = codecs.open(file_name, 'r', encoding='gbk')
        fp_write = codecs.open('file.tmp', 'w')
        sign = 0 #用来控制
        while True:
            read = fp_read.readline()
            if not read:
                break
            length = len(read)
            i = -1
            while i < length - 1:
                i += 1
                if sign == 0:
                    if read[i] == ' ':
                        continue
                elif sign == 10:#跳过读取
                    if "*/" not in read:
                        print("ERROR: missing '*/'")
                        exit()
                    if read[i] == "*" and read[i+1] == "/":
                        sign = 0
                        i += 2
                    else:
                        continue

                if read[i] == '#':#读到是注释，那就读下一行
                    break
                elif read[i] == '/' and read[i+1] == '*':
                    sign = 10
                elif read[i] == ' ':#读到空格
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '\t':#读到制表符
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '\n':#读到换行
                    """
                    if sign == 1:
                        continue
                    else:
                        #fp_write.write(' ')
                        #sign = 1
                    """
                    continue
                elif read[i] == '"' or read[i] == "'":#读到双引号和单引号处理方法一致
                    temp = read[i]
                    fp_write.write(read[i])
                    while 1:
                        i += 1
                        fp_write.write(read[i])
                        if i >= length:
                            print("ERROR: missing '"' or "'" ")
                            exit()
                        if read[i] == temp and i < length:
                            break

                else:
                    sign = 3
                    fp_write.write(read[i])
    except Exception as e:
        print(e)
        print(file_name, ': This FileName Not Found!')

def save(string):
    if string in keywords.keys():
        if(len(keylist) >= 1 ):  # 防止数组越界
            if keylist[-1] in string:  # save的字符串可能重复，如':'  ':='
                signlist[-1] = keywords[string]#直接覆盖最后一个元素
                keylist[-1] = string
            else:
                signlist.append(keywords[string])
                keylist.append(string)
            if string not in signdict.keys():
                signdict[string] = keywords[string]
        else:  # keylist为空，即第一个循环
            signlist.append(keywords[string])
            keylist.append(string)
            if string not in signdict.keys():
                signdict[string] = keywords[string]
    else:
        save_var(string)
def save_var(string):
    if string not in signdict.keys():
        if len(string.strip()) < 1:
            pass
        else:
            if is_signal(string) == 1:  # 标识符
                signdict[string] = 36
            elif is_integer(string) == 1:  # 整数
                signdict[string] = 37
            elif is_char(string) == 1:  # 字符常数
                signdict[string] = 38
            else:  # 错误信息
                signdict[string] = 501
            signlist.append(signdict[string])
            keylist.append(string)
    else:  # 重复出现的
        signlist.append(signdict[string])
        keylist.append(string)
        pass
def save_error(string):
    if string not in signdict.keys():
        signdict[string] = 501
def is_signal(s):#判断是否为标识符
    if s[0] == '_' or s[0] in string.ascii_letters:
        for i in s:
            #标识符定义：首字符必须为字母，其他字符必须是字母数字的组合
            if i in string.ascii_letters or i == '_' or i in string.digits:
                pass
            else:
                return 0
        return 1
    else:
        return 0
def is_integer(s):
    try:
        float(s)
        if s not in signdict.keys():
            return 1
    except ValueError:
        return 0
def is_char(s):
    if s[0] == '\'' and s[-1] == '\'':
        return 1
    elif s[0] == '\"' and s[-1] == '\"':
        return 1
    else:
        return 0

def recognition(filename):
    try:
        fp_read = open(filename, 'r')
        string = ""
        sign = 0
        while True:
            read = fp_read.read(1)
            if not read:
                break

            if read == ' ':#空格换词
                if len(string.strip()) < 1:
                    sign = 0
                    pass
                else:
                    if sign == 1:#如果是一个"" () [] {}
                        string += read
                    else:
                        save(string)
                        string = ""
                        sign = 0
            elif read == '(':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('(')
            elif read == ')':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(')')
            elif read == '[':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('[')
            elif read == ']':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(']')
            elif read == '{':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('{')
            elif read == '}':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('}')
            elif read == '<':
                save(string)
                string = ""
                save('<')
                sign = 54  # <=种别码为54
            elif read == '>':  # 这里要判断是否是单词<>
                if sign == 54:
                    save(string)
                    string = ""
                    save("<>")
                    sign = 0
                else:
                    save(string)
                    string = ""
                    #save('>')
                    sign = 58  # <=种别码为58
            elif read == ',':
                save(string)
                string = ""
                save(',')

            elif read == ':':
                if sign >= 1:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(':')
                    sign = 51  # :=种别码为51
            elif read == '+':
                save(string)
                string = ""
                save(read)
            elif read == '*':
                save(string)
                string = ""
                save(read)
            elif read == '.':
                save(string)
                string = ""
                save(read)
            elif read == '=':  # 注意要判断是否是两个char连起来的单词
                if sign == 51:
                    string = ""
                    save(":=")
                    sign = 0
                elif sign == 54:
                    string = ""
                    save("<=")
                    sign = 0
                elif sign == 58:
                    string = ""
                    save(">=")
                    sign = 0
                else:
                    save(string)
                    string = ""
                    save('=')
            elif read == ';':

                save(string)
                string = ""
                save(';')
            elif read == '\n': #换行不读取
                save(string)
                string = ""
                continue
            else:
                string += read

    except Exception as e:
        print(e)

def main():
    print("邓远亭 16计科一班 201530821046\n")
    print("Please Input FileName\n")
    filename = input("FileName: ")
    #filename = "TEST3"
    pretreatment(filename)
    #recognition(filename)
    recognition('file.tmp')#返回signlist和keylist

    for i in range(len(signlist)):
        if (i+1) % 5 == 0:
            print("(", signlist[i], ",", keylist[i], ")")
        else:
            print("(", signlist[i], ",", keylist[i], ")", end=' ')

    print("\n---------------------------------------------------------------")

    #把上面的结果转化为实验要求的输出，利用新的数组resultlist
    resultlist = []#resultlist测试用
    resultdict = {}
    j = 1
    for i in range(len(signlist)):
        if signlist[i] == 36 or signlist[i] == 37 or signlist[i] == 38:
            if keylist[i] not in resultdict:
                resultdict[keylist[i]] = j
                j += 1
            resultlist.append(keylist[i])
        else:
            resultdict[keylist[i]] = '-'
            resultlist.append('-')


    for i in range(len(signlist)):
        if (i+1) % 5 == 0:
            print("(", signlist[i], ",", resultdict[keylist[i]], ")")
        else:
            print("(", signlist[i], ",", resultdict[keylist[i]], ")", end=' ')
if __name__ == '__main__':
    main()