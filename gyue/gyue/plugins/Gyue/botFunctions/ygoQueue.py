import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.utils.fileOperation as fileopt

async def addPlayer(m: model.GroupMsgModel):
    username=m.getMsg().replace("/排队","")
    connected_clients=gs.get_value("connected_clients")
    for client in connected_clients:
        await client.send(f"add {username.replace("\n","")}")
    await m.sendGroupMessage(f"已向排队板发送用户{username}，有没有请自行查看直播间排队板",m.getGroupid())

async def delPlayer(m: model.GroupMsgModel):
    connected_clients = gs.get_value("connected_clients")
    for client in connected_clients:
        await client.send(f"del")
    await m.sendGroupMessage(f"[DuelQueue]\nDeleted", m.getGroupid())

async def delAllPlayer(m: model.GroupMsgModel):
    connected_clients = gs.get_value("connected_clients")
    for client in connected_clients:
        await client.send(f"delall")
    await m.sendGroupMessage(f"[DuelQueue]\nCleared", m.getGroupid())