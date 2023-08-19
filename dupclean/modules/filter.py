#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2022 by ZHANG ZHIJIE.
# All rights reserved.

# Last Modified Time: 2023/8/14 16:44
# Author: ZHANG ZHIJIE
# Email: norvyn@norvyn.com
# File Name: fileter.py
# Tools: PyCharm

"""
---Short description of this Python module---

"""
import os

from .datatype import *
from .listduplicate import ListDuplicate
from os import path
import threading


class Filter(object):
    def __init__(self, files: list[File] = None):
        self.files = files

        self.filedict = self._dup_dataclass_to_dict()

    def _dup_dataclass_to_dict(self) -> dict:
        """
        Before:

        [
            File(checksum='md5 or sha512',
            locations=[
                Location(timestamp=1692000990, mode=hold, abs_path='/path/to/file1'),
                Location(timestamp=1692001004, mode=hold, abs_path='/path/to/file2')
            ]
        ]

        After:
        [{'checksum':
            '4e58964ad5ebfdbf50a679861490ebb1',
            'duplicate': True, '
            count': 4,
            'locations': {
                '/path/to/file1': {
                    'timemap': 1692000990,
                    'abs_path': '/home/scripts/40-Python/DuplicateCleaner-0.0.1/dupclean/test/mongodb.bak',
                    'mode': False
                    },
                '/path/to/file2': {
                    'timemap': 1692001004,
                    'abs_path': '/home/scripts/40-Python/DuplicateCleaner-0.0.1/dupclean/test/mongodb.py 2',
                    'mode': False
                    }
                }
            }
        ]

        :return:
        """
        dup_dataclass = self.files
        filedict = {}
        for file in dup_dataclass:
            # file_dict = {'checksum': file.checksum, 'duplicate': file.duplicate, 'count': file.count, 'locations': []}
            file_dict = {'checksum': file.checksum, 'duplicate': file.duplicate, 'count': file.count, 'locations': {}}
            locations = file.locations
            for loc in locations:
                file_dict['locations'].update(
                    {loc.abs_path: {'timestamp': loc.timestamp, 'abs_path': loc.abs_path, 'mode': loc.mode}})
                # file_dict['locations'].append({'timemap': loc.timestamp, 'abs_path': loc.abs_path, 'mode': loc.mode})

            # data.append(file_dict)

            filedict.update({file.checksum: file_dict})

        return filedict

    def mark_by_basename(self, keyword: str = None, suffix: str = None, mode: Mode = 'hold'):

        for checksum, loc_info in self.filedict.items():
            for loc in loc_info['locations'].keys():
                filename = path.basename(loc)
                if keyword and keyword in filename:
                    self.filedict[checksum]['locations'][loc]['mode'] = mode
                    print(keyword)
                if suffix and filename.endswith(suffix):
                    self.filedict[checksum]['locations'][loc]['mode'] = mode

        return self.filedict

    def mark_by_dirname(self, keyword: str = None, mode: Mode = 'hold'):
        """
        Marking file as 'hold' or 'burn' depends on if the file's 'dirname' contains 'keyword' or not.
        :param keyword:
        :param mode: Setting 'hold' to keep the file while 'burn' to delete it.
        :return: Class attribute, self.filedict.
        """
        for checksum, loc_info in self.filedict.items():
            for loc in loc_info['locations'].keys():
                dirname = path.dirname(loc)

                if keyword and keyword in dirname:
                    self.filedict[checksum]['locations'][loc]['mode'] = mode

        return self.filedict

    def hold_copies_by_st_time(self, count: int = 1, time_priority: Time_Priority = 'latest'):
        # each loop (checksum) stands for one group of duplicate files
        for checksum, loc_info in self.filedict.items():
            oldest_time = latest_time = list(self.filedict[checksum]['locations'].values())[0]['timestamp']
            no_hold = 0
            # counting the number of files to hold
            for loc, loc_detail in loc_info['locations'].items():
                if loc_detail['mode'] == 'hold':
                    no_hold += 1

                if no_hold >= count:
                    continue

                st_time = loc_detail['timestamp']

                if st_time >= latest_time:
                    latest_time = st_time

                if st_time <= oldest_time:
                    oldest_time = st_time

            standard_time = oldest_time if time_priority == 'oldest' else latest_time

            # the files to hold already more than the value of 'count', jump out of this loop, and begin the next one.
            if no_hold >= count:
                continue

            for loc, loc_detail in loc_info['locations'].items():
                # if no_hold >= count:
                # continue
                # Causing the locations those have the same 'st_atime',
                # 'st_ctime' and 'st_mtime' all been marked to 'hold'
                # If the number of 'hold' already large than count,
                # the above codes will let the loop jump to next one.
                # If not, the codes below mark the first location to 'hold'
                # and jump out of the loop to the next one (file)

                if loc_detail['timestamp'] == standard_time:
                    self.filedict[checksum]['locations'][loc]['mode'] = 'hold'
                    break  # break to next file; continue only jump to the next location of the file group

        return self.filedict

    def print_result(self):
        for checksum, locations in self.filedict.items():
            print('checksum: ', checksum)
            for loc in locations['locations'].values():
                mode = loc['mode']
                timestamp = loc['timestamp'] if mode == 'hold' else f"\033[0;31m{loc['timestamp']}\033[0m"
                abs_path = loc['abs_path'] if mode == 'hold' else f"\033[0;31m{loc['abs_path']}\033[0m"
                print('\t', f"{mode:5s}", f'{timestamp}', f"'{abs_path}'")

    def burn_paths(self, move_to_dir: str = None, prompt: bool = True):
        paths_to_burn = []
        for checksum, locations in self.filedict.items():
            for loc in locations['locations'].values():
                mode = loc['mode']
                abs_path = loc['abs_path']
                paths_to_burn.append(abs_path) if mode == 'burn' else ''

        def _burn_path(path_to_burn: str):
            RM = 'rm -ri' if prompt else 'rm -rf'
            cmd = f"""{RM} '{path_to_burn}'""" if not move_to_dir else f"""mv '{path_to_burn}' {move_to_dir}"""
            os.system(cmd)

        threads = [threading.Thread(target=_burn_path, args=(p,)) for p in paths_to_burn]

        [t.start() for t in threads]
        [t.join() for t in threads]


if __name__ == '__main__':
    file_opt = ListDuplicate('../test', hash_algo='sha512', st_time='st_atime')
    fileset = file_opt.list_duplicate()

    flt = Filter(files=fileset)
    flt.mark_by_basename(suffix='.bak', mode='burn')
    flt.mark_by_basename(suffix=' 2', mode='burn')
    flt.mark_by_basename(keyword='mongodb', mode='burn')
    flt.mark_by_basename(keyword='.py', mode='burn')
    # flt.mark_by_basename(suffix='.py', mode='hold')
    flt.hold_copies_by_st_time(time_priority='oldest')

    flt.print_result()

