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
            pass

    async def wait_till(self,t):
        while self.time < t:
            pass

class Clock:
    def __init__(self,sim_time: SimTime):
        self.sim_time = sim_time
