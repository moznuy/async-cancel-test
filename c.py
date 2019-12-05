import asyncio
import contextvars
import gc
import logging
import warnings
import aiotask_context as context
import aiohttp
from aiohttp import WSMessage

client_addr_var = contextvars.ContextVar('client_addr')


class NeedClose:
    def __init__(self):
        self._closed = None

    async def __aenter__(self):
        self._closed = False
        return self

    # def __await__(self):
    #     return

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._closed = True
        print('exit')

    def __del__(self):
        if self._closed is not None and not self._closed:
            logging.warning('NeedClose has not been closed properly')


def render_goodbye():
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.

    client_addr = client_addr_var.get()
    return f'Good bye, client @ {client_addr}\n'.encode()


async def handle_request(reader, writer):
    addr = writer.transport.get_extra_info('socket').getpeername()
    client_addr_var.set(addr)

    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break
        writer.write(line)

    writer.write(render_goodbye())
    writer.close()


async def main4():
    await asyncio.sleep(0.5)
    raise asyncio.CancelledError


def main3(f):
    async def wraps(*args, **kwargs):
        nc = context.get('lol')

        async with nc:
            await main4()
    return wraps


@main3
async def k():
    pass



async def main2():
    context.set('lol', NeedClose())
    try:
        await asyncio.gather(k(), asyncio.sleep(2))
    except asyncio.CancelledError:
        pass


# ws = None
# cs = None


async def main_t():
    # global cs
    async with aiohttp.ClientSession() as session:
        # async with session.ws_connect('wss://echo.websocket.org') as ws:
            ws = await session.ws_connect('wss://echo.websocket.org')
            # cs = session

            await ws.send_str('Lol!')
            await ws.send_str('Lol!')
            await ws.send_str('Lol!')
            try:
                async for msg in ws:  # type: WSMessage
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(msg.data)
            except asyncio.CancelledError:
                print('Canceled')
                # session._connector = None
                # raise

    gc.collect()




async def main():
    t = asyncio.create_task(main_t())
    await asyncio.sleep(6)
    t.cancel()
    await t



if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        pass

# To test it you can use telnet:
#     telnet 127.0.0.1 8081
