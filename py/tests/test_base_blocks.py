from src.isa_model.emulator.base_block import (
    BaseClock,
    BaseInput,
    BaseOutput,
    BaseBlock,
)
import pytest
import random

class Adder(BaseBlock):
    def __init__(self, width: int):
        self.width = width
        super().__init__(
            {
                "a": BaseInput("a"),
                "b": BaseInput("b"),
                "cin": BaseInput("cin"),
            },
            {
                "s": BaseOutput("s"),
                "cout": BaseOutput("c"),
            },
        )

    def update_comb(self):
        s = 0
        c_i = (self.cin._value & 0x1)
        for i in range(self.width):
            a_i = ((self.a._value >> i) & 0x1)
            b_i = ((self.b._value >> i) & 0x1)
            s |= (a_i ^ b_i ^ c_i) << i
            c_i = (a_i & b_i) | (b_i & c_i) | (c_i & a_i)
        self.s = s
        self.cout = c_i

def test_adder():
    w = 4
    add = Adder(width=w)
    for i in range(100):
        a = random.randrange(1<<w)
        b = random.randrange(1<<w)
        cin = random.randrange(1<<1)
        sum = a + b + cin

        add.a.value = a
        add.b.value = b
        add.cin.value = cin
        add.update_comb()

        assert add.s == sum & ((1 << add.width) - 1)
        assert add.cout == sum >> add.width & 0x1

class Counter(BaseBlock,clock_ports = ["clk"]):
    def __init__(self, width: int):
        self.width = width

        inputs = {
            "reset": BaseInput("reset"),
        }
        outputs = {
            "ctr": BaseOutput("ctr"),
        }
        clocks = {
            "clk": BaseClock("clk",1),
        }
        super().__init__(inputs,outputs,clocks)
    
    def update_comb(self):
        pass

    def update_ff_clk(self):
        self.ctr._value = 0 if self.reset._value else (self.ctr._value+1) & ((1<<self.width)-1)

def test_counter():
    w = 4
    ctr = Counter(width=w)
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
