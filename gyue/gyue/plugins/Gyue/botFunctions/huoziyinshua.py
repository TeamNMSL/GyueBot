import datetime

from gyue.extlib.huoziyinshua import *
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
def exportWav(speakerName:str,text:str,outputPath:str):
    sDir=f"{gs.path_botHzysPath}/{speakerName}"
    HZYS=huoZiYinShua(buildCfg(sourceDir=f"{sDir}/source/",
                      ostDir=f"{sDir}/ost/",
                      dictFile=f"{sDir}/dictionary.json",
                      ostTable=f"{sDir}/ostTable.json"))
    HZYS.export(text,
                filePath=outputPath,#输出路径
                inYsddMode=True,#原声大碟模式
                pitchMult=1,#1默认，大于1升调小于1降调
                speedMult=1,#1默认，大于1加速小于1减速
                reverse=False,#倒放
                norm=False)#标准化音量


def buildCfg(sourceDir:str,ostDir:str,dictFile:str,ostTable:str):
    return {
	"sourceDirectory": sourceDir,
	"ysddSourceDirectory": ostDir,
	"dictFile": dictFile,
	"ysddTableFile": ostTable}


speakerList={
    "包菜":"milicon",
    "电棍":"otto"
}

async def checkName(m:model.GroupMsgModel):
    #/活字印刷 内容
    #/活字印刷 名字 内容
    msgarr=m.getMsg().split(" ")
    if len(msgarr)==2:
        res=callExport("otto",m.getMsg().replace(msgarr[0]+" ",""),m)
    else:
        if(msgarr[1] in speakerList.keys()):
            res=callExport(speakerList[msgarr[1]],m.getMsg().replace(msgarr[0]+" ","").replace(msgarr[1]+" ",""),m)
        else:
            res = callExport("otto", m.getMsg().replace(msgarr[0] + " ", ""), m)
    await m.sendGroupMessage(m.CQ.Audio(res),m.getGroupid())



def callExport(name:str,text:str,m:model)->str:
    t=datetime.datetime.now().timestamp()
    path=f"{gs.path_botTmpAudioPath}/hzys.{name}.{t}.wav"
    exportWav(name,text,path)
    return path