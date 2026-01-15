import json
import re
import aiohttp
import asyncio
from pathlib import Path
from typing import Dict
from bilibili_api import video
from bilibili_api.video import VideoDownloadURLDataDetecter
from gyue.extlib.bvideo.download.common import download_file_by_stream, merge_av
from nonebot.log import logger
from bilibili_api import video, live, article, Credential, select_client
import gyue.gyue.plugins.Gyue.GlobalScope as gs

BILIBILI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87",
    "referer": "https://www.bilibili.com",
}

def cookies_str_to_dict(cookies_str: str) -> Dict[str, str]:
    res = {}
    for cookie in cookies_str.split(";"):
        name, value = cookie.strip().split("=", 1)
        res[name] = value
    return res
credential: Credential | None = (None)

patterns: dict[str, re.Pattern] = {
    "BV": re.compile(r"(BV[1-9a-zA-Z]{10})(?:\s)?(\d{1,3})?"),
    "av": re.compile(r"av(\d{6,})(?:\s)?(\d{1,3})?"),
    "/BV": re.compile(r"/(BV[1-9a-zA-Z]{10})()"),
    "/av": re.compile(r"/av(\d{6,})()"),
    "b23": re.compile(r"https?://b23\.tv/[A-Za-z\d\._?%&+\-=/#]+()()"),
    "bili2233": re.compile(r"https?://bili2233\.cn/[A-Za-z\d\._?%&+\-=/#]+()()"),
    "bilibili": re.compile(
        r"https?://(?:space|www|live|m|t)?\.?bilibili\.com/[A-Za-z\d\._?%&+\-=/#]+()()"
    ),
}
async def forceParse(text: str)->str|None:

    try:
        j = json.loads(text)
        print("Loaded")
        ja=j[0]
        print(1)
        jaa=ja["data"]
        print(2)
        turl = jaa["data"]
        print(3)
        jaaa=json.loads(turl)
        print(turl)
        appurl=jaaa["meta"]["detail_1"]["qqdocurl"]
        print(appurl)
        text=appurl
    except:
        if str(ja["type"])!="text":
            return
        print("not json")
        text=ja["data"]["text"]
        pass

    # 使用正则表达式查找 &p= 后的数字
    match2 = re.search(r"&p=(\d+)", text)

    # 如果匹配到,提取数字并赋值给 page_num,否则赋值 0
    page_num = int(match2.group(1)) if match2 else 0
    #是否短链
    if "b23" in text:
        b23url = text
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    b23url, headers=BILIBILI_HEADERS, allow_redirects=False
            ) as resp:
                url = resp.headers.get("Location", b23url)
        if url == b23url:
            logger.info(f"链接 {url} 无效，忽略")
            return
    else:
        url=text
    #链接中是否包含BV，av号
    if url and (id_type := next((i for i in ("BV", "av") if i in url), None)):
        if match := patterns[id_type].search(url):
            keyword = id_type
            video_id = match.group(1)
    print(video_id)

    # 如果不是视频
    if not video_id:
        return
    # 视频
    if keyword in ("av", "/av"):
        v = video.Video(aid=int(video_id), credential=credential)
    else:
        v = video.Video(bvid=video_id, credential=credential)
    # 合并转发消息 list
    try:
        video_info = await v.get_info()
    except Exception as e:
        print("解析失败")
    video_title, video_cover, video_desc, video_duration = (
        video_info["title"],
        video_info["pic"],
        video_info["desc"],
        video_info["duration"],
    )
    # 校准 分 p 的情况
    page_num = (int(page_num) - 1) if page_num else 0
    if (pages := video_info.get("pages")) and len(pages) > 1:
        # 解析URL
        if url and (match := re.search(r"(?:&|\?)p=(\d{1,3})", url)):
            page_num = int(match.group(1)) - 1
        # 取模防止数组越界
        page_num = page_num % len(pages)
        p_video = pages[page_num]
        video_duration = p_video.get("duration", video_duration)
        if p_name := p_video.get("part").strip():
            print(f"分集标题: {p_name}")
        if first_frame := p_video.get("first_frame"):
            print(first_frame)
    else:
        page_num = 0

    try:
        prefix = f"{video_id}-{page_num}"
        video_name = f"{prefix}.mp4"
        video_path =  Path(f"{gs.path_botTmpVideoPath}/{video_name}")
        if not video_path.exists():
            download_url_data = await v.get_download_url(page_index=page_num)
            detecter = VideoDownloadURLDataDetecter(download_url_data)
            streams = detecter.detect_best_streams()
            video_stream = streams[0]
            audio_stream = streams[1]
            assert video_stream is not None
            assert audio_stream is not None
            video_url, audio_url = video_stream.url, audio_stream.url

            # 下载视频和音频
            v_path, a_path = await asyncio.gather(
                download_file_by_stream(
                    video_url, f"{prefix}-video.m4s", ext_headers=BILIBILI_HEADERS
                ),
                download_file_by_stream(
                    audio_url, f"{prefix}-audio.m4s", ext_headers=BILIBILI_HEADERS
                ),
            )
            await merge_av(v_path, a_path, video_path)
    except Exception as e:
        print(e)
        return
    return video_path