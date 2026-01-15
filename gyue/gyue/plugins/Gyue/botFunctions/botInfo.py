import datetime
import platform

import cpuinfo
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
import psutil
import pynvml
import gyue.gyue.plugins.Gyue.botFunctions.updateQuery as uq


def getBotVersion():
    return f"BotVersion: {gs.get_value(gs.key_botVersionKey)}\n"


async def botInfo(m:model.GroupMsgModel):
    #msg=m.CQ.At(m.getUserid())+f"\n[System]\n{getSysPlatform()}{cpuStat()}{gpuStat()}{getMem()}\n[Bot]\n{getTime()}{getBotVersion()}\n[Update]\n{getUpdateInfo()}"
    msg = m.CQ.At(
        m.getUserid()) + f"[Bot]\n{getTime()}{getBotVersion()}\n[Update]\n{getUpdateInfo()}"
    await m.sendGroupMessage(msg,m.getGroupid())

def getUpdateInfo()->str:
    return uq.getLatestUpdateInfo()

def cpuStat()->str:
    cpuName=cpuinfo.get_cpu_info()["brand_raw"]
    usage=psutil.cpu_percent()
    return f"CPU: {cpuName}\nCPU_USAGE: {usage}%\n"

def gpuStat()->str:
    result=""
    pynvml.nvmlInit()
    for i in range(pynvml.nvmlDeviceGetCount()):
        hdl=pynvml.nvmlDeviceGetHandleByIndex(i)
        info=pynvml.nvmlDeviceGetMemoryInfo(hdl)
        result+=f"GPU{i}: {pynvml.nvmlDeviceGetName(hdl)}\nGPU{i}_USAGE: {round(info.used/1073741824,1)}/{round(info.total/1073741824,1)}(Gb)\n"
    return result

def getMem()->str:
    mem=psutil.virtual_memory()
    return f"Mem: {round(mem.used/1073741824,1)}/{round(mem.total/1073741824,1)}(Gb)\n"

def getTime()->str:
    dtmO=gs.get_value(gs.key_botStartTimeKey)
    dtmN=datetime.datetime.now()
    dt=dtmN-dtmO
    return f"UpTime: {dt}\n"

def getSysPlatform()->str:
    return f"Platform: {platform.platform()}\n"