from dataclasses import dataclass
from typing import Literal


@dataclass
class Location:
    timestamp: int = 0
    abs_path: str = None
    delete: bool = False

@dataclass
class File:
    checksum: str = None
    locations: list[Location] = None
    duplicate: bool = False
    count: int = 0


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
ST_Index = {'st_atime': 8,
            'st_mtime': 9,
            'st_ctime': 10}