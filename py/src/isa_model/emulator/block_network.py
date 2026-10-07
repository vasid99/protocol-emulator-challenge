from .base_block import (
    BaseBlock,
    BaseInput,
    BaseOutput,
    BaseClock,
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
