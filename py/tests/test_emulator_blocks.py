from src.isa_model.emulator.base_block import BaseClockSignal
from src.isa_model.emulator.emulator_blocks import ShiftRegister
import random

def test_shift_register():
    w = 8
    clk = BaseClockSignal("clk",1)
    sr = ShiftRegister(name = "I_shift_reg",clock = clk, width = w)
    sr_ref = [0]*w
    for i in range(100):
        b = random.randrange(1<<1)
        sr.i_bit.value = b
        sr.update_ff_i_clk()
        sr_ref.insert(0,b)
        sr_ref.pop()
        sr_ref_val = sum([b<<i for i,b in enumerate(sr_ref)])
        assert sr.o_reg.value == sr_ref_val

