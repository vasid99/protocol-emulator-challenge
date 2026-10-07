from functools import partial
from dataclasses import dataclass,field
from abc import ABC,abstractmethod

@dataclass
class BaseClock:
    name: str
    period: int
    start: int = 0

class BaseInput:
    def __init__(self, name: str):
        self.name = name
        self._value = 0

    @partial(property,None)
    def value(self,val):
        self._value = val

class BaseOutput:
    def __init__(self, name: str):
        self.name = name
        self._value = 0
        self.block = None
    
    def _assign_driver_block(self, block):
        assert self.block is None,(
            f"attempted to assign multiple drivers"
            f" to output {self.name}"
        )
        self.block = block

    @property
    def value(self):
        return self._value

class BaseBlock(ABC):
    def __init__(
        self,
        name: str,
        inputs: dict[str,BaseInput],
        outputs: dict[str,BaseOutput],
        clocks: dict[str,BaseClock] = {},
    ):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.clocks = {}
        for cname in self._clock_ports:
            c = clocks[cname]
            self.clocks[cname] = c
            assert isinstance(c,BaseClock),(
                f"expected BaseClock datatype, "
                f"got: {c.__class__.__name__}"
            )
            setattr(self,cname,c)
        for iname,i in inputs.items():
            assert isinstance(i,BaseInput),(
                f"expected BaseInput datatype, "
                f"got: {i.__class__.__name__}"
            )
            setattr(self,iname,i)
        for oname,o in outputs.items():
            assert isinstance(o,BaseOutput),(
                f"expected BaseOutput datatype, "
                f"got: {o.__class__.__name__}"
            )
            setattr(self,oname,o)
            o._assign_driver_block(self)
        self._run_setattr_checks = True

    def __setattr__(self,name,value):
        if getattr(self,"_run_setattr_checks",None) is True:
            assert name not in self.inputs,(
                f"cannot set input {name}, try setting {name}.value."
            )
            assert name not in self.outputs,(
                f"cannot set output {name}."
            )
            assert name not in self.clocks,(
                f"cannot set clock {name}."
            )
        super().__setattr__(name,value)

    @abstractmethod
    def update_comb(self):
        raise NotImplementedError

    def __init_subclass__(
        cls,
        clock_ports: list[str] = [],
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)
        cls._clock_ports = clock_ports

        @abstractmethod
        def update_ff_abstract(self):
            raise NotImplementedError
        
        for clk in clock_ports:
            if getattr(cls,f"update_ff_{clk}",None) is None:
                setattr(cls,f"update_ff_{clk}",update_ff_abstract)
