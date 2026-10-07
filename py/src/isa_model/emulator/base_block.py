from functools import partial
from dataclasses import dataclass,field
from abc import ABC,abstractmethod
from typing import Optional

@dataclass
class BaseClockSignal:
    name: str
    period: int
    start: int = 0

class BasePort:
    def __init__(self, name: str):
        self.name = name
        self._value = 0
        self._block = None

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, value):
        assert self.block is None,(
            f"attempted to assign multiple blocks"
            f" to input {self.name}.\n"

            f"Existing block: {self.block.name}\n"
            f"Attempted block: {value.name}\n"
        )
        self._block = value

class BaseClockPort(BasePort):
    def __init__(self,
        name: str,
        sig: BaseClockSignal,
    ):
        super().__init__(name)
        self.sig = sig

class BaseInputPort(BasePort):
    @partial(property,None)
    def value(self,val):
        self._value = val

class BaseOutputPort(BasePort):
    @property
    def value(self):
        return self._value

class BaseBlock(ABC):
    def __init__(
        self,
        name: str,
        inputs: list[BaseInputPort],
        outputs: list[BaseOutputPort],
        clocks: Optional[list[BaseClockPort]] = None,
    ):
        self.name = name
        self.inputs = {i.name:i for i in inputs}
        self.outputs = {o.name:o for o in outputs}
        _clocks = clocks
        if _clocks is None:
            _clocks = {}
        clocks_d = {c.name:c for c in _clocks}
        self.clocks = {}
        for cname in self._clock_ports:
            c = clocks_d[cname]
            self.clocks[cname] = c
            assert isinstance(c,BaseClockPort),(
                f"expected BaseClockPort datatype, "
                f"got: {c.__class__.__name__}"
            )
            setattr(self,cname,c)
            c.block = self
        for iname,i in self.inputs.items():
            assert isinstance(i,BaseInputPort),(
                f"expected BaseInputPort datatype, "
                f"got: {i.__class__.__name__}"
            )
            setattr(self,iname,i)
            i.block = self
        for oname,o in self.outputs.items():
            assert isinstance(o,BaseOutputPort),(
                f"expected BaseOutputPort datatype, "
                f"got: {o.__class__.__name__}"
            )
            setattr(self,oname,o)
            o.block = self
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
