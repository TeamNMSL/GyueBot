from .emoji_data import dates, emojis
from typing import List, Optional, Union
import httpx
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model

API = "https://www.gstatic.com/android/keyboard/emojikitchen/"

def find_emoji(emoji_code: str) -> Optional[List[int]]:
    emoji_num = ord(emoji_code)
    for e in emojis:
        if emoji_num in e:
            return e
    return None

def create_url(date: str, emoji1: List[int], emoji2: List[int]) -> str:
    def emoji_code(emoji: List[int]):
        return "-".join(f"u{c:x}" for c in emoji)

    u1 = emoji_code(emoji1)
    u2 = emoji_code(emoji2)
    return f"{API}{date}/{u1}/{u1}_{u2}.png"

async def mix_emoji(emoji_code1, emoji_code2) ->bytes:
    emoji1 = emoji_code1
    emoji2 = emoji_code2
    if not emoji1:
        return None
    if not emoji2:
        return None

    urls: List[str] = []
    for date in dates:
        urls.append(create_url(date, emoji1, emoji2))
        urls.append(create_url(date, emoji2, emoji1))

    try:
        async with httpx.AsyncClient(
            proxies="", timeout=20
        ) as client:  # type: ignore
            for url in urls:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.content
            return None
    except Exception:

        return None

async def emojimix(m:model.GroupMsgModel):

    msg=m.getMsg()
    msg=msg.replace("/mix","").replace("/mix ","")
    em=[]
    for i in msg:
        x=find_emoji(i)
        if x!=None:
            em.append(x)

    if len(em)!=2:
        return
    print(em)
    dat:bytes=await mix_emoji(em[0],em[1])
    if len(dat)<=8:
        return
    await m.sendGroupMessage(m.CQ.Img(dat),m.getGroupid())
