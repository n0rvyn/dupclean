# dupclean
用来标记并清理重复文件的小工具

## 兼容平台
- macOS
- Linux

## 用法
```bazaar
Usage: dupclean.py [action] [options] [filter] [path]
       dupclean.py -h | --help

# PATH:  The last parameter is considered as working folder by default.
Path:
       -f, --folder                     the working directory
       -h, --help                       display this help message and exit

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
      
Filter:
       --key-to-hold "K1, K2..."        keywords to hold the file, "key1, key2..."
       --key-to-burn "K1, K2..."        keywords to burn the file
       --suffix-to-hold "K1, K2..."     suffix to hold the file
       --suffix-to-burn "K1, K2..."     suffix to burn the file
       --key-to-path-hold "K1, K2..."   keywords to hold the file by file's absolute path.
       --key-to-path-burn "K1, K2..."   keywords to burn the file by file's absolute path.
       
Example:
       dupclean.py -r -c 1 --key-to-burn 'test,log' --suffix-to-burn '.bak,.log' /path/to/folder

```

## 示例

### 人为创造用来测试的重复文件
#### 1. 在`/tmp`下创建目录 `test`
```bash
mkdir /tmp/test
```

#### 2. 复制该项目源文件到目录`/tmp/test`
```bash
cp -r /path/to/dupclean/ /tmp/test/
```

#### 3. 制造重复文件
```bash
for f in `ls -1 /tmp/test/modules/`; do cp /tmp/test/modules/{"$f","$f".bak}; done
```

### 下载`dupclean`二进制文件并拷贝到目录`/tmp`
```bash
cp /path/to/dupclean /tmp
```

### 用`dupclean`命令列出重复文件

#### 1. 列出文件
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

#### 2. 通过添加关键字和后缀来标记文件目录为`burn`或者`hold`
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

#### 3. 通过`-c 1`选项控制同一个文件最少保留的副本数
如：`__init__`文件及其备份由于满足`--key-to-burn="init"`而均被标记为删除

添加保留副本选项后，默认以文件修改时间`st_mtime`为序标记最近`latest`的路径为`hold` (选项为`-p [latest | oldest]`).
```bash
beyan@MacHome /tmp/test/modules $ /tmp/dupclean -r -f /tmp/test --suffix-to-burn '.bak' --key-to-burn 'init' -c 1
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

#### 4. 添加参数`--run`直接删除已标记的文件，或者`-b /path/to/backup/ --run`将标记文件移动到指定的目录中
```bash
mkdir /tmp/backup
/tmp/dupclean -r -f /tmp/test --suffix-to-burn '.bak' --key-to-burn 'init' -c 1 -b /tmp/backup --run
```

## 源码地址
[GitHub](https://github.com/n0rvyn/dupclean)
