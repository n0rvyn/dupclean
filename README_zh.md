# 文件消重脚本

A set of scripts to delete duplicate files.  
本来是‘a set’，import来import去太麻烦，先弄个简版。

## 目录
- [适用平台](#requirement)
- [用法](#usage)


## 适用平台
- macOS
- Linux

## 用法
```bazaar
    Usage: duplicateclean.py [options] PATH

    Options:
          --dryrun             analyze and shows the result, delete nothing

          -h, --help           display this help message and exit

          -f, --folder         target directory to analyze, default '.'

          -r, --recursively    recursively analyze entire directories
          -a, --hash-algorithm 'sha512' or 'md5'(default)

          -c, --count          number of copies to hold even all duplicate met the filter
                               depends on the value of '--st-time' and '--priority'
          -t, --st-time        'st_mtime', 'st_atime', or 'st_ctime'
          -p, --priority       choose 'oldest' or 'latest' st_time to hold the file

          --key-to-hold        keywords to hold the file, "key1, key2..."
          --key-to-burn        keywords to burn the file
          --suffix-to-hold     suffix to hold the file
          --suffix-to-burn     suffix to burn the file

          --key-to-path-hold   keywords to hold the file by file's absolute path.
          --key-to-path-burn   keywords to burn the file by file's absolute path.
```

## Example - 示例

### 以md5值为依据列出重复文件
```bash
$ ./duplicateclean.py --dryrun -r -p oldest  -f ./test
checksum:  fc87c7dea6d66d0a61f9806911848b9a
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/same_as_fileoperator.py'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/fileoperator.py'
checksum:  4e58964ad5ebfdbf50a679861490ebb1
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py'
	 hold  1692100162 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak.230846.py'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py 2'
```

### 添加标记删除关键字和后缀进行筛选
```bash
$ ./duplicateclean.py --dryrun -r -p oldest  -f ./test --key-to-burn 'same_as,mongo' --suffix-to-burn '.bak, 2'
checksum:  fc87c7dea6d66d0a61f9806911848b9a
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/same_as_fileoperator.py'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/fileoperator.py'
checksum:  4e58964ad5ebfdbf50a679861490ebb1
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py'
	 burn  1692100162 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak.230846.py'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py 2'
```

### 至少保留一个副本'-c 1'， 保留时间策略'-p latest'，最新优先
```bash
$ ./duplicateclean.py --dryrun -r -p latest -f ./test --key-to-burn 'same_as,mongo' --suffix-to-burn '.bak, 2' -c 1
checksum:  fc87c7dea6d66d0a61f9806911848b9a
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/same_as_fileoperator.py'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/fileoperator.py'
checksum:  4e58964ad5ebfdbf50a679861490ebb1
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py'
	 hold  1692100162 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak.230846.py'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py 2'
```

### 以'sha512'值为依据重新计算重复文件
```bash
$ ./duplicateclean.py --dryrun -r -p latest -f ./test --key-to-burn 'same_as,mongo' --suffix-to-burn '.bak, 2' -c 1 --hash-algo 'sha512'
checksum:  3ea7013447d2a726e548db65075313035185fd2debbfbb4ac95f3dd710cc39d8d933ea515a81719a1d20e3c41ca96b0d3419c502bb772571b8918967fee49a9a
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/same_as_fileoperator.py'
	 hold  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/fileoperator.py'
checksum:  e7035c79fdb52282ffc926c21f61669bd35bbb6fa7cb7cb5eac1683a4cf8df5b8483ae58fed1caebb0381d36021df886886a1675c203c4873f8da69463cddf0b
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py'
	 hold  1692100162 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak.230846.py'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.bak'
	 burn  1692100039 '/Users/beyan/Documents/Scripts/40-Python/duplicateclean-0.0.1/test/mongodb.py 2'
```

## 下载地址
