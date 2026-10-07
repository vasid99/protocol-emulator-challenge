from abc import ABC,abstractmethod
from .base_block import (
    BaseBlock,
    BaseInputPort,
    BaseOutputPort,
    BaseClockPort,
    BaseClockSignal,
)
from .port_conn import (
    PortConnGraph,
)

class BaseBlockNetwork(ABC):
    def __init__(
        self,
        blocks: list[BaseBlock],
        port_conn: PortConnGraph,
    ):
        self.blocks = blocks
        self.port_conn = port_conn
    
    @abstractmethod
    @classmethod
    def generate(cls):
        raise NotImplementedError
