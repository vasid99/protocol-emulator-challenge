import networkx as nx
from .base_block import (
    BaseBlock,
    BaseInputPort,
    BaseOutputPort,
    BaseClockPort,
    BaseClockSignal,
)
from queue import Queue

class PortConnGraph(nx.DiGraph):
    allowed_edge_types = {
        "clk": (BaseClockSignal,BaseClockPort),
        "wire": (BaseOutputPort,BaseInputPort),
    }
    def _edge_ports_sanity_check(self, u_of_edge, v_of_edge):
        edge_types = (
            type(u_of_edge),
            type(v_of_edge),
        )
        edge_type_key = None
        for ek,ev in self.allowed_edge_types.items():
            if edge_types == ev:
                edge_type_key = ek
                break
        else:
            raise TypeError(
                f"expected edge types as "
                f"one of {self.allowed_edge_types}, "
                f"found {edge_types}."
            )
        if u_of_edge.qname not in self.nodes:
            self.add_node(
                u_of_edge.qname,
                outport=u_of_edge,
                kpn_fifo=Queue(),
            )
        else:
            outport = self.nodes[u_of_edge.qname]["outport"]
            assert outport == u_of_edge,(
                f"attempted to assign new {type(u_of_edge).__name__} "
                f"port to existing port of same name {u_of_edge.qname}"
            )
        if v_of_edge.qname not in self.nodes:
            # TODO add BaseClockPort support
            self.add_node(
                v_of_edge.qname,
                inport=v_of_edge,
                kpn_fifo=Queue(),
            )
        else:
            inport = self.nodes[v_of_edge.qname]["inport"]
            assert inport == v_of_edge,(
                f"attempted to assign new {type(v_of_edge).__name__} "
                f"port to existing port of same name {v_of_edge.qname}"
            )

            # multiple driver check
            inport_inedges = tuple(self.in_edges[v_of_edge.qname])
            assert len(inport_inedges) == 0,(
                f"attempted to assign multiple drivers to "
                f"{type(v_of_edge).__name__} port: "
                f"{inport_inedges[0][1]}."

                f"\nCurrently driven by "
                f"{type(u_of_edge).__name__} port: "
                f"{inport_inedges[0][0]}."
            )

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self._edge_ports_sanity_check(u_of_edge, v_of_edge)
        super().add_edge(u_of_edge.qname, v_of_edge.qname, **attr)
    
    def add_edges_from(self, ebunch_to_add, **attr):
        ebunch_to_add_checked = []
        for e in ebunch_to_add:
            u_of_edge = e[0]
            v_of_edge = e[1]
            self._edge_ports_sanity_check(u_of_edge, v_of_edge)
            ebunch_to_add_checked += [
                u_of_edge.qname,
                v_of_edge.qname,
            ] + list(e[2:])
        super().add_edges_from(ebunch_to_add_checked, **attr)
