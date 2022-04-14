Matrix = [  # 列混淆
    ['0x02', '0x03', '0x01', '0x01'],
    ['0x01', '0x02', '0x03', '0x01'],
    ['0x01', '0x01', '0x02', '0x03'],
    ['0x03', '0x01', '0x01', '0x02']
]

plaintext = [[], [], [], []]  # 存放明文
plaintext1 = [[], [], [], []]  # 最后输出的密文

def MixColumns(pt):  # 列混淆
    for i in range(4):
        for j in range(4):
            plaintext1[i].append(MatrixMulti(Matrix[j], pt[i]))
    print(plaintext1)

def MatrixMulti(s1, s2):  # 列混淆中的矩阵乘法
    result = []
    s3 = []
    for i in range(4):
        s3.append(hextobin(s2[i]))  # s3保存原始矩阵一行的四个二进制值
    for i in range(4):
        result.append(MultiProcess(int(s1[i], 16), s3[i]))
    for i in range(3):
        result[0] = xor_8(result[0], result[i+1])
    return bintohex(result[0])

def bintohex(word):  # 把二进制转换十六进制
    word = hex(int(word, 2))
    if len(word) == 4:
        return word
    elif len(word) < 4:
        return word.replace('x', 'x0')

def hextobin(word):  # 把十六进制转换成二进制
    word = bin(int(word, 16))[2:]  # 去除掉最前面的0b
    for i in range(0, 8-len(word)):  # 补全八位
        word = '0'+word
    return word

def MultiProcess(a, b):  # 列混淆中的乘法运算的具体过程
    if a == 1:
        return b
    elif a == 2:
        if b[0] == '0':
            b = b[1:] + '0'
        else:
            b = b[1:] + '0'
            b = xor_8(b, '00011011')
        return b
    elif a == 3:
        tmp_b = b
        if b[0] == '0':
            b = b[1:] + '0'
        else:
            b = b[1:] + '0'
            b = xor_8(b, '00011011')
        return xor_8(b, tmp_b)

    elif a == 9:
        tmp_b = b
        return xor_8(tmp_b, MultiProcess(2, MultiProcess(2, MultiProcess(2, b))))
    elif a == 11:
        tmp_b = b
        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, b)))
    elif a == 13:
        tmp_b = b
        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))
    elif a == 14:
        return xor_8(MultiProcess(2, b), xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))

def xor_8(begin, end):  # 8位异或
    xor_8_tmp = ""
    for i in range(8):
        xor_8_tmp += str(int(begin[i]) ^ int(end[i]))
    return xor_8_tmp


# pt = [['7c','6b','01','d7'],['f2','30','fe','63'],['2b','76','7b','c5'],['ab','77','bf','67']]
pt = [['7c','f2','2b','ab'],['6b','30','76','77'],['01','fe','7b','bf'],['d7','63','c5','67']]
MixColumns(pt)