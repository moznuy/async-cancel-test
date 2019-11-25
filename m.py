import asyncio
import logging
import random

k = 0

f = logging.Formatter('%(relativeCreated)d - %(levelname)-9s: %(message)s')
h = logging.StreamHandler()
h.setFormatter(f)
logging.root.addHandler(h)


async def factorial(n: int = 0):
    try:
        print(n, 'before')
        await asyncio.sleep(3)  # random.random() * 3 + .5
        if n == 0:
            return 1

        print(n, 'after')
        return await factorial(n - 1) * n
    except asyncio.CancelledError:
        logging.warning('Canceled factorial, lo')
        # logging.exception('')
        await asyncio.sleep(3)
        logging.warning('Canceled factorial 2, lo')
        global k
        k+=1
        raise


async def main2():
    try:
        print('MAIN !!!')
        tasks = [factorial(5) for _ in range(10)]  # random.randint(2, 5)

        g = asyncio.gather(*tasks)
        results = await g
        print(results)
    except asyncio.CancelledError:
        logging.warning('Canceled main2')
        await asyncio.sleep(3)
        logging.warning('Canceled main2 2')
        # raise


async def inter3():
    try:
        await main2()
    except asyncio.CancelledError:
        logging.warning('Canceled inter3')
        await asyncio.sleep(0.5)
        logging.warning('Canceled inter3 2')


async def inter2():
    try:
        await inter3()
    except asyncio.CancelledError:
        logging.warning('Canceled inter2')
        await asyncio.sleep(0.5)
        logging.warning('Canceled inter2 2')


async def inter1():
    try:
        await inter2()
    except asyncio.CancelledError:
        logging.warning('Canceled inter1')
        await asyncio.sleep(0.5)
        logging.warning('Canceled inter1 2')


async def main():
    try:
        t1 = asyncio.create_task(inter1())
        await asyncio.sleep(2)
        print('Canceling T1')
        t1.cancel()
        await t1
    except asyncio.CancelledError:
        logging.warning('Canceled main')
        await asyncio.sleep(3)
        logging.warning('Canceled main 2, lo')


if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
    except KeyboardInterrupt:
        print('CTRL-C')
    print(k)
