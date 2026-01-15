import gyue.gyue.plugins.Gyue.GlobalScope
import gyue.gyue.plugins.Gyue.handles.Models.PrivateMsgModel as model
async def onMessage(m:model.PrivateMsgModel):
    print(f"{m.getUserid()}说\"{m.getMsg()}\",但是消息被丢弃了")
