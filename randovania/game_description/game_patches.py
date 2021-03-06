import copy
import dataclasses
from dataclasses import dataclass
from typing import Dict, Tuple, Iterator

from randovania.game_description.area_location import AreaLocation
from randovania.game_description.dock import DockWeakness
from randovania.game_description.node import DockConnection
from randovania.game_description.resources import PickupAssignment, PickupIndex, PickupEntry, ResourceGainTuple


@dataclass(frozen=True)
class GamePatches:
    """Determines patches that are made to the game's data.
    Currently we support:
    * Swapping pickup locations
    """

    pickup_assignment: PickupAssignment
    elevator_connection: Dict[int, AreaLocation]
    dock_connection: Dict[Tuple[int, int], DockConnection]
    dock_weakness: Dict[Tuple[int, int], DockWeakness]
    extra_initial_items: ResourceGainTuple
    starting_location: AreaLocation

    @classmethod
    def with_game(cls, game: "GameDescription") -> "GamePatches":
        return GamePatches({}, {}, {}, {}, (), game.starting_location)

    def assign_new_pickups(self, assignments: Iterator[Tuple[PickupIndex, PickupEntry]]) -> "GamePatches":
        new_pickup_assignment = copy.copy(self.pickup_assignment)

        for index, pickup in assignments:
            assert index not in new_pickup_assignment
            new_pickup_assignment[index] = pickup

        return dataclasses.replace(self, pickup_assignment=new_pickup_assignment)

    def assign_pickup_assignment(self, assignment: PickupAssignment) -> "GamePatches":
        items: Iterator[Tuple[PickupIndex, PickupEntry]] = assignment.items()
        return self.assign_new_pickups(items)

    def assign_starting_location(self, location: AreaLocation) -> "GamePatches":
        return dataclasses.replace(self, starting_location=location)
