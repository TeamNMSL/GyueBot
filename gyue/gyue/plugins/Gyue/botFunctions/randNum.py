import random

import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
async def randNum(m:model.GroupMsgModel):
    msg=m.getMsg()
    if msg=="随机数 帮助":
        await m.sendGroupMessage(m.CQ.At(m.getUserid()) + f"[随机数帮助]\n例子:\n随机数 5 20 <-这是生成一个5-20的随机数的指令\n随机数 1145 <-生成一个0-1145的随机数指令",m.getGroupid())
        return
    a=msg.split(" ")
    num=0
    if len(a)==3:
        num=random.randint(int(a[1]),int(a[2]))
    elif len(a)==2:
        num=random.randint(0,int(a[1]))
    else:
        return
    await m.sendGroupMessage(m.CQ.At(m.getUserid())+f"你随机到的数为: {num}",m.getGroupid())

