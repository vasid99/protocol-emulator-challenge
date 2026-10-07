import networkx as nx
from .base_block import (
    BaseBlock,
    BaseInput,
    BaseOutput,
    BaseClock,
)

class PortConn(nx.DiGraph):
    def _edge_ports_sanity_check(self, u_of_edge, v_of_edge):
        if u_of_edge.name not in self.nodes:
            assert isinstance(u_of_edge,BaseOutput),(
                f"expected BaseOutput as edge_from, "
                f"got {u_of_edge.__class__.__name__} "
                f"({u_of_edge})"
            )
            self.add_node(u_of_edge.name,outport=u_of_edge)
        else:
            outport = self.nodes[u_of_edge.name]["outport"]
            assert outport == u_of_edge,(
                f"attempted to assign new BaseOutput port to existing "
                f"port of same name {u_of_edge.name}"
            )
        if v_of_edge.name not in self.nodes:
            assert isinstance(v_of_edge,BaseInput),(
                f"expected BaseInput as edge_from, "
                f"got {v_of_edge.__class__.__name__} "
                f"({v_of_edge})"
            )
            self.add_node(v_of_edge.name,inport=v_of_edge)
        else:
            inport = self.nodes[v_of_edge.name]["inport"]
            assert outport == v_of_edge,(
                f"attempted to assign new BaseInput port to existing "
                f"port of same name: {v_of_edge.name}"
            )
        inport_inedges = tuple(self.in_edges[v_of_edge.name])
        assert len(inport_inedges) == 0,(
            f"attempted to assign multiple drivers to BaseInput "
            f"{inport_inedges[0][1]}. Currently driven by BaseOutput "
            f"{inport_inedges[0][0]}."
        )

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self._edge_ports_sanity_check(u_of_edge, v_of_edge)
        super().add_edge(u_of_edge.name, v_of_edge.name, **attr)
    
    def add_edges_from(self, ebunch_to_add, **attr):
        ebunch_to_add_checked = []
        for e in ebunch_to_add:
            u_of_edge = e[0]
            v_of_edge = e[1]
            self._edge_ports_sanity_check(u_of_edge, v_of_edge)
            ebunch_to_add_checked += [
                u_of_edge.name,
                v_of_edge.name,
            ] + list(e[2:])
        super().add_edges_from(ebunch_to_add_checked, **attr)
