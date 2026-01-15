import os
import sys
import gyue.plugins.Gyue.utils.textOpt as txtOpt
import bot

import chardet
os.chdir((sys.argv[0].replace("bot.py", "").replace("devStart.py", "")))
with open("version.txt", "rb") as f:
    data = f.read()
    res = chardet.detect(data)
    enc = res["encoding"]
with open("version.txt","r", encoding=enc) as ff:
    arr=ff.readlines()
mV=int(arr[0].replace("\r","").replace("\n",""))
sV=int(arr[1].replace("\r","").replace("\n",""))
pV=int(arr[2].replace("\r","").replace("\n",""))
bV=int(arr[3].replace("\r","").replace("\n",""))
pV+=1
bV+=1
cV=arr[4].replace("\r","").replace("\n","")
with open("version.txt","w", encoding=enc) as ff:
    ff.write(f"{mV}\n{sV}\n{pV}\n{bV}\n{cV}")
versionCode=txtOpt.versionCodeGen(mV,sV,pV,"Dev",bV)
bot.m(versionCode)