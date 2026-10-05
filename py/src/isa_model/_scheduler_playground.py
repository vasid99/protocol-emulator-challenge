import asyncio
import time

class Timer():
    def __init__(self):
        self.time = 0
    
    async def tick(self):
        await asyncio.sleep(0)
        self.time += 1

async def wait_for(T,t):
    ti = T.time
    while not T.time >= ti+t:
        await asyncio.sleep(0)
    print("done")

async def main():
    T = Timer()
    ts = asyncio.create_task(wait_for(T,6))
    for i in range(10):
        await T.tick()
        print(T.time)

asyncio.run(main())
