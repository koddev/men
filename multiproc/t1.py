import asyncio
import time


async def hold(seconds):
    print(f'Waiting {seconds} seconds...')
    time.sleep(seconds)
    # await asyncio.sleep(seconds)


def run(a):
    yield 5*a

async def main():
    await asyncio.gather(
        run(1),
        run(2),
        run(3),
    )


asyncio.run(main())

# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
# async def main():
#     print(f"started at {time.strftime('%X')}")
#     await say_after(1, 'hello')
#     await say_after(2, 'world')
#     print(f"finished at {time.strftime('%X')}")
#
#
# asyncio.run(main())
