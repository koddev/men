import asyncio
import time


async def hold(seconds):
    print(f'Waiting {seconds} seconds...')
    time.sleep(seconds)
    # await asyncio.sleep(seconds)


async def get_chat_id(name):
    await asyncio.sleep(3)
    return "chat-%s" % name




async def main():
    s=time.time()

    task = asyncio.create_task(get_chat_id('aa'))
    await asyncio.sleep(3)
    res=await task
    print(res)
    print(time.time()-s)
    # await asyncio.gather(
    #     hold(1),
    #     hold(2),
    #     hold(3),
    # )


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
