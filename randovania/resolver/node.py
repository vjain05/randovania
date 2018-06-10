from typing import NamedTuple, Iterator, Tuple, Union

from randovania.resolver.dock import DockWeakness
from randovania.resolver.game_patches import GamePatches
from randovania.resolver.resources import PickupIndex, ResourceDatabase, ResourceInfo, ResourceType


class GenericNode(NamedTuple):
    name: str
    heal: bool
    index: int


class DockNode(NamedTuple):
    name: str
    heal: bool
    dock_index: int
    connected_area_asset_id: int
    connected_dock_index: int
    dock_weakness: DockWeakness


class TeleporterNode(NamedTuple):
    name: str
    heal: bool
    destination_world_asset_id: int
    destination_area_asset_id: int
    teleporter_instance_id: int


class PickupNode(NamedTuple):
    name: str
    heal: bool
    pickup_index: PickupIndex

    def __deepcopy__(self, memodict):
        return PickupNode(self.name, self.heal, self.pickup_index)

    def resource(self, resource_database: ResourceDatabase) -> ResourceInfo:
        return self.pickup_index

    def resource_gain_on_collect(self,
                                 resource_database: ResourceDatabase,
                                 game_patches: GamePatches
                                 ) -> Iterator[Tuple[ResourceInfo, int]]:
        yield self.resource(resource_database), 1

        new_index = game_patches.pickup_mapping[self.pickup_index.index]
        yield from resource_database.pickups[new_index].resource_gain(resource_database)


class EventNode(NamedTuple):
    name: str
    heal: bool
    event_index: int

    def resource(self, resource_database: ResourceDatabase) -> ResourceInfo:
        return resource_database.get_by_type_and_index(ResourceType.EVENT, self.event_index)

    def resource_gain_on_collect(self,
                                 resource_database: ResourceDatabase,
                                 game_patches: GamePatches
                                 ) -> Iterator[Tuple[ResourceInfo, int]]:
        yield self.resource(resource_database), 1


ResourceNode = Union[PickupNode, EventNode]
Node = Union[GenericNode, DockNode, TeleporterNode, ResourceNode]


def is_resource_node(node: Node):
    return isinstance(node, (PickupNode, EventNode))