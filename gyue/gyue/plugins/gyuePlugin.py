import json
import gyue.gyue.plugins.Gyue.utils.fileOperation as fo
import gyue.gyue.plugins.Gyue.handles.gNoticeRecalled
import nonebot
from gyue.gyue.plugins.Gyue.handles.Models.GroupRecalledNoticeModel import GroupRecalledNoticeModel
from nonebot import on_message
from nonebot import on_notice
from nonebot import on_request
from nonebot.adapters.onebot.v11 import Event, GroupRecallNoticeEvent
from nonebot.matcher import Matcher
import gyue.gyue.plugins.Gyue.handles.msgJson as messageHandle
from nonebot import get_bots
import gyue.gyue.plugins.Gyue.GlobalScope as gs

@on_message().handle()
async def allMsg_handle(event: Event, matcher: Matcher):
   await messageHandle.msgHandle(event.model_dump_json(), event, get_bots()[gs.const_botid])

@on_notice().handle()
async def allNotice_handle(event: Event, matcher: Matcher):
   evttype=event.get_event_name()
   if evttype=="notice.group_recall":
      e:GroupRecallNoticeEvent=event
      await gyue.gyue.plugins.Gyue.handles.gNoticeRecalled.onRecalled(GroupRecalledNoticeModel(e,get_bots()[gs.const_botid]))

@on_request().handle()
async def allRequest_handle(event:Event,matcher:Matcher):
   evttype=event.get_event_name()
   if evttype=="request.group.add":
      b:nonebot.adapters.onebot.V11Bot=get_bots()[gs.const_botid]
      es=event.model_dump_json()
      e=json.loads(es)
      if "812477441" in str(e["group_id"]):
         x=fo.readFile("groupmemberlist.txt")
         print(e)
         if str(e["user_id"]) in str(x):
            await b.set_group_add_request(**{"flag":str(e["flag"]),"sub_type":e["sub_type"],"approve":True})

#{"time":1718988932,"self_id":3923938731,"post_type":"notice","notice_type":"group_recall","user_id":3250184610,"group_id":691450484,"operator_id":3250184610,"message_id":-2147460823}