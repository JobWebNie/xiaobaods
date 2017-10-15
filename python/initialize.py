#!/usr/bin/env python
# -*- coding: gbk -*-

"""
__title__ = ''
__author__ = 'Administrator'
__mtime__ = '2017-10-09'
"""
import os
import configparser


def conftodict(filename, path=""):
    if path == "":
        path = os.path.dirname(__file__)+"/"
    dic = {}
    cp = configparser.ConfigParser()
    cp.read(path+filename)
    s = cp.sections()
    for i in s:
        dic[i] = {}
        for j in cp.options(i):
            dic[i][j] = cp.get(i, j)
    return dic


def storegrouplist(filename):
    '''待转换为SQL'''
    import codecs
    storegroup = {}
    try:
        f = codecs.open(filename, 'r', 'utf-8')
        storegrouptxt = f.readlines()
        for i in range(1, len(storegrouptxt)):  # 第一行为编码行，略去
            storegroup[storegrouptxt[i].split(":")[0]] = storegrouptxt[i].split(":")[1].split("\r\n")[0].split(",")
        f.close()
    except:
        pass
    return storegroup
