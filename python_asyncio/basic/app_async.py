import asyncio
import time


async def count():
    await asyncio.sleep(1)
    print('1')
    await asyncio.sleep(1)
    print('2')
    await asyncio.sleep(1)
    print('3')


async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    stop = time.perf_counter()
    print(f'Total time: {stop - start}')

