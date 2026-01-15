import gyue.gyue.plugins.Gyue.handles.Models.GroupRecalledNoticeModel as gnm
from gyue.gyue.plugins.Gyue.utils.sql import SQLiteHelper
import gyue.gyue.plugins.Gyue.GlobalScope as gs

async def onRecalled(e:gnm.GroupRecalledNoticeModel):
    db = SQLiteHelper(gs.path_botMsgDb)
    x=gs.SQLKeys.MsgDB
    d=db.select(x.tableName,'*',f"{x.msgid}='{e.getmsgid()}'")[0]
    db.cupdate(x.tableName, {
        x.groupid: e.getGroupid(),
        x.userid: e.getuserid(),
        x.msg: d[x.msg],
        x.msgid: e.getmsgid(),
        x.stamp: d[x.stamp],
        x.recalled: e.getTimestamp(),
        x.opId:e.getopid()
    }, f"{x.msgid}='{e.getmsgid()}'")
