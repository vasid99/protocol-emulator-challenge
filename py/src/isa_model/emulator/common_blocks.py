from .base_block import (
    BaseBlock,
    BaseInputPort,
    BaseOutputPort,
    BaseClockPort,
    BaseClockSignal,
)

class Adder(BaseBlock):
    def __init__(self, name: str, width: int):
        super().__init__(
            name = name,
            inputs = [
                BaseInputPort("a"),
                BaseInputPort("b"),
                BaseInputPort("cin"),
            ],
            outputs = [
                BaseOutputPort("s"),
                BaseOutputPort("cout"),
            ],
        )
        self.width = width

    def update_comb(self):
        s = 0
        c_i = (self.cin._value & 0x1)
        for i in range(self.width):
            a_i = ((self.a._value >> i) & 0x1)
            b_i = ((self.b._value >> i) & 0x1)
            s |= (a_i ^ b_i ^ c_i) << i
            c_i = (a_i & b_i) | (b_i & c_i) | (c_i & a_i)
        self.s._value = s
        self.cout._value = c_i

class Counter(BaseBlock,clock_ports = ["clk"]):
    def __init__(
        self,
        name: str,
        width: int,
        clock: BaseClockSignal,
    ):
        inputs = [
            BaseInputPort("reset"),
        ]
        outputs = [
            BaseOutputPort("ctr"),
        ]
        clocks = [
            BaseClockPort("clk",clock),
        ]
        super().__init__(
            name = name,
            inputs = inputs,
            outputs = outputs,
            clocks = clocks,
        )
        self.width = width

    def update_comb(self):
        pass

    def update_ff_clk(self):
        self.ctr._value = (
            0 if self.reset._value else 
            (self.ctr._value+1) & ((1<<self.width)-1)
        )
