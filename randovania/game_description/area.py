from typing import NamedTuple, List, Dict

from randovania.game_description.node import Node, DockNode
from randovania.game_description.requirements import RequirementSet


class Area(NamedTuple):
    name: str
    area_asset_id: int
    default_node_index: int
    nodes: List[Node]
    connections: Dict[Node, Dict[Node, RequirementSet]]

    def __repr__(self):
        return "Area[{}]".format(self.name)

    def node_with_dock_index(self, dock_index: int) -> DockNode:
        for node in self.nodes:
            if isinstance(node, DockNode) and node.dock_index == dock_index:
                return node
        raise IndexError("No DockNode found with dock_index {} in {}".format(
            dock_index, self.name))
