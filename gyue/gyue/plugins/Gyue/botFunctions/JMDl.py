import asyncio
import threading

import jmcomic, os, time, yaml
import py7zr
import pyminizip
from PIL import Image
from jmcomic import JmOption
import gyue.gyue.plugins.Gyue.GlobalScope as gs
import gyue.gyue.plugins.Gyue.handles.Models.GroupMsgModel as model

def all2PDF(input_folder, pdfpath, pdfname):
    start_time = time.time()
    paht = input_folder
    zimulu = []  # 子目录（里面为image）
    image = []  # 子目录图集
    sources = []  # pdf格式的图

    with os.scandir(paht) as entries:
        for entry in entries:
            if entry.is_dir():
                zimulu.append(int(entry.name))
    # 对数字进行排序
    zimulu.sort()

    for i in zimulu:
        with os.scandir(paht + "/" + str(i)) as entries:
            for entry in entries:
                if entry.is_dir():
                    print("这一级不应该有自录")
                if entry.is_file():
                    image.append(paht + "/" + str(i) + "/" + entry.name)

    if "jpg" in image[0]:
        output = Image.open(image[0])
        image.pop(0)

    for file in image:
        if "jpg" in file:
            img_file = Image.open(file)
            if img_file.mode == "RGB":
                img_file = img_file.convert("RGB")
            sources.append(img_file)

    pdf_file_path = pdfpath + "/" + pdfname
    if pdf_file_path.endswith(".pdf") == False:
        pdf_file_path = pdf_file_path + ".pdf"
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    end_time = time.time()
    run_time = end_time - start_time
    print("运行时间：%3.2f 秒" % run_time)

def getJMOpt() -> 'JmOption':
    return JmOption.construct({
    'version':'2.0',
    'dir_rule':{
        'base_dir':gs.path_botJMdl,
        'rule':'Bd_Aid_Pindex'
    },
    #'client':{
    #    'domain':[
    #        '18comic.vip',
    #        '18comic.org'
    #    ]
    #},
    'download':{
        'cache':True,
        'image':{
            'decode':True,
            'suffix':".jpg"
        },
        'threading':{
            'batch_count':50
        }
    }
})

def dl(mid:str):
    jmopt=getJMOpt()
    pth=f"{gs.path_botJMdl}/{mid}"
    if os.path.exists(f"{gs.path_botJMdl}/{mid}.pdf"):
        return f"{gs.path_botJMdl}/{mid}.pdf"
    else:
        jmcomic.download_album(mid, jmopt)
        all2PDF(pth, gs.path_botJMdl, f"{mid}.pdf")

def process(e:model.GroupMsgModel):
    t=threading.Thread(target=thread_worker,kwargs={"e":e})
    t.start()
def thread_worker(e):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process1(e))
    loop.close()

def sendmsg(e,msg):
    t=threading.Thread(target=sendmsgasio,kwargs={"e":e,"msg":msg})
    t.start()

def sendmsgasio(e,msg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(e.sendGroupMessage(msg, e.getGroupid()))
    loop.close()
async def process1(e:model.GroupMsgModel):
    print('getjm')
    m=e.getMsg()
    v=m.split(" ")
    if v[0]=='/jm':
        return
    password='114514'
    if len(v) > 3:
        return
    if len(v)==3 and m.startswith("/xjm"):
        password=v[2]
    if not(m.startswith("/xjm")):
        return
    if len(v)<2:
        return
    mid=v[1]
    pdffile= f"{gs.path_botJMdl}/{mid}.pdf"
    sendmsg(e,f"正在把{mid}端到群里")
    output_zip = f"{pdffile}-{password}.7z"
    try:
        if not os.path.exists(pdffile):
            print(f"不存在{pdffile}")
            dl(mid)
        sendmsg(e,f"{mid}下载成功，正在压缩并为你端上来（文件越大等越久，密码为横线后内容）")
        input_file = pdffile
        cp7z(input_file,output_zip,password)

    except(e):
        await e.sendGroupMessage(f"出现了异常，没法端过来", e.getGroupid())
        print(e)
        return
    await e.uploadFile(output_zip, f"{mid}.pdf-{password}.7z", e.getGroupid())
    return

def cp7z(input_path, output_7z, password):
    #检查输入文件或目录是否存在
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件或目录 {input_path} 不存在！")
    # 创建 7z 压缩文件，并设置密码
    with py7zr.SevenZipFile(output_7z, 'w', password=password) as archive:
        # 如果是目录，将整个目录都压缩进7z；如果是文件，添加该文件
        if os.path.isdir(input_path):
            # 目录压缩时可以指定在压缩包内的根目录名称，这里用 os.path.basename 获取目录名
            archive.writeall(input_path, arcname=os.path.basename(input_path))
        else:
            # 对于单个文件，arcname 指定存储在压缩包内的名称
            archive.write(input_path, arcname=os.path.basename(input_path))
    print(f"压缩成功：{output_7z}")