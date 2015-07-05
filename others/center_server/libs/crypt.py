#!/usr/bin/env python
#coding:utf-8
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class crypt_aes():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC

    #加密函数，如果text不足16位就用空格补足为16位，
    #如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt_aes(self,text):
        cryptor = AES.new(self.key,self.mode)
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt_aes(self,text):
        cryptor = AES.new(self.key,self.mode)
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

# pc = crypt_aes('keyskeyskeyskeys') #初始化密钥
# import sys
# e = pc.encrypt_aes(sys.argv[1]) #加密
# d = pc.decrypt_aes(e) #解密
# print "加密:",e
# print "解密:",d


def encrypt(key,text):
    l1 = []
    l2 = []
    a = 0
    if len(key) > len(text):
        length = len(text)
    else:
        length = len(key)
    for i in key:
        a += ord(i)
    num = a % len(key)
    if num == 0:
        num = 7
    for i in text:
        l1.append(ord(i) + num)
    for i in range(len(l1)/2):
        l1[i],l1[-(i+1)] = l1[-(i+1)],l1[i]
    for i in range(length):
        l1[i] += num
    for i in l1:
        l2.append(chr(i))
    t = ''.join(l2)
    return t

def decrypt(key,text):
    l1 = []
    l2 = []
    a = 0
    if len(key) > len(text):
        length = len(text)
    else:
        length = len(key)
    for i in key:
        a += ord(i)
    num = a % len(key)
    if num == 0:
        num = 7
    for i in text:
        l1.append(ord(i))
    for i in range(length):
        l1[i] -= num
    for i in range(len(l1)/2):
        l1[i],l1[-(i+1)] = l1[-(i+1)],l1[i]
    for i in range(len(text)):
        l1[i] -= num
    for i in l1:
        l2.append(chr(i))
    t = ''.join(l2)
    return t

def strong_encrypt(key,text):
    data = base64.b64encode(text)
    data = encrypt(key,data)
    return data

def strong_decrypt(key,text):
    data = decrypt(key,text)
    data = base64.b64decode(data)
    return data
