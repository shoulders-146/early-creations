# -*- coding: utf-8 -*-

import re
import binascii

class Aes:
    s_box = {  # 字节替换s盒
        '0x00': '0x63', '0x01': '0x7c', '0x02': '0x77', '0x03': '0x7b', '0x04': '0xf2', '0x05': '0x6b', '0x06': '0x6f', '0x07': '0xc5', '0x08': '0x30', '0x09': '0x01', '0x0a': '0x67', '0x0b': '0x2b', '0x0c': '0xfe', '0x0d': '0xd7', '0x0e': '0xab', '0x0f': '0x76',
        '0x10': '0xca', '0x11': '0x82', '0x12': '0xc9', '0x13': '0x7d', '0x14': '0xfa', '0x15': '0x59', '0x16': '0x47', '0x17': '0xf0', '0x18': '0xad', '0x19': '0xd4', '0x1a': '0xa2', '0x1b': '0xaf', '0x1c': '0x9c', '0x1d': '0xa4', '0x1e': '0x72', '0x1f': '0xc0',
        '0x20': '0xb7', '0x21': '0xfd', '0x22': '0x93', '0x23': '0x26', '0x24': '0x36', '0x25': '0x3f', '0x26': '0xf7', '0x27': '0xcc', '0x28': '0x34', '0x29': '0xa5', '0x2a': '0xe5', '0x2b': '0xf1', '0x2c': '0x71', '0x2d': '0xd8', '0x2e': '0x31', '0x2f': '0x15',
        '0x30': '0x04', '0x31': '0xc7', '0x32': '0x23', '0x33': '0xc3', '0x34': '0x18', '0x35': '0x96', '0x36': '0x05', '0x37': '0x9a', '0x38': '0x07', '0x39': '0x12', '0x3a': '0x80', '0x3b': '0xe2', '0x3c': '0xeb', '0x3d': '0x27', '0x3e': '0xb2', '0x3f': '0x75',
        '0x40': '0x09', '0x41': '0x83', '0x42': '0x2c', '0x43': '0x1a', '0x44': '0x1b', '0x45': '0x6e', '0x46': '0x5a', '0x47': '0xa0', '0x48': '0x52', '0x49': '0x3b', '0x4a': '0xd6', '0x4b': '0xb3', '0x4c': '0x29', '0x4d': '0xe3', '0x4e': '0x2f', '0x4f': '0x84',
        '0x50': '0x53', '0x51': '0xd1', '0x52': '0x00', '0x53': '0xed', '0x54': '0x20', '0x55': '0xfc', '0x56': '0xb1', '0x57': '0x5b', '0x58': '0x6a', '0x59': '0xcb', '0x5a': '0xbe', '0x5b': '0x39', '0x5c': '0x4a', '0x5d': '0x4c', '0x5e': '0x58', '0x5f': '0xcf',
        '0x60': '0xd0', '0x61': '0xef', '0x62': '0xaa', '0x63': '0xfb', '0x64': '0x43', '0x65': '0x4d', '0x66': '0x33', '0x67': '0x85', '0x68': '0x45', '0x69': '0xf9', '0x6a': '0x02', '0x6b': '0x7f', '0x6c': '0x50', '0x6d': '0x3c', '0x6e': '0x9f', '0x6f': '0xa8',
        '0x70': '0x51', '0x71': '0xa3', '0x72': '0x40', '0x73': '0x8f', '0x74': '0x92', '0x75': '0x9d', '0x76': '0x38', '0x77': '0xf5', '0x78': '0xbc', '0x79': '0xb6', '0x7a': '0xda', '0x7b': '0x21', '0x7c': '0x10', '0x7d': '0xff', '0x7e': '0xf3', '0x7f': '0xd2',
        '0x80': '0xcd', '0x81': '0x0c', '0x82': '0x13', '0x83': '0xec', '0x84': '0x5f', '0x85': '0x97', '0x86': '0x44', '0x87': '0x17', '0x88': '0xc4', '0x89': '0xa7', '0x8a': '0x7e', '0x8b': '0x3d', '0x8c': '0x64', '0x8d': '0x5d', '0x8e': '0x19', '0x8f': '0x73',
        '0x90': '0x60', '0x91': '0x81', '0x92': '0x4f', '0x93': '0xdc', '0x94': '0x22', '0x95': '0x2a', '0x96': '0x90', '0x97': '0x88', '0x98': '0x46', '0x99': '0xee', '0x9a': '0xb8', '0x9b': '0x14', '0x9c': '0xde', '0x9d': '0x5e', '0x9e': '0x0b', '0x9f': '0xdb',
        '0xa0': '0xe0', '0xa1': '0x32', '0xa2': '0x3a', '0xa3': '0x0a', '0xa4': '0x49', '0xa5': '0x06', '0xa6': '0x24', '0xa7': '0x5c', '0xa8': '0xc2', '0xa9': '0xd3', '0xaa': '0xac', '0xab': '0x62', '0xac': '0x91', '0xad': '0x95', '0xae': '0xe4', '0xaf': '0x79',
        '0xb0': '0xe7', '0xb1': '0xc8', '0xb2': '0x37', '0xb3': '0x6d', '0xb4': '0x8d', '0xb5': '0xd5', '0xb6': '0x4e', '0xb7': '0xa9', '0xb8': '0x6c', '0xb9': '0x56', '0xba': '0xf4', '0xbb': '0xea', '0xbc': '0x65', '0xbd': '0x7a', '0xbe': '0xae', '0xbf': '0x08',
        '0xc0': '0xba', '0xc1': '0x78', '0xc2': '0x25', '0xc3': '0x2e', '0xc4': '0x1c', '0xc5': '0xa6', '0xc6': '0xb4', '0xc7': '0xc6', '0xc8': '0xe8', '0xc9': '0xdd', '0xca': '0x74', '0xcb': '0x1f', '0xcc': '0x4b', '0xcd': '0xbd', '0xce': '0x8b', '0xcf': '0x8a',
        '0xd0': '0x70', '0xd1': '0x3e', '0xd2': '0xb5', '0xd3': '0x66', '0xd4': '0x48', '0xd5': '0x03', '0xd6': '0xf6', '0xd7': '0x0e', '0xd8': '0x61', '0xd9': '0x35', '0xda': '0x57', '0xdb': '0xb9', '0xdc': '0x86', '0xdd': '0xc1', '0xde': '0x1d', '0xdf': '0x9e',
        '0xe0': '0xe1', '0xe1': '0xf8', '0xe2': '0x98', '0xe3': '0x11', '0xe4': '0x69', '0xe5': '0xd9', '0xe6': '0x8e', '0xe7': '0x94', '0xe8': '0x9b', '0xe9': '0x1e', '0xea': '0x87', '0xeb': '0xe9', '0xec': '0xce', '0xed': '0x55', '0xee': '0x28', '0xef': '0xdf',
        '0xf0': '0x8c', '0xf1': '0xa1', '0xf2': '0x89', '0xf3': '0x0d', '0xf4': '0xbf', '0xf5': '0xe6', '0xf6': '0x42', '0xf7': '0x68', '0xf8': '0x41', '0xf9': '0x99', '0xfa': '0x2d', '0xfb': '0x0f', '0xfc': '0xb0', '0xfd': '0x54', '0xfe': '0xbb', '0xff': '0x16'
    }
    ns_box = {  # 逆字节替换s盒
    }

    Rcon = {  # Rcon生成密钥的表
        1: ['0x01', '0x00', '0x00', '0x00'],
        2: ['0x02', '0x00', '0x00', '0x00'],
        3: ['0x04', '0x00', '0x00', '0x00'],
        4: ['0x08', '0x00', '0x00', '0x00'],
        5: ['0x10', '0x00', '0x00', '0x00'],
        6: ['0x20', '0x00', '0x00', '0x00'],
        7: ['0x40', '0x00', '0x00', '0x00'],
        8: ['0x80', '0x00', '0x00', '0x00'],
        9: ['0x1B', '0x00', '0x00', '0x00'],
        10: ['0x36', '0x00', '0x00', '0x00']
    }
    Matrix = [  # 列混淆
        ['0x02', '0x03', '0x01', '0x01'],
        ['0x01', '0x02', '0x03', '0x01'],
        ['0x01', '0x01', '0x02', '0x03'],
        ['0x03', '0x01', '0x01', '0x02']
    ]
    ReMatrix = [  # 逆列混淆
        ['0x0e', '0x0b', '0x0d', '0x09'],
        ['0x09', '0x0e', '0x0b', '0x0d'],
        ['0x0d', '0x09', '0x0e', '0x0b'],
        ['0x0b', '0x0d', '0x09', '0x0e']
    ]
    plaintext = [[], [], [], []]  # 存放明文
    plaintext1 = [[], [], [], []]  # 最后输出的密文
    subkey = [[], [], [], []]  # 存放密钥

    def __init__(self, key):  # 构造函数，同时生成密钥
        for i in range(4):
            for j in range(0, 8, 2):
                self.subkey[i].append("0x" + key[i * 8 + j:i * 8 + j + 2])  # 将密钥变成二维矩阵
        # print(self.subkey)
        for i in range(4, 44):  # 生成密钥
            if i % 4 != 0:  # 如果不是4的倍数，那么直接异或
                tmp = xor_32(self.subkey[i - 1], self.subkey[i - 4])
                self.subkey.append(tmp)
            else:  # 4的倍数的时候执行
                tmp1 = self.subkey[i - 1][1:]
                tmp1.append(self.subkey[i - 1][0])
                # print(tmp1)
                for m in range(4):
                    tmp1[m] = self.s_box[tmp1[m]]
                # tmp1 = self.s_box['cf']  # 字节代替
                tmp1 = xor_32(tmp1, self.Rcon[i / 4])  # 和Rcon异或
                self.subkey.append(xor_32(tmp1, self.subkey[i - 4]))
        # print(self.subkey)

    def AddRoundKey(self, round):  # 轮密钥加
        for i in range(4):
            self.plaintext[i] = xor_32(self.plaintext[i], self.subkey[round * 4 + i])
        # print(self.plaintext)

    def PlainSubBytes(self):  # 字节代替
        for i in range(4):
            for j in range(4):
                self.plaintext[i][j] = self.s_box[self.plaintext[i][j]]
        # print(self.plaintext)

    def RePlainSubBytes(self):  # 逆字节代替
        for i in range(4):
            for j in range(4):
                self.plaintext[i][j] = self.ns_box[self.plaintext[i][j]]

    def ShiftRows(self):  # 行移位
        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]
        self.plaintext[0][1] = p2
        self.plaintext[1][1] = p3
        self.plaintext[2][1] = p4
        self.plaintext[3][1] = p1
        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]
        self.plaintext[0][2] = p3
        self.plaintext[1][2] = p4
        self.plaintext[2][2] = p1
        self.plaintext[3][2] = p2
        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]
        self.plaintext[0][3] = p4
        self.plaintext[1][3] = p1
        self.plaintext[2][3] = p2
        self.plaintext[3][3] = p3
        # print(self.plaintext)

    def ReShiftRows(self):  # 逆行移位
        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]
        self.plaintext[3][1] = p3
        self.plaintext[2][1] = p2
        self.plaintext[0][1] = p4
        self.plaintext[1][1] = p1
        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]
        self.plaintext[0][2] = p3
        self.plaintext[1][2] = p4
        self.plaintext[2][2] = p1
        self.plaintext[3][2] = p2
        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]
        self.plaintext[0][3] = p2
        self.plaintext[1][3] = p3
        self.plaintext[2][3] = p4
        self.plaintext[3][3] = p1

    def MixColumns(self):  # 列混淆
        for i in range(4):
            for j in range(4):
                self.plaintext1[i].append(MatrixMulti(self.Matrix[j], self.plaintext[i]))
        # print(self.plaintext1)

    def ReMixColumns(self):  # 逆列混淆
        for i in range(4):
            for j in range(4):
                self.plaintext1[i].append(MatrixMulti(self.ReMatrix[j], self.plaintext[i]))

    def AESEncryption(self, plaintext):  # AES单组加密函数
        self.plaintext = [[], [], [], []]
        for i in range(4):
            for j in range(0, 8, 2):
                self.plaintext[i].append("0x" + plaintext[i * 8 + j:i * 8 + j + 2])
        self.AddRoundKey(0)
        for i in range(9):
            self.PlainSubBytes()
            self.ShiftRows()
            self.MixColumns()
            self.plaintext = self.plaintext1
            self.plaintext1 = [[], [], [], []]  # 重置
            self.AddRoundKey(i + 1)

        self.PlainSubBytes()  # 最后一轮字节代替
        self.ShiftRows()  # 最后一轮行移位
        self.AddRoundKey(10)  # 最后一轮轮密钥加
        return Matrixtostr(self.plaintext)

    def AESDecryption(self, cipher):  # AES单组解密函数
        self.plaintext = [[], [], [], []]
        for i in range(4):
            for j in range(0, 8, 2):
                self.plaintext[i].append('0x' + cipher[i * 8 + j:i * 8 + j + 2])  # 16进制转成2进制

        self.ns_box = dict(zip(self.s_box.values(), self.s_box.keys()))  # s盒键值互换，变为逆S盒
        # print(self.ns_box)
        self.AddRoundKey(10)
        for i in range(9):
            self.ReShiftRows()
            self.RePlainSubBytes()
            self.AddRoundKey(9-i)
            self.ReMixColumns()
            self.plaintext = self.plaintext1
            self.plaintext1 = [[], [], [], []]
        self.ReShiftRows()
        self.RePlainSubBytes()
        self.AddRoundKey(0)
        return Matrixtostr(self.plaintext)

    def Encryption(self, text):  # 加密函数
        group = PlaintextGroup(TextToByte(text), 32, 1)
        # print(group)
        cipher = ""
        for i in range(len(group)):
            cipher = cipher + self.AESEncryption(group[i])
        return cipher

    def Decryption(self, cipher):  # 解密函数
        group = PlaintextGroup(cipher, 32, 0)
        # print(group)
        text = ''
        for i in range(len(group)):
            text = text + self.AESDecryption(group[i])
        text = ByteToText(text)
        return text


def xor_32(start, end):  # 32位进行异或

    a = []
    for i in range(0, 4):
        xor_tmp = ""
        b = hextobin(start[i])
        c = hextobin(end[i])
        for j in range(8):
            xor_tmp += str(int(b[j], 10) ^ int(c[j], 10))
        a.append(bintohex(xor_tmp))
    return a


def xor_8(begin, end):  # 8位异或
    xor_8_tmp = ""
    for i in range(8):
        xor_8_tmp += str(int(begin[i]) ^ int(end[i]))
    return xor_8_tmp


def hextobin(word):  # 把十六进制转换成二进制
    word = bin(int(word, 16))[2:]  # 去除掉最前面的0b
    for i in range(0, 8-len(word)):  # 补全八位
        word = '0'+word
    return word


def bintohex(word):  # 把二进制转换十六进制
    word = hex(int(word, 2))
    if len(word) == 4:
        return word
    elif len(word) < 4:
        return word.replace('x', 'x0')


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


def Matrixtostr(matrix):  # 矩阵转成字符串
    result = ""
    for i in range(4):
        for j in range(4):
            result += matrix[i][j][2:]
    return result


def PlaintextGroup(plaintext, length, flag):  # 明文分组和填充
    group = re.findall('.{'+str(length)+'}', plaintext)
    group.append(plaintext[len(group)*length:])
    if group[-1] == '' and flag:
        group[-1] = '16161616161616161616161616161616'
    elif len(group[-1]) < length and flag:
        tmp = int((length-len(group[-1])) / 2)
        if tmp < 10:
            for i in range(tmp):
                group[-1] = group[-1] + '0'+str(tmp)
        else:
            for i in range(tmp):
                group[-1] = group[-1] + str(tmp)
    elif not flag:
        del group[-1]
    return group


def TextToByte(words):  # 明文转成十六进制字节流
    text = words.encode('utf-8').hex()
    return text


def ByteToText(encode):  # 十六进制字节流转成明文
    tmp = int(encode[-2:])
    word = ''
    for i in range(len(encode)-tmp*2):
        word = word + encode[i]
    # print(word)
    word = bytes.decode(binascii.a2b_hex(word))
    return word


key = '2b7e151628aed2a6abf7158809cf4f3c'
# plaintext = '68656c6c6f20776f726c640505050505'
# A1 = Aes(key)
# abc = A1.AESEncryption(plaintext)
# print(abc)
# print(A1.AESDecryption(abc))
AESDemo = Aes(key)
plaintext = input("请输入要加密的文字:\n")
a = AESDemo.Encryption(plaintext)
print("密文为：" + a)
print("明文为：" + AESDemo.Decryption(a))

