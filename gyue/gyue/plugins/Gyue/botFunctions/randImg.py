import random

import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
import gyue.gyue.plugins.Gyue.utils.fileOperation as fileopt
async def randImg(m:model.GroupMsgModel,dir:str):
    pth=fileopt.dirRedirect(f"{gs.path_botImgRandImg}/{dir}")
    fl=fileopt.getFileList(pth)
    index=random.randint(0, len(fl)-1)
    msg=m.CQ.Img(f"{pth}/{fl[index]}")
    await m.sendGroupMessage(msg,m.getGroupid())