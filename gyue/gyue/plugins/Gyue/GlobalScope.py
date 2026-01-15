import datetime
import os.path
import builtins
import chardet
import gyue.gyue.plugins.Gyue.utils.fileOperation as fileOpt
import gyue.gyue.plugins.Gyue.utils.textOpt as txtOpt
from gyue.gyue.plugins.Gyue.utils.sql import SQLiteHelper

const_botid:str = "3923938731"
path_botDataPath= "D:/Bot/GyueBot/Data"
path_botAudioPath=f"{path_botDataPath}/Audio"
path_botJMdl=f"{path_botDataPath}/JM"
path_botTmpPath=f"{path_botDataPath}/Tmp"
path_botTmpAudioPath=f"{path_botTmpPath}/Audio"
path_botTmpVideoPath=f"{path_botTmpPath}/Video"
path_botTmpVideoPathCache=f"{path_botTmpVideoPath}/Cache"
path_botHzysPath=f"{path_botAudioPath}/huoziyinshua"
path_botImgPath=f"{path_botDataPath}/img"
path_botImgFortuneDir=f"{path_botImgPath}/fortune"
path_botImgTarotDir=f"{path_botImgPath}/tarot"
path_botImgRandImg=f"{path_botImgPath}/randImg"
path_botUpdateLogFile=f"{path_botDataPath}/updatelog.json"
path_botDatabaseDir=f"{path_botDataPath}/database"
path_botMsgDb=f"{path_botDatabaseDir}/Msgdb.db"


key_botUpdateLogKey="str_botUpdateLog"
key_botVersionKey="str_botVersionCode"
key_botStartTimeKey="dateTime_botStartTime"


class SQLKeys:
    #MsgDB:
    #GroupId(private=0)   UserId   MessageContent   MessageId   Timestamp   isRecalled
    class MsgDB:
        tableName="MsgDB"#表名 MSGDB 消息数据库
        groupid="GroupId" #群号
        userid="UserId"#QQ号
        msg="MessageContent"#消息内容（Segment）
        msgid="MessageId"#消息Id
        stamp="TimeStamp"#时间
        recalled="Recalled"#是否撤回
        opId="OperatorId"#操作人

def set_value(key, value):
    builtins.gs[key] = value

def get_value(key, defValue=None):
    try:
        return builtins.gs[key]
    except KeyError:
        return defValue


def setVersion():
    arr=fileOpt.readFileLine("version.txt")
    versionCode=txtOpt.versionCodeGen(arr[0],arr[1],arr[2],arr[4],arr[3])
    set_value(key_botVersionKey,versionCode)


def initBot():
    builtins.gs={}
    setVersion()
    set_value(key_botStartTimeKey,datetime.datetime.now())
    set_value("isDeloresCued",False)
    if not os.path.exists(path_botDataPath):
        os.mkdir(path_botDataPath)
    if not os.path.exists(path_botImgPath):
        os.mkdir(path_botImgPath)
    if not os.path.exists(path_botImgFortuneDir):
        os.mkdir(path_botImgFortuneDir)
    if not os.path.exists(path_botImgTarotDir):
        os.mkdir(path_botImgTarotDir)
    if not os.path.exists(path_botUpdateLogFile):
        set_value(key_botUpdateLogKey,"[]")
    else:
        set_value(key_botUpdateLogKey, fileOpt.readFile(path_botUpdateLogFile))
    if not os.path.exists(path_botImgRandImg):
        os.mkdir(path_botImgRandImg)
    if not os.path.exists(path_botAudioPath):
        os.mkdir(path_botAudioPath)
    if not os.path.exists(path_botJMdl):
        os.mkdir(path_botJMdl)
    if not os.path.exists(path_botHzysPath):
        os.mkdir(path_botHzysPath)
    if not os.path.exists(path_botTmpPath):
        os.mkdir(path_botTmpPath)
    if not os.path.exists(path_botTmpAudioPath):
        os.mkdir(path_botTmpAudioPath)
    if not os.path.exists(path_botTmpVideoPath):
        os.mkdir(path_botTmpVideoPath)
    if not os.path.exists(path_botTmpVideoPathCache):
        os.mkdir(path_botTmpVideoPathCache)
    if not os.path.exists(path_botMsgDb):
        db=SQLiteHelper(path_botMsgDb)
        x =SQLKeys.MsgDB()
        db.createTable(x.tableName, {
            x.groupid: "TEXT",
            x.userid: "TEXT",
            x.msg: "TEXT",
            x.msgid: "TEXT",
            x.stamp: "TEXT",
            x.recalled: "TEXT",
            x.opId:"TEXT"
        })
    pass


