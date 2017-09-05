#!usr/bin/python
# -*- coding: UTF-8 -*-
# use like python /Users/mac/easyLocalize.py /Users/mac/easyLocal/foot.m+Users/mac/easyLocal/dog.m Users/mac/easyLocal/Localizable.strings LOC
import sys
import re
import time
import os
import os.path

def gci(filepath, tmp):
#遍历filepath下所有文件，包括子目录
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)
    if os.path.isdir(fi_d):
      gci(fi_d,tmp)
    else:
      tmp.append(os.path.join(filepath,fi_d))

def dealWithArgs(arg):
    return arg.split('+')

def dealWithPaths1(paths):
    rList = []
    tmp = []
    gci(paths, rList)
    for path in rList:
        if '.m' == os.path.splitext(os.path.basename(path))[1]  or '.mm' == os.path.splitext(os.path.basename(path))[1] :
            tmp.append(path)
    return tmp

def dealWithPaths2(paths):
    rList = []
    tmp = []
    gci(paths,rList)
    for path in rList:
        if os.path.basename(path) == 'Localizable.strings':
            tmp.append(path)
    return tmp



def getCheckTable(localizableFilePath):
    table = []
    with open(localizableFilePath) as f:
        for line in f.readlines():
            if line != '\n' and not line.startswith('//'):
                table.append(line.split('=')[0].strip())
    return table

def getAllLocalizableStrings(inPath, checkTable, rString):
    table = []
    pattern = re.compile(rString + '\(\@\"([^\)]*)\"\)')
    with open(inPath) as f:
        for line in f.readlines():
            if not line.startswith('//'):
                if rString in line:
                    rlist = pattern.findall(line)
                    for item in rlist:
                        item = r'"'+ item + r'"'
                        if item not in checkTable:
                            table.append(item)
    return table

def writeTableToLocalizableFile(outPath,addTable, annotation):
    components = outPath.split(r'/')
    with open(outPath,'a') as f:
        f.write('\n')
        f.writelines(annotation)
        f.write('\n')
        if components[-2] == 'zh-Hans.lproj':
            for item in addTable:
                f.writelines(item + ' = ' + item + ';')
                f.write('\n')
            f.close()
        else:
            for item in addTable:
                f.writelines(item + ' = ' + r'" ";')
                f.write('\n')
            f.close()


if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("please check the args number")
    sys.exit(-1)
else:
    ifiles = dealWithPaths1(sys.argv[1])
    ofiles = dealWithPaths2(sys.argv[2])
    checkTable = getCheckTable(ofiles[0])
    addTable   = []
    if len(sys.argv) == 4:
        rString = dealWithArgs(sys.argv[3])
    else:
        rString = 'LOC'
    for inPath in ifiles:
        addTable.extend(getAllLocalizableStrings(inPath,checkTable,rString))
    addTable = list(set(addTable))
    print('items number added this time:',len(addTable),'\n')
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    t = time.strftime(ISOTIMEFORMAT, time.localtime())
    t = '//  ' + t
    for outPath in ofiles:
        writeTableToLocalizableFile(outPath,addTable,t)


