import asyncio
import json
import nonebot.adapters.onebot.v11.message as Message
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment
import threading


class BaseMsgModel:
    evtdata: nonebot.adapters.Event
    bot: nonebot.adapters.onebot.V11Bot

    async def getMemberList(self,group)->list[dict]:
        return await self.bot.call_api("get_group_member_list",**{"group_id":group})

    def getEvt(self) -> nonebot.adapters.Event:
        return self.evtdata

    def getUserid(self) -> str:
        return self.getEvt().get_user_id()

    def getMsgid(self) -> str:
        return str(json.loads(self.getEvt().model_dump_json())["message_id"])

    def getTimeStamp(self) -> str:
        return str(json.loads(self.getEvt().model_dump_json())["time"])

    def getMsgSegment(self) -> str:
        return json.dumps(json.loads(self.getEvt().model_dump_json())["original_message"])

    async def sendGroupMessage(self, msg: str, gid: str, auto_escape: bool = False):
        await self.bot.call_api('send_group_msg', **{
            'message': f'{msg}',
            'group_id': gid,
            'auto_escape': auto_escape
        })

    def sendGroupMessageThread(self, msg: str, gid: str, auto_escape: bool = False):
        asyncio.create_task(self.sendGroupMessage(msg, gid, auto_escape))
        # a=threading.Thread(target=self.sendGroupMessage,args=(msg,gid,auto_escape))
        # a.start()

    async def sendPrivateMessage(self, msg: str, uid: str, auto_escape: bool = False):
        await self.bot.call_api('send_private_msg', **{
            'message': f'{msg}',
            'user_id': uid,
            'auto_escape': auto_escape
        })

    async def sendGroupForwardMsg(self, messages: list, gid: str):
        print({
            'group_id': f'{gid}',
            'messages': messages
        })
        await self.bot.call_api('send_group_forward_msg', **{
            'group_id': f'{gid}',
            'messages': messages
        })

    async def uploadFile(self,path:str,fname,gid:str):
        await self.bot.call_api('upload_group_file',**{

                "group_id": f'{gid}',
                "file": path,
                "name": fname
        })

    class forwardMsg:
        msg = []

        def addMsg(self, uName: str, uId: str, msg: nonebot.adapters.onebot.v11.message.Message | str):
            if type(msg) is str:
                self.msg.append({
                    "type": "node",
                    "data": {
                        "name": uName,
                        "uin": uId,
                        "content": msg
                    }
                })
            else:
                z:nonebot.adapters.onebot.v11.message.Message=msg
                k=[]
                for i in z:
                    k.append({
                        "type":i.type,
                        "data":i.data
                    })
                self.msg.append({
                    "type": "node",
                    "data": {
                        "name": uName,
                        "uin": uId,
                        "content": k
                    }
                })

        def getMessage(self):
            return self.msg

    class CQ:
        @staticmethod
        def At(qq: str):
            return MessageSegment.at(qq) + " "

        @staticmethod
        def Img(file: str | bytes):
            # print(f"img:{file}")
            return MessageSegment.image(file)

        @staticmethod
        def Segm():
            return MessageSegment

        @staticmethod
        def Audio(file: str | bytes):
            return MessageSegment.record(file)

        @staticmethod
        def Video(file: str | bytes):
            # print(f"img:{file}")
            return MessageSegment.video(file)
