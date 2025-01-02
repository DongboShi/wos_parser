#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import os
import chardet


def detect_code(file_path):
    with open(file_path, 'rb') as file:
        data = file.read(200000)
        dicts = chardet.detect(data)
    return dicts["encoding"]


# 文件所在目录
if __name__ == '__main__':
    path = input("输入log文件路径： ")
    print(detect_code(path))
