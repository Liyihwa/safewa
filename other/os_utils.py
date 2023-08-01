#!e:/Enviorment/Python/py3.8/python.exe
# -*- coding: utf-8 -*-
'''
对于文件名的拼接,最好用 os.path.join(path,name),不要自己手动拼接
'''

import os
import re


def isfile(path):
    return os.path.isfile(path)


def isdir(path):
    return os.path.isdir(path)


def exist(path):
    return os.path.exists(path)


def mkdir(path, cover=False):
    if isdir(path=path):
        if cover:
            os.removedirs(path)
        else:
            raise RuntimeError("目录" + path + "已存在")
    return os.mkdir(path=path)


def touch(path, cover=False):
    if isfile(path=path):
        if cover:
            os.remove(path)
        else:
            raise RuntimeError("文件" + path + "已存在")
    elif isdir(path):
        raise RuntimeError(path + "是一个目录")
    file = open(path, 'w')
    file.close()


def rm(path, rm_all=False):
    if isfile(path):
        os.remove(path)
    elif isdir(path):
        if rm_all:
            files = ls(path, dfs=True,only_file=False)
            for it in files:
                if isfile(it):
                    os.remove(it)
            for it in files:
                if isdir(it):
                    os.removedirs(it)
        else:
            files = ls(path, dfs=False, only_file=True)
            for it in files:
                os.remove(it)
    else:
        raise RuntimeError(path + "不存在")


'''
    递归的列出 path下的所有子项
    需要保证path一定是目录
'''


def __dfs(path, _list, only_file, ignore):
    for it in os.listdir(path):
        _path = os.path.join(path, it)
        flag = False
        for ig in ignore:
            if re.search(ig, path):
                flag = True
        if flag:
            continue
        if only_file:
            if isfile(_path):
                _list.append(_path)
            else:
                try:
                    __dfs(_path, _list, only_file,ignore)
                except PermissionError:
                    pass
        else:
            _list.append(_path)
            if isdir(_path):
                try:
                    __dfs(_path, _list, only_file, ignore)
                except PermissionError:
                    pass


def __in_dir(path, _list, only_file, ignore):
    for it in os.listdir(path):
        _path = os.path.join(path, it)
        flag = False
        for ig in ignore:
            if re.match(ig, path):
                flag = True
        if flag:
            continue
        if only_file:
            if isfile(_path):
                _list.append(_path)
        else:
            _list.append(_path)


def pwd():
    return os.getcwd()


'''
    ls 会以dfs形式列出目录下的文件/目录
    @:param dfs: 是否递归访问
    @:param only_file: 是否仅记录文件,不记录目录
    @:param only_access: 是否仅记录有权限的文件/目录 
'''


def ls(path, dfs=False, only_file=False, ignore=[r"\$+"]):
    if not isdir(path):
        raise RuntimeError(path + "不是目录")
    _list = []
    if not os.access(path, os.R_OK):
        return _list
    if dfs:
        __dfs(path, _list, only_file, ignore)
    else:
        __in_dir(path, _list, only_file, ignore)
    return _list


def append(path, _str, cover=False, create=True, _encoding="utf8"):
    if not exist(path):
        if create:
            touch(path)
            with open(path, 'a', encoding=_encoding) as _f:
                _f.write(_str)
        else:
            raise RuntimeError("文件" + path + "不存在,无法追加")
    elif isdir(path):
        raise RuntimeError(path + "是一个目录,无法追加")
    if isfile(path):
        if cover:
            with open(path, 'a', encoding=_encoding) as _f:
                _f.write(_str)
        else:
            raise RuntimeError("文件" + path + "已存在")


def write(path, _str, cover=False, create=True, _encoding="utf8"):
    if not exist(path):
        if create:
            touch(path)
            with open(path, 'w', encoding=_encoding) as _f:
                _f.write(_str)
        else:
            raise RuntimeError("文件" + path + "不存在,无法写入")
    elif isdir(path):
        raise RuntimeError(path + "是一个目录,无法写入")
    if isfile(path):
        if cover:
            with open(path, 'w', encoding=_encoding) as _f:
                _f.write(_str)
        else:
            raise RuntimeError("文件" + path + "已存在")


if __name__ == '__main__':
    print(ls("E:\\"))
