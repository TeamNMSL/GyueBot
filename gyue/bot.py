import os
import sys
import threading
import ScheduleList
import nonebot
import gws

from nonebot.adapters.console import Adapter as ConsoleAdapter  # 避免重复命名
from nonebot.adapters.onebot.v11 import Adapter as OnebotAdapter
import gCli
import gyue.plugins.Gyue.GlobalScope as gs


def m(vcode="n"):
    os.chdir((sys.argv[0].replace("bot.py", "").replace("devStart.py", "")))
    gs.initBot()
    if vcode!="n":
        gs.set_value(gs.key_botVersionKey,vcode)
    Schedules = threading.Thread(target=ScheduleList.startThread)
    Schedules.start()
    Gws=threading.Thread(target=gws.runws)
    Gws.start()
    nbthrd = threading.Thread(target=runnb)
    nbthrd.start()
    gCli.gyueCli()

def runnb():
    # 初始化 NoneBot
    nonebot.init()

    # 注册适配器
    driver = nonebot.get_driver()
    # driver.register_adapter(ConsoleAdapter)
    driver.register_adapter(OnebotAdapter)

    # 在这里加载插件
    nonebot.load_builtin_plugins("echo")  # 内置插件
    # nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
    nonebot.load_plugins("gyue/plugins")  # 本地插件
    nonebot.run()





if __name__ == "__main__":
    m()
