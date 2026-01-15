import json

import nonebot
from nonebot.adapters.onebot.v11 import GroupRecallNoticeEvent


class GroupRecalledNoticeModel():
    timestamp:str
    groupid:str
    opid:str
    userid:str
    msgid:str
    evtdata: GroupRecallNoticeEvent
    bot: nonebot.Bot
    def __init__(self,e:GroupRecallNoticeEvent,bot:nonebot.Bot):
        x = json.loads(e.model_dump_json())
        self.timestamp = str(x["time"])
        self.groupid = str(x["group_id"])
        self.opid = str(x["operator_id"])
        self.userid = str(x["user_id"])
        self.msgid = str(x["message_id"])
        self.evtdata=e
        self.bot=bot
    def getTimestamp(self)->str:
        return self.timestamp
    def getGroupid(self)->str:
        return self.groupid
    def getopid(self)->str:
        return self.opid
    def getuserid(self)->str:
        return self.userid
    def getmsgid(self)->str:
        return self.msgid