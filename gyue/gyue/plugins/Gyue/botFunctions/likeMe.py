import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model
async def sendLike(m:model.GroupMsgModel)->bool:
    await m.bot.call_api('send_like', **{
        'user_id': f'{m.getUserid()}',
        'times': 10
    })
    await m.sendGroupMessage(m.CQ.At(m.getUserid())+"已发送 请查收",m.getGroupid())
    return True