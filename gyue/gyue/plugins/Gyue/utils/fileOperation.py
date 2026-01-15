import os

import chardet

def readByte(fileName):
    print(fileName)
    with open(fileName, "rb") as f:
        data = f.read()
        return data
def readFile(fileName)->str:
    with open(fileName, "rb") as f:
        data = f.read()
        res = chardet.detect(data)
        enc = res["encoding"]
        with open(fileName, encoding=enc) as ff:
            return ff.read()

def readFileLine(fileName)->list:
    with open(fileName, "rb") as f:
        data = f.read()
        res = chardet.detect(data)
        enc = res["encoding"]
        with open(fileName, encoding=enc) as ff:
            return ff.readlines()

def writeFile(fileName,content):
    with open(fileName,'w') as f:
        f.close()
    with open(fileName, "rb") as f:
        data = f.read()
        res = chardet.detect(data)
        enc = res["encoding"]
        with open(fileName,'w' ,encoding=enc) as ff:
            ff.write(content)

def getFileList(dir)->list:
    return os.listdir(dir)
def dirRedirect(dir)->str:
    if os.path.isfile(dir):
        return readFile(dir)
    return dir