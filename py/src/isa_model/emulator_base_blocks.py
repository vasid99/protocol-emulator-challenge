import asyncio

# reference: https://github.com/ianphil/pyRoute13/blob/master/docs/coroutine_simulation_tutorial.md

class SimTime:
    # allowed_time_steps = {
    #     's' : 1,
    #     'ms': 1e-3,
    #     'us': 1e-6,
    #     'ns': 1e-9,
    #     'ps': 1e-12,
    #     'fs': 1e-15,
    # }

    def __init__(self, time_step: int = 1, time_res = None):
        assert time_step > 0,(
            f"expected positive number for time step,"
            " got {time_step}"
        )
        self.time_step = time_step
        self.time_res = time_res
        self.reset()
    
    def reset(self):
        self.time = 0

    def tick(self):
        self.time += self.time_step

    async def wait_for(self,t):
        t_curr = self.time
        while self.time < (t_curr+t):
            await asyncio.sleep(0)

    async def wait_till(self,t):
        while self.time < t:
            await asyncio.sleep(0)
    
    @classmethod
    async def _unit_test_1(cls):
        sim_time = cls()
        async def coro1():
            await sim_time.wait_for(1)
            print("Wait for 1 done")
            await sim_time.wait_for(2)
            print("Wait for 2 done")
            await sim_time.wait_till(6)
            print("Wait till 6 done")
        async def coro2():
            print(f"time = {sim_time.time}")
            for i in range(7):
                await asyncio.sleep(sim_time.time_step)
                sim_time.tick()
                print(f"time = {sim_time.time}")
        t1 = asyncio.create_task(coro1(),)
        t2 = asyncio.create_task(coro2(),)
        await t1
        await t2

class Clock:
    def __init__(self,sim_time: SimTime):
        self.sim_time = sim_time

if __name__ == '__main__':
    asyncio.run(SimTime._unit_test_1())

