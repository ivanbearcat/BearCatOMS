#!/usr/bin/env python
#coding:utf-8
import base64

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
