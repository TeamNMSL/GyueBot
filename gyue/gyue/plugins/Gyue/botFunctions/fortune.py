import datetime
import random
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model


def __calcUserFortune(uid:int)->list:
    a:list=[]
    d = datetime.date.today()
    sapd = d.year * 10000 + d.month * 100 + d.day
    random.seed(uid * 7 + sapd)
    total=random.randint(0,100)
    sub=random.randint(0,total)
    f1=total-sub
    total=total-sub
    sub=random.randint(0,total)
    f2 = total - sub
    total = total - sub
    f3=total
    a.append(f1*3)
    a.append(f2*3)
    a.append(f3*3)
    return a
def calcUserFortune(uid:int,d:datetime)->list:
    a:list=[]
    sapd = d.year * 10000 + d.month * 100 + d.day
    random.seed(uid * 7 + sapd)
    total=random.randint(0,100)
    a.append(total)
    a.append(total)
    a.append(total)
    return a
async def _fortune(m:model.GroupMsgModel)->bool:
    fortuneList:list=_calcUserFortune(int(m.getUserid()))
    s=generateSummary(fortuneList)
    r=m.CQ.At(m.getUserid())+m.CQ.Img(f"{gs.path_botImgFortuneDir}/{s}.jpg")+f"[今日运势]\n财运:{fortuneList[0]}\n桃花运:{fortuneList[1]}\n事业运:{fortuneList[2]}\n点评:{s}"
    await m.sendGroupMessage(r,m.getGroupid())
    return True
async def fortune(m:model.GroupMsgModel)->bool:
    fortuneList:list=calcUserFortune(int(m.getUserid()),datetime.date.today())
    s=generateSummary(fortuneList)
    r=m.CQ.At(m.getUserid())+m.CQ.Img(f"{gs.path_botImgFortuneDir}/{s}.jpg")+f"[今日运势]\n运势值: {getAvg(fortuneList)}\n点评:{s}"
    await m.sendGroupMessage(r,m.getGroupid())
    return True
async def ystdFortune(m:model.GroupMsgModel)->bool:
    fortuneList:list=calcUserFortune(int(m.getUserid()),datetime.date.today()-datetime.timedelta(days=1))
    s=generateSummary(fortuneList)
    r=m.CQ.At(m.getUserid())+m.CQ.Img(f"{gs.path_botImgFortuneDir}/{s}.jpg")+f"[昨日运势]\n运势值: {getAvg(fortuneList)}\n点评:{s}"
    await m.sendGroupMessage(r,m.getGroupid())
    return True
async def tmrFortune(m:model.GroupMsgModel)->bool:
    fortuneList:list=calcUserFortune(int(m.getUserid()),datetime.date.today()+datetime.timedelta(days=1))
    s=generateSummary(fortuneList)
    r=m.CQ.At(m.getUserid())+m.CQ.Img(f"{gs.path_botImgFortuneDir}/{s}.jpg")+f"[明日运势]\n运势值: {getAvg(fortuneList)}\n点评:{s}"
    await m.sendGroupMessage(r,m.getGroupid())
    return True
async def sbFortune(m:model.GroupMsgModel)->bool:
    ystI=0
    tmrI=0
    dayK=1
    for i in m.getMsg():
        if i=="昨":
            ystI+=dayK
            dayK=1
        elif i=="明":
            tmrI+=dayK
            dayK=1
        elif i=="前":
            ystI+=1+dayK
            dayK=1
        elif i=="后":
            tmrI+=1+dayK
            dayK=1
        elif i=="大":
            dayK+=1

    k=tmrI-ystI
    fortuneList:list=calcUserFortune(int(m.getUserid()),datetime.date.today()+datetime.timedelta(days=k))
    s=generateSummary(fortuneList)
    r=m.CQ.At(m.getUserid())+m.CQ.Img(f"{gs.path_botImgFortuneDir}/{s}.jpg")+f"[{m.getMsg()}]\n运势值: {getAvg(fortuneList)}\n点评:{s}"
    await m.sendGroupMessage(r,m.getGroupid())
    return True
def _calcUserFortune(uid:int)->list:
    a:list=[]
    d=datetime.date.today()
    sapd=d.year*10000+d.month*100+d.day
    random.seed(uid*7+sapd)
    a.append(random.randint(0,100))
    random.seed(uid * 5+sapd)
    a.append(random.randint(0, 100))
    random.seed(uid * 2+sapd)
    a.append(random.randint(0, 100))
    return a


def getAvg(fL)->int:
    return int((fL[0]+fL[1]+fL[2])/3)


def generateSummary(fL:list)->str:
    avg:int=getAvg(fL)
    if avg==100:
        return "急麻了"
    elif avg>=90:
        return "大吉"
    elif avg>=75:
        return "吉"
    elif avg>=50:
        return "中吉"
    elif avg>=25:
        return "末吉"
    elif avg>=10:
        return "凶"
    elif avg>0:
        return "寄"
    elif avg==0:
        return "寄麻了"