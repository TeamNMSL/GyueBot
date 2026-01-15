import json
import gyue.gyue.plugins.Gyue.handles.Models.PrivateMsgModel as pmd
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as gmd
import gyue.gyue.plugins.Gyue.handles.pMsgHandle as pMsgHandle
import gyue.gyue.plugins.Gyue.handles.gMsgHandle as gMsgHandle
import nonebot



async def msgHandle(jsonStr:str,evt:nonebot.adapters.Event,bot:nonebot.Bot):
    model = json.loads(jsonStr);
    mtp: str = model["message_type"];
    if mtp == MessageType.groupMsg:
        val = gmd.GroupMsgModel();
        val.evtdata = evt;
        val.bot = bot;
        await gMsgHandle.onMessage(val);
    elif mtp == MessageType.privateMsg:
        val = pmd.PrivateMsgModel()
        val.evtdata = evt;
        val.bot = bot;
        await pMsgHandle.onMessage(val)

    else:
        raise NotImplementedError();



class MessageType:
    groupMsg="group";
    privateMsg="private";