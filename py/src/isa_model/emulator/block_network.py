from .base_block import (
    BaseBlock,
    BaseInputPort,
    BaseOutputPort,
    BaseClockPort,
    BaseClockSignal,
)
from .port_conn import (
    PortConn
)

class BlockNetwork:
    def __init__(
        self,
        blocks: list[BaseBlock],
        port_conn: PortConn,
    ):
        self.blocks = blocks
        self.port_conn = port_conn
