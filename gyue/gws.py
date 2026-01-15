import asyncio
import threading

import websockets
import gyue.plugins.Gyue.GlobalScope as gs

def runws():
    x=threading.Thread(target=runthis)
    x.start()
    return

def runthis():
    asyncio.run(wsmain())


async def handle_connection(websocket, path):
    # 添加新连接的客户端
    gs.get_value("connected_clients").add(websocket)
    print("客户端连接:", path)
    try:
        async for message in websocket:
            print("收到消息:", message)
            # 可以发送回消息给客户端
            await websocket.send(f"收到你的消息: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print("连接关闭:", e)
    finally:
        # 移除断开的客户端
        gs.get_value("connected_clients").remove(websocket)

# 主协程，启动 WebSocket 服务器
async def wsmain():
    # 创建 WebSocket 服务器，监听端口 11451
    gs.set_value("connected_clients", set())
    while True:
        server = await websockets.serve(handle_connection, "localhost", 11451)
        print("WebSocket 服务器运行在 ws://localhost:11451")
        await server.wait_closed()
