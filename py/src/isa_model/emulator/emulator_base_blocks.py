from .base_block import (
    BaseBlock,
    BaseInput,
    BaseOutput,
    BaseClock,
)

class ShiftRegister(BaseBlock, clock_ports=["i_clk"]):
    def __init__(self, name: str, clock: BaseClock, width: int):
        super().__init__(
            name = name,
            inputs = {
                "i_bit": BaseInput("i_bit"),
            },
            outputs = {
                "o_reg": BaseOutput("o_reg"),
            },
            clocks = {
                "i_clk": clock,
            }
        )
        self.width = width
    
    def update_comb(self):
        pass

    def update_ff_i_clk(self):
        shifted_val = self.o_reg._value << 1
        shifted_val &= ((1 << self.width) - 1)
        self.o_reg._value = shifted_val | (self.i_bit._value & 0x1)


