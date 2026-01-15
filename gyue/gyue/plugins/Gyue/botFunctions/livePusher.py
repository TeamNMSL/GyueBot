import asyncio
import datetime
import random
import threading
import time
import gyue.gyue.plugins.Gyue.handles.Models.BaseMsgModel as bmm
from bilireq.live import get_rooms_info_by_uids
from nonebot import get_bots
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.log import logger
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.configs.Sublist as sbl


status = {}
live_time = {}

def calc_time_total(t):
    t = int(t * 1000)
    if t < 5000:
        return f"{t} 毫秒"

    timedelta = datetime.timedelta(seconds=t // 1000)
    day = timedelta.days
    hour, mint, sec = tuple(int(n) for n in str(timedelta).split(",")[-1].split(":"))

    total = ""
    if day:
        total += f"{day} 天 "
    if hour:
        total += f"{hour} 小时 "
    if mint:
        total += f"{mint} 分钟 "
    if sec and not day and not hour:
        total += f"{sec} 秒 "
    return total

#原版
async def live_sched():
    # sourcery skip: use-fstring-for-concatenation
    """直播推送"""
    uids = [2079997275] #主播账号UID

    if not uids:  # 订阅为空
        return
    logger.debug(f"爬取直播列表，目前开播{sum(status.values())}人，总共{len(uids)}人")
    res = await get_rooms_info_by_uids(uids, reqtype="web")
    if not res:
        return
    for uid, info in res.items():
        new_status = 0 if info["live_status"] == 2 else info["live_status"]
        if uid not in status:
            status[uid] = new_status
            continue
        old_status = status[uid]
        if new_status == old_status:  # 直播间状态无变化
            continue
        status[uid] = new_status

        name = info["uname"]
        if new_status:  # 开播
            live_time[uid] = info["live_time"]
            room_id = info["short_id"] or info["room_id"]
            url = f"https://live.bilibili.com/{room_id}"
            title = info["title"]
            cover = info["cover_from_user"] or info["keyframe"]
            area = info["area_v2_name"]
            area_parent = info["area_v2_parent_name"]
            room_area = f"{area_parent} / {area}"
            logger.info(f"检测到开播：{name}（{uid}）")
            live_msg = (
                f"{name} 开播啦！\n分区：{room_area}\n标题：{title}\n"
                + MessageSegment.image(cover)
                + f"\n{url}"
            )
        else:  # 下播
            logger.info(f"检测到下播：{name}（{uid}）")
            if not True:  # 没开下播推送
                continue
            live_time_msg = (
                f"\n本次直播时长 {calc_time_total(time.time() - live_time[uid])}。"
                if live_time.get(uid)
                else "。"
            )
            live_msg = f"{name} 下播了{live_time_msg}"

#魔改版

async def dBg_HXN():
    uids=["15688975","313683284"]
    res = await get_rooms_info_by_uids(uids, reqtype="web")
    if not res:
        return
    # 遍历并发送消息
    for uid, info in res.items():
        name = info["uname"]
        live_time[uid] = info["live_time"]
        room_id = info["short_id"] or info["room_id"]
        url = f"https://live.bilibili.com/{room_id}"
        title = info["title"]
        cover = info["cover_from_user"] or info["keyframe"]
        area = info["area_v2_name"]
        area_parent = info["area_v2_parent_name"]
        room_area = f"{area_parent} / {area}"
        logger.info(f"检测到开播：{name}（{uid}）")
        cstMsgList=[f"嘿！是我，拽姐！{name}说你连他都不理了。都开播了还不看直播，佩服佩服",f"嘿！是多儿！抽出几分钟和我一起看{name}直播怎么样"]
        cstMsg=cstMsgList[random.randint(0,len(cstMsgList)-1)]
        live_msg = (
                f"{cstMsg} \n分区：{room_area}\n标题：{title}\n"
                + MessageSegment.image(cover)
                + f"\n{url}\n{random.randint(1,100)}"
        )
        msgsend(live_msg, uid, 0)
        logger.info(f"检测到下播：{name}（{uid}）")
        if not True:  # 没开下播推送
            continue
        live_time_msg = (
            f"\n本次直播时长 {calc_time_total(time.time() - live_time[uid])}。"
            if live_time.get(uid)
            else "。"
        )
        live_msg = f"{name} 下播了{live_time_msg}该打开多邻国学习了。"
        msgsend(live_msg, uid, 1)
    # 遍历完了


async def liveTest():
    # sourcery skip: use-fstring-for-concatenation
    """直播推送"""
    uids = [] #主播账号UID
    subList=sbl.SubscribeList
    for liverUid in subList:
        uids.append(liverUid)

    if not uids:  # 订阅为空
        return
    logger.debug(f"爬取直播列表，目前开播{sum(status.values())}人，总共{len(uids)}人")
    res = await get_rooms_info_by_uids(uids, reqtype="web")
    if not res:
        return
    #遍历并发送消息
    for uid, info in res.items():
        new_status = 0 if info["live_status"] == 2 else info["live_status"] #如果info["live_status"]的值等于2，则new_status被赋值为0，否则new_status被赋值为info["live_status"]的值。
        if uid not in status:
            status[uid] = new_status
            continue
        old_status = status[uid]
        if new_status == old_status:  # 直播间状态无变化
            continue
        status[uid] = new_status

        name = info["uname"]
        if new_status:  # 开播
            live_time[uid] = info["live_time"]
            room_id = info["short_id"] or info["room_id"]
            url = f"https://live.bilibili.com/{room_id}"
            title = info["title"]
            cover = info["cover_from_user"] or info["keyframe"]
            area = info["area_v2_name"]
            area_parent = info["area_v2_parent_name"]
            room_area = f"{area_parent} / {area}"
            logger.info(f"检测到开播：{name}（{uid}）")
            cstMsgList = [f"嘿！是我，拽姐！{name}说你连他都不理了。都开播了还不看直播，佩服佩服",
                          f"嘿！是多儿！抽出几分钟和我一起看{name}直播怎么样"]
            cstMsg = cstMsgList[random.randint(0, len(cstMsgList) - 1)]
            live_msg = (
                    f"{cstMsg} \n分区：{room_area}\n标题：{title}\n"
                    + MessageSegment.image(cover)
                    + f"\n{url}\n{random.randint(1, 100)}"
            )
            msgsend(live_msg,uid,0)
        else:  # 下播
            logger.info(f"检测到下播：{name}（{uid}）")
            if not True:  # 没开下播推送
                continue
            live_time_msg = (
                f"\n本次直播时长 {calc_time_total(time.time() - live_time[uid])}。"
                if live_time.get(uid)
                else "。"
            )
            live_msg = f"{name} 下播了{live_time_msg}该打开多邻国学习了。"
            msgsend(live_msg,uid,1)
    #遍历完了


async def livechkloop():
    try:
        while True:
            time.sleep(10)
            await asyncio.create_task(liveTest())
    except:
        return




def livecheck():
    aa=threading.Thread(target=asynciorun())
    aa.start()
    time.sleep(2)
    while True:
        if not aa.is_alive():
            print("直播线程死了 已重启")
            livecheck()
            return

def asynciorun():
    asyncio.run(livechkloop())

def msgsend(s,uid:str,typ:int):
    target:dict=sbl.SubscribeList[uid]
    print(target)
    i=0
    for g,b in target.items():
        time.sleep(1)
        i=i+1
        print(f"向第{i}个群推送")
        sendLivePush(s,g,b,typ)

def sendLivePush(s,gid:str,atall:bool,typ:int):
    m=bmm.BaseMsgModel()
    m.bot=get_bots()[gs.const_botid]
    if atall and typ==0:
        s=m.CQ.At("all")+s
    s=s+f"\n[{random.randint(0,65536)}]"
    m.sendGroupMessageThread(s,gid)
    print(f"向群组:{gid}发送了{s}")