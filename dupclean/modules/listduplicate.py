#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2022 by ZHANG ZHIJIE.
# All rights reserved.

# Created Time: 2023-08-12 09:47
# Author: ZHANG ZHIJIE
# Email: norvyn@norvyn.com
# Git: @n0rvyn
# File Name: list_duplicate.py
# Tools: PyCharm

"""
---Listing files to data structure---

"""
from subprocess import getstatusoutput
from os import environ, path, stat
from .datatype import *
# todo typing --> Optional


class ListDuplicate(object):
    def __init__(self,
                 folder: str = '.',
                 recursively: bool = False,
                 hash_algo: HashAlgorithm = 'md5',
                 st_time: ST_Time = 'st_mtime'):
        if folder.startswith('~'):
            folder = path.abspath(path.join(environ['HOME'], folder.replace('~/', '', 1)))
        else:
            folder = path.abspath(path.join(environ['PWD'], folder))

        self.folder = folder
        self.recursively = recursively
        self.hash_algo = hash_algo
        self.st_time = st_time

    def list_files(self) -> list:
        """
        Listing files and those checksums as a dict, like: {'checksums': ['file location1', 'file location2']}
        """
        fileset = []

        files_by_checksum = {}

        # when 'recursively' set to 'True', find files under the directory recursively, just like 'scp -r'
        maxdepth = '-maxdepth 1' if not self.recursively else ''

        if self.hash_algo == 'sha512':
            expression = '-exec sha512sum {} \;'
        else:
            expression = '-exec md5sum {} \;'

        cmd = f'find {self.folder} {maxdepth} -type f {expression}'
        status, output = getstatusoutput(cmd)
        """
        file_hash1 file_path1
        file_hash2 file_path2
        """
        for f in output.split('\n'):
            _delimiter = '^@^'
            # replace the first blank to '^@^', then split the string with '^@^'
            # in case if 'file_path' contains blank itself.
            f = f.replace(' ', _delimiter, 1)
            _list = f.split(_delimiter)

            _checksum = _list[0]
            try:
                _abs_path = _list[1].strip()
            except IndexError:
                break
            # checking the 'st_time' of file path
            _st_time = stat(_abs_path)[ST_Index[self.st_time]]

            _location = Location(timestamp=_st_time, abs_path=_abs_path, mode='hold')
            try:
                files_by_checksum[_checksum].append(_location)
            except KeyError:
                files_by_checksum.update({_checksum: [_location]})

        for checksum, locations in files_by_checksum.items():
            count = len(locations)
            duplicate = True if count > 1 else False
            file = File(checksum=checksum, locations=locations, duplicate=duplicate, count=count)
            fileset.append(file)

        return fileset

    def list_duplicate(self) -> list:
        fileset = self.list_files()
        duplicate = []
        for file in fileset:
            if file.duplicate:
                duplicate.append(file)

        return duplicate

    def print_duplicate(self) -> None:
        duplicate = self.list_duplicate()
        for file in duplicate:
            print('Checksum: ', file.checksum)
            for loc in file.locations:
                print('\t', loc)


if __name__ == '__main__':
    fo = ListDuplicate('../test', hash_algo='sha512')

    keep_suffix_list = ['.sh', '.conf']
    del_suffix_list = ['.sh2']

    fo.print_duplicate()




