import os.path
import gyue.gyue.plugins.Gyue.GlobalScope
import gyue.gyue.plugins.Gyue.utils.fileOperation as fo
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
import gyue.gyue.plugins.Gyue.botFunctions.fortune as fortune
import gyue.gyue.plugins.Gyue.botFunctions.tarotSingle as tarotS
import gyue.gyue.plugins.Gyue.botFunctions.tarotPro as tarotP
import gyue.gyue.plugins.Gyue.botFunctions.botInfo as botInfo
import gyue.gyue.plugins.Gyue.botFunctions.randImg as randimg
import gyue.gyue.plugins.Gyue.botFunctions.likeMe as likeMe
import gyue.gyue.plugins.Gyue.botFunctions.randNum as randNum
import gyue.gyue.plugins.Gyue.botFunctions.huoziyinshua as hzys
import gyue.gyue.plugins.Gyue.botFunctions.emoji.emojimix as emormx
import gyue.gyue.plugins.Gyue.botFunctions.ygoQueue as ygoqueue
import gyue.gyue.plugins.Gyue.botFunctions.JMDl as jm
from gyue.gyue.plugins.Gyue.utils.sql import SQLiteHelper
import gyue.extlib.bvideo.bvideoParse as bvp
import gyue.gyue.plugins.Gyue.GlobalScope as gs




devGroup=["691450484","917074903"]
adminList=["3250184610","2898907618"]
vidEnableGroup=["691450484","917074903","877879736","1016806616"]
def isIn(lst,elm)->bool:
    for i in lst:
        if i==elm:
            return True
    return False


def addMsg(m:model.GroupMsgModel):
    db = SQLiteHelper(gs.path_botMsgDb)
    x = gs.SQLKeys.MsgDB
    db.cinsert(x.tableName,
        {
            x.groupid: m.getGroupid(),
            x.userid: m.getUserid(),
            x.msg: m.getMsgSegment(),
            x.msgid: m.getMsgid(),
            x.stamp: m.getTimeStamp(),
            x.recalled: "0",
            x.opId:"0"
    })



async def onMessage(m:model.GroupMsgModel):
    addMsg(m)
    msg:str=m.getMsg()
    if isIn(devGroup,m.getGroupid()):
        if msg.startswith("/test "):
            a=m.forwardMsg()
            a.addMsg("Himeki","1848200159","jaja")
            a.addMsg("Shizuku",m.getUserid(),m.CQ.Img("C:/Users/AmemiyaHimeki/Desktop/b3c61b0a74c148d639f2a13a1efded84ed1c5518.jpg")+"abc")
            await m.sendGroupForwardMsg(a.getMessage(),m.getGroupid())

    if isIn(adminList,m.getUserid()):
        if msg=="/dq del":
            await ygoqueue.delPlayer(m)
        if msg=="/dq clear":
            await ygoqueue.delAllPlayer(m)
        if msg=="/saveGroupMemberWhiteList()":
            x=await m.getMemberList(m.getGroupid())
            l=[]
            for i in x:
                l.append(str(i["user_id"]))
            fo.writeFile(f"{m.getGroupid()}.txt",'\n'.join(l))



    if msg=="今日运势":
        await fortune.fortune(m)
        return
    if msg.endswith("运势") and ("昨" in msg or "明" in msg or "前" in msg or "后" in msg):
        await fortune.sbFortune(m)
        return
    if msg=="抽塔罗牌":
        await tarotS.singleCard(m)
        return
    if msg.startswith("抽塔罗牌 "):
        await tarotP.tarotMain(m)
        return
    if msg=="botinfo":
        await botInfo.botInfo(m)
        return
    if msg=="龙图来":
        await randimg.randImg(m,"dragonpicture")
        return
    if msg=="赞我":
        await likeMe.sendLike(m)
        return
    if msg.startswith("随机数 "):
        await randNum.randNum(m)
        return
    if msg.startswith("/活字印刷 "):
        await hzys.checkName(m)
        return
    if msg.startswith("/mix"):
        await emormx.emojimix(m)
        return
    if msg.startswith("/jm") or msg.startswith("/xjm"):
        jm.process(m)
        return
    if isIn(vidEnableGroup,m.getGroupid()):
        vp = await bvp.forceParse(m.getMsgSegment())
        if vp:
            await m.sendGroupMessage( "正在帮你把视频端到群里", m.getGroupid())
            await m.sendGroupMessage(m.CQ.Video(vp), m.getGroupid())
            return
    return



