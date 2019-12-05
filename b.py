import asyncio


async def task(i):
    try:
        print(f'{i}')
        await asyncio.sleep(6)
    except asyncio.CancelledError:
        print(f'Canceled {i}')
        # raise AttributeError()
        raise
    finally:
        print('end')


async def main2():
    try:
        tasks = [asyncio.create_task(task(i)) for i in range(2)]
        await asyncio.sleep(1.5)

        print('Awating')
        # print(await asyncio.gather(*tasks, return_exceptions=True))
    except asyncio.CancelledError:
        print('Canceled main')
        (asyncio.gather(*tasks, return_exceptions=True)).cancel()
        # print(await tasks[0])
        # raise


async def main():
    task = asyncio.create_task(main2())
    await asyncio.sleep(1)
    task.cancel()
    await task

if __name__ == '__main__':
    try:
        # asyncio.run(main(), debug=True)
        #
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(2))
        loop.close()
    except KeyboardInterrupt:
        pass
    finally:
        import gc
        gc.collect()
