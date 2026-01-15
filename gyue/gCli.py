import os
import sys
from importlib import reload
class DummyStream(object):
    def write(self,text):
        pass
def gyueCli():
    while True:
        uInput=input()
        if uInput=="exit":
            os._exit(0)
        elif uInput.startswith("reload"):
            gReload(uInput)


def gReload(moduleName:str):
    """
    try:
        reload(moduleName.split(" ")[1])
    except:
        print("重载失败")
        return
    print("重载成功")
    return
    """
    print(moduleName.split(" ")[1])
    reload(moduleName.split(" ")[1])
