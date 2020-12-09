# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
import random
import time
import hashlib
import re
from jieba import analyse


def md5(data):
    md5data = hashlib.md5(str(data).encode(encoding='UTF-8')).hexdigest()
    return md5data


# 生成一个永不重复的随机数
def rand_number():
    t = time.time()
    mt = int(round(t * 10000))
    rn = int(random.random() * 10000)
    n = int(str(mt) + str(rn))
    return n


class ShortenURL:
    _alphabet = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ'
    _base = len(_alphabet)

    def encode(self, number):
        string = ''
        while number > 0:
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number


def get_id(data):
    if '.' not in data:
        return data
    tmp = data.split('.')
    return tmp[0]


# 获取关键词
def get_keywords(text):
    textrank = analyse.textrank
    keywords = textrank(text)
    k = ""
    for item in keywords:
        k += item + ','
    return k[:-1]


def get_description(text):
    content = re.sub(r"</?(.+?)>", "", text)
    content = re.sub(r"&/?(.+?);", "", content)
    d = re.sub(r"\s+", "", content)
    return d[:160]
