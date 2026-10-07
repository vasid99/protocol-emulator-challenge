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

    @property
    def value(self):
        return self._value

class BaseBlock(ABC):
    def __init__(
        self,
        inputs: dict[str,BaseInput],
        outputs: dict[str,BaseOutput],
        clocks: dict[str,BaseClock] = {},
    ):
        for cname in self._clock_ports:
            c = clocks[cname]
            assert isinstance(c,BaseClock),f"expected BaseClock datatype, got: {c.__class__.__name__}"
            setattr(self,cname,c)
        for iname,i in inputs.items():
            assert isinstance(i,BaseInput),f"expected BaseInput datatype, got: {i.__class__.__name__}"
            setattr(self,iname,i)
        for oname,o in outputs.items():
            assert isinstance(o,BaseOutput),f"expected BaseOutput datatype, got: {o.__class__.__name__}"
            setattr(self,oname,o)

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
