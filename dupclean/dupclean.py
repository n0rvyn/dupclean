#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2022 by ZHANG ZHIJIE.
# All rights reserved.

# Created Time: 2023-08-13 08:59
# Author: ZHANG ZHIJIE
# Email: norvyn@norvyn.com
# Git: @n0rvyn
# File Name: dupclean.py
# Tools: PyCharm

"""
---Short description of this Python module---

"""
import os
from os import path
from modules import ListDuplicate
from modules import Filter
from modules import HashAlgorithm
from modules import ST_Time
from modules import Time_Priority
import sys
from getopt import getopt, GetoptError

filename = path.basename(path.abspath(__file__))
folder = '.'
run = False
recursively = False
hash_algo: HashAlgorithm = 'md5'
st_time: ST_Time = 'st_mtime'
prompt = True
count = 0
priority: Time_Priority = 'latest'
backup_to = None

key_to_hold = []
key_to_burn = []
suffix_to_hold = []
suffix_to_burn = []

key_to_path_hold = []
key_to_path_burn = []

USAGE = f"""
Usage: {filename} [action] [options] [filter] [path]

Path:
       -f, --folder                     the working directory

Actions:
       --run                            analyze and delete the files marked as 'burn'
       -h, --help                       display this help message and exit

Options:
       -r, --recursively                recursively analyze entire directories
       -a, --hash-algo HASH_ALGORITHM   hashing algorithm to identifying the file, 'sha512' or 'md5'(default)
       -c, --count COUNT                number of copies to hold even all duplicate met the filter
                                        depends on the value of '--st-time' and '--priority'
       -t, --st-time ST_TIME            st_mtime'(default), 'st_atime', or 'st_ctime'
       -p, --priority PRIORITY          choose 'oldest' or 'latest'(default) st_time to hold the file
       -b, --backup DIRECTORY           moving files to DIRECTORY instead of delete directly
       --force                          deleting files without prompt (default: rm -ri)
      
Filter:
       --key-to-hold      "K1,K2..."    keywords to hold the file, "key1, key2..."
       --key-to-burn      "K1,K2..."    keywords to burn the file
       --suffix-to-hold   "K1,K2..."    suffix to hold the file
       --suffix-to-burn   "K1,K2..."    suffix to burn the file
       --key-to-path-hold "K1,K2..."    keywords to hold the file by file's absolute path
       --key-to-path-burn "K1,K2..."    keywords to burn the file by file's absolute path

\033[0;31mWarning\033[0m: 
       Do NOT leave blank after ',' for specifying more than 2 keywords, 
       because the BLANK will be considered as the first part of the next keyword. 
       
Example:
       {filename} -r -c 1 --key-to-burn 'test,log' --suffix-to-burn '.bak,.log' /path/to/folder
"""
# todo adding method to deleting files those have the same 'mtime', 'atime', 'ctime'.
options = sys.argv[1:]
# folder = sys.argv[-1]  # if command ends with '-b PATH', the 'PATH' will be taken as the working directory by mistake.
# folder = folder if path.isdir(folder) else '.'

if len(sys.argv) == 1:
    print(USAGE)
    sys.exit(0)

# short option has a value --> d:
# long option has a value  --> 'long-args='
try:
    opts, args = getopt(options,
                        'ha:t:c:p:f:rb:',
                        [
                            'run', 'help', 'hash-algorithm=', 'st-time=', 'priority', 'count', 'folder',
                            'recursively', 'force',
                            'key-to-hold=', 'key-to-burn=', 'suffix-to-hold=', 'suffix-to-burn=',
                            'key-to-path-hold=', 'key-to-path-burn=', 'backup='])
except GetoptError as e:
    raise e

for opt, arg in opts:
    if opt == '--run':
        run = True
    elif opt in ['--help', '-h']:
        print(USAGE)
        sys.exit(0)
    elif opt in ['-f', '--folder']:
        folder = arg
        if not path.isdir(folder):
            raise NotADirectoryError
    elif opt in ['-r', '--recursively']:
        recursively = True
    elif opt in ['-a', '--hash-algorithm']:
        if arg not in ['sha512', 'md5']:
            raise TypeError
        hash_algo = arg
    elif opt in ['-t', '--st-time']:
        if arg not in ['st_atime', 'st_mtime', 'st_ctime']:
            raise TypeError
        st_time = arg
    elif opt in ['-c', '--count']:
        try:
            count = int(arg)
        except TypeError as e:
            raise e
    elif opt in ['-p', '--priority']:
        if not arg in ['latest', 'oldest']:
            raise TypeError
        priority = arg
    elif opt in ['--key-to-hold']:
        key_to_hold = arg.split(',')
    elif opt in ['--key-to-burn']:
        key_to_burn = arg.split(',')
    elif opt in ['--suffix-to-hold']:
        suffix_to_hold = arg.split(',')
    elif opt in ['--suffix-to-burn']:
        suffix_to_burn = arg.split(',')
    elif opt in ['--key-to-path-hold']:
        key_to_path_hold = arg.split(',')
    elif opt in ['--key-to-path-burn']:
        key_to_path_burn = arg.split(',')
    elif opt in ['-b', '--backup']:
        backup_to = arg
        if not path.isdir(backup_to):
            raise NotADirectoryError
    elif opt in ['--force']:
        prompt = False

ls_duplicate = ListDuplicate(folder=folder, recursively=recursively, hash_algo=hash_algo, st_time=st_time)
duplicate = ls_duplicate.list_duplicate()
flt = Filter(duplicate)

for key in key_to_burn:
    flt.mark_by_basename(keyword=key, mode='burn')
for suffix in suffix_to_burn:
    flt.mark_by_basename(suffix=suffix, mode='burn')
for path_key in key_to_path_burn:
    flt.mark_by_dirname(keyword=path_key, mode='burn')

for key in key_to_hold:
    flt.mark_by_basename(keyword=key, mode='hold')
for suffix in suffix_to_hold:
    flt.mark_by_basename(suffix=suffix, mode='hold')
for path_key in key_to_path_hold:
    flt.mark_by_dirname(keyword=path_key, mode='hold')

flt.hold_copies_by_st_time(count=count, time_priority=priority) if count > 0 else ''

if flt.filedict:
    print('-' * 40, 'Duplicate Results', '-' * 40)
    flt.print_result()
    print('-' * 40, 'Duplicate Results', '-' * 40)
    print('Need taking action, followed with "--run" parameter.')
    print('You can also move the files to directory followed by "-b" or "--backup" instead of deleting directly.')

flt.burn_paths(move_to_dir=backup_to, prompt=prompt) if run else ''
