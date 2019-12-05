import asyncio

# %(relativeCreated)d
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(relativeCreated)5d] %(levelname)6s [%(name)-8s.%(funcName)10s:%(lineno)-5d] %(message)s", # asctime
    datefmt="%H:%M:%S"
)


async def task():
    try:
        logging.info('TASK Enter')
        await asyncio.sleep(3)
    except asyncio.CancelledError:
        logging.error('TASK Canceled')
        # raise AttributeError()
        raise
    finally:
        logging.info('TASK end')


async def main2():
    while True:
        try:
            logging.info('main2 Awating')
            await task()

            # print(await asyncio.gather(*tasks, return_exceptions=True))
        except asyncio.CancelledError:
            logging.error('main2 Canceled')
            break
            # print(await tasks[0])
            # raise
    logging.info('main2 END')



async def main():
    task = asyncio.create_task(main2())
    await asyncio.sleep(10)
    task.cancel()
    await task

if __name__ == '__main__':
    try:
        # asyncio.run(main(), debug=True)
        #
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(main())
        # loop.run_until_complete(asyncio.sleep(2))
        loop.close()
    except KeyboardInterrupt:
        pass
    finally:
        import gc
        gc.collect()
