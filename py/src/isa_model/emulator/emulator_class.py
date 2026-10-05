from abc import ABC,abstractmethod
from typing import Union,Optional,Mapping

from .emulator_base_blocks import (
    Clock,
    Pin,
    ShiftRegister,
)

class Emulator:
    def __init__(
        self,
        clock: Clock = None,
        pins: Optional[Mapping[Pin]] = None,
        shregs: Optional[Mapping[ShiftRegister]] = None,
    ):
        self.clock = clock
        self.pins = pins
        self.shregs = shregs

class Instruction(ABC):
    def __init__(self,**operands):
        self.operands = operands
    
    @property
    @abstractmethod
    def latency(self):
        return 0

    @abstractmethod
    async def execute(self,em: Emulator):
        return

    async def __call__(self,em: Emulator):
        self.clock.sim_time
