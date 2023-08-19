# Duplicate Clean
A simple tool to delete duplicate files.  

## Table of Content
- [Compatible Platform](#compatible-platform)
- [Usage](#usage)
- [Example](#example)


## Compatible Platform
- macOS
- Linux

## Usage
```bazaar
Usage: dupclean.py [action] [options] [filter] [path]
       dupclean.py [-h | --help]           display this help message and exit

Path:
       -f, --folder                     the working directory

Actions:
       --run                            analyze and delete the files marked as 'burn'

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
       --key-to-hold "K1,K2..."        keywords to hold the file, "key1, key2..."
       --key-to-burn "K1,K2..."        keywords to burn the file
       --suffix-to-hold "K1,K2..."     suffix to hold the file
       --suffix-to-burn "K1,K2..."     suffix to burn the file
       --key-to-path-hold "K1,K2..."   keywords to hold the file by file's absolute path
       --key-to-path-burn "K1,K2..."   keywords to burn the file by file's absolute path

Warning: 
       Do NOT leave blank after ',' for specifying more than 2 keywords, 
       because the BLANK will be considered as the first part of the next keyword. 
       
Example:
       dupclean.py -r -c 1 --key-to-burn 'test,log' --suffix-to-burn '.bak,.log' /path/to/folder
```

## Example

### Manually creating duplicate files
#### 1. Creating a directory named 'test' under '/tmp'
```bash
mkdir /tmp/test
```

#### 2. Coping `dupclean` source files to directory `/tmp/test`
```bash
cp -r /path/to/dupclean/ /tmp/test/
```

#### 3. Creating duplicate files
```bash
for f in `ls -1 /tmp/test/modules/`; do cp /tmp/test/modules/{"$f","$f".bak}; done
```

### Downloading `dupclean` bin file and coping to `/tmp`
```bash
cp /path/to/dupclean /tmp
```

### Listing and deleting duplicate files with `dupclean`

#### 1. Listing files
```bash
$ /tmp/dupclean -r -f /tmp/test
---------------------------------------- Duplicate Results ----------------------------------------
checksum:  6e5e4d9714608714ce952f5c42555b3d
         hold  1692413845 '/tmp/test/modules/__init__.py'
         hold  1692414154 '/tmp/test/modules/__init__.py.bak'
checksum:  d55ecb1291a11d396eccfaadfb9133f5
         hold  1692413845 '/tmp/test/modules/filter.py'
         hold  1692414154 '/tmp/test/modules/filter.py.bak'
checksum:  ed0178bb65e6747a77017ff3fccd26af
         hold  1692413845 '/tmp/test/modules/datatype.py'
         hold  1692414154 '/tmp/test/modules/datatype.py.bak'
checksum:  9a20e19c2f93f5e689408d0994ad4b2e
         hold  1692413845 '/tmp/test/modules/listduplicate.py'
         hold  1692414154 '/tmp/test/modules/listduplicate.py.bak'
---------------------------------------- Duplicate Results ----------------------------------------
Need taking action, followed with "--run" parameter.
You can also move the files to directory followed by "-b" or "--backup" instead of deleting directly.

```

#### 2. Adding `keyword` and `suffix` to mark files as `burn` or `hold`
```bash
$ /tmp/dupclean -r -f /tmp/test --suffix-to-burn '.bak' --key-to-burn 'init' 
---------------------------------------- Duplicate Results ----------------------------------------
checksum:  6e5e4d9714608714ce952f5c42555b3d
         burn  1692413845 '/tmp/test/modules/__init__.py'
         burn  1692414154 '/tmp/test/modules/__init__.py.bak'
checksum:  d55ecb1291a11d396eccfaadfb9133f5
         hold  1692413845 '/tmp/test/modules/filter.py'
         burn  1692414154 '/tmp/test/modules/filter.py.bak'
checksum:  ed0178bb65e6747a77017ff3fccd26af
         hold  1692413845 '/tmp/test/modules/datatype.py'
         burn  1692414154 '/tmp/test/modules/datatype.py.bak'
checksum:  9a20e19c2f93f5e689408d0994ad4b2e
         hold  1692413845 '/tmp/test/modules/listduplicate.py'
         burn  1692414154 '/tmp/test/modules/listduplicate.py.bak'
---------------------------------------- Duplicate Results ----------------------------------------
Need taking action, followed with "--run" parameter.
You can also move the files to directory followed by "-b" or "--backup" instead of deleting directly.
```

#### 3. Setting `-c 1` option to `hold` at least on copy of each file
Both of origin and copy of `__init__` are marked as *burn* from last output. 

After adding `-c 1` option:
```bash
$ /tmp/dupclean -r -f /tmp/test --suffix-to-burn '.bak' --key-to-burn 'init' -c 1
---------------------------------------- Duplicate Results ----------------------------------------
checksum:  6e5e4d9714608714ce952f5c42555b3d
         burn  1692413845 '/tmp/test/modules/__init__.py'
         hold  1692414154 '/tmp/test/modules/__init__.py.bak'
checksum:  d55ecb1291a11d396eccfaadfb9133f5
         hold  1692413845 '/tmp/test/modules/filter.py'
         burn  1692414154 '/tmp/test/modules/filter.py.bak'
checksum:  ed0178bb65e6747a77017ff3fccd26af
         hold  1692413845 '/tmp/test/modules/datatype.py'
         burn  1692414154 '/tmp/test/modules/datatype.py.bak'
checksum:  9a20e19c2f93f5e689408d0994ad4b2e
         hold  1692413845 '/tmp/test/modules/listduplicate.py'
         burn  1692414154 '/tmp/test/modules/listduplicate.py.bak'
---------------------------------------- Duplicate Results ----------------------------------------
Need taking action, followed with "--run" parameter.
You can also move the files to directory followed by "-b" or "--backup" instead of deleting directly.
```

#### 4. Deleting files with `--run` action or just move to backup directory with `-b /path/to/backup --run` 
```bash
mkdir /tmp/backup
/tmp/dupclean -r -f /tmp/test --suffix-to-burn '.bak' --key-to-burn 'init' -c 1 -b /tmp/backup --run
```

## Code URL
[GitHub](https://github.com/n0rvyn/dupclean)
