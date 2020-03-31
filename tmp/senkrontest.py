import asyncio
import time

loop = asyncio.get_event_loop()


async def count():
    print("One")
    await asyncio.sleep(2)
    print("Two")

async def main():
    task=asyncio.gather(count())
    time.sleep(5)
    print('bbb')
    await task

if __name__ == "__main__":

    s = time.perf_counter()
    loop.run_until_complete(main())

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    exit()