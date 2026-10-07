from src.isa_model.emulator.base_block import (
    BaseClockPort,
    BaseInputPort,
    BaseOutputPort,
    BaseBlock,
    BaseClockSignal,
)
from src.isa_model.emulator.common_blocks import Adder,Counter
import pytest
import random

def test_adder():
    w = 4
    add = Adder("I_adder",width=w)
    for i in range(100):
        a = random.randrange(1<<w)
        b = random.randrange(1<<w)
        cin = random.randrange(1<<1)
        sum = a + b + cin

        add.a.value = a
        add.b.value = b
        add.cin.value = cin
        add.update_comb()

        assert add.s.value == sum & ((1 << add.width) - 1)
        assert add.cout.value == sum >> add.width & 0x1

def test_counter():
    w = 4
    ctr = Counter("I_ctr",width=w,clock=BaseClockSignal("clk",1))
    ctr_val = 0
    
    for i in range(20):
        ctr.update_ff_clk()
        ctr_val = (ctr_val+1) & ((1<<ctr.width)-1)
        assert ctr.ctr.value == ctr_val
    
    ctr.reset.value = 1
    ctr.update_ff_clk()
    ctr.reset.value = 0
    ctr_val = 0
    assert ctr.ctr.value == ctr_val
    
    for i in range(20):
        ctr.update_ff_clk()
        ctr_val = (ctr_val+1) & ((1<<ctr.width)-1)
        assert ctr.ctr.value == ctr_val
