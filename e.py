import asyncio
import logging
# PYTHONASYNCIODEBUG=1
# sudo tcpkill -i lo port 8080
import aiohttp
from aiohttp import web


async def task():
    print('TASK ENTER')
    try:
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print('TASK CANCELED')
        raise
    finally:
        print('TASK EXIT')


async def read(ws):
    print('read ENTER')
    try:
        async for msg in ws:  # type: aiohttp.WSMessage
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    except asyncio.CancelledError:
        print('read CANCELED')
        raise
    finally:
        print('read EXIT')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    task1 = asyncio.create_task(task())
    task2 = asyncio.create_task(read(ws))
    try:
        await asyncio.gather(asyncio.shield(task1), asyncio.shield(task2))
        # await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        print('Canceled')
        task1.cancel()
        task2.cancel()
    finally:
        print(await asyncio.gather(task1, task2, return_exceptions=True))
        return ws

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])

web.run_app(app)
