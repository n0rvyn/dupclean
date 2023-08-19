from dataclasses import dataclass
from typing import Literal


Mode= Literal[
    'burn', 'hold'
]


# Not necessary^_^
# Just want to try something new.
@dataclass
class Location:
    timestamp: int = -1
    mode: Mode = 'keep'
    abs_path: str = None


@dataclass
class File:
    checksum: str = None
    locations: list[Location] = None
    duplicate: bool = False
    count: int = -1


ST_Time = Literal[
    'st_atime',
    'st_mtime',
    'st_ctime'
]

HashAlgorithm = Literal[
    'sha512', 'md5'
]

Time_Priority = Literal[
    'oldest', 'latest'
]


# the index of 'st_atime', 'st_mtime' and 'st_ctime' in method: os.stat()
ST_Index = {'st_atime': 7,
            'st_mtime': 8,
            'st_ctime': 9}
