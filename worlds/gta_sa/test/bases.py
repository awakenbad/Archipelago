from argparse import Namespace

from BaseClasses import CollectionState, MultiWorld
from test.bases import WorldTestBase
from worlds.AutoWorld import call_all


from ..branches import branch_of, effective_requirement
from ..items import (
    HORSESHOES_UNLOCK_ITEM,
    OYSTERS_UNLOCK_ITEM,
    PROGRESSIVE_BRANCH_ITEMS,
    STREET_RACES_ITEM,
    SUBMISSION_UNLOCK_ITEMS,
    TAGS_UNLOCK_ITEM,
)
from ..mission_list import get_start_index
from ..world import GTASAWorld

ELIGIBLE_UNLOCKS = set(SUBMISSION_UNLOCK_ITEMS) | {
    STREET_RACES_ITEM, TAGS_UNLOCK_ITEM, OYSTERS_UNLOCK_ITEM, HORSESHOES_UNLOCK_ITEM,
}

GEN_STEPS = ("generate_early", "create_regions", "create_items", "set_rules")

def generate(options: dict, seed: int, passthrough: dict | None = None) -> MultiWorld:
    multiworld = MultiWorld(1)
    multiworld.game = {1: GTASAWorld.game}
    multiworld.player_name = {1: "Tester1"}
    multiworld.set_seed(seed)

    args = Namespace()
    for key, option in GTASAWorld.options_dataclass.type_hints.items():
        setattr(args, key, {1: option.from_any(options.get(key, option.default))})
    multiworld.set_options(args)
    multiworld.state = CollectionState(multiworld)

    if passthrough is not None:
        multiworld.re_gen_passthrough = {GTASAWorld.game: passthrough}

    for step in GEN_STEPS:
        call_all(multiworld, step)
    return multiworld

class GTASATestBase(WorldTestBase):
    game = "Grand Theft Auto: San Andreas"
    world: GTASAWorld

    options = {"starting_unlock": False}

    def collect_mission_requirement(self, mission_id: int, hold_back: str | None = None) -> None:
        requirement = effective_requirement(mission_id, get_start_index(self.world))
        for branch, count in requirement.items():
            items = self.get_items_by_name(PROGRESSIVE_BRANCH_ITEMS[branch])
            take = count - (1 if branch == hold_back else 0)
            for item in items[:take]:
                self.multiworld.state.collect(item)

    def assert_branch_gated(self, location_name: str, mission_id: int) -> None:
        location = self.world.get_location(location_name)
        requirement = effective_requirement(mission_id, get_start_index(self.world))
        own_branch = branch_of(mission_id)

        self.collect_mission_requirement(mission_id, hold_back=own_branch)
        if own_branch in requirement:
            self.assertFalse(location.can_reach(self.multiworld.state),
                             f"{location_name} reachable one {own_branch} item short")
            final = self.get_items_by_name(PROGRESSIVE_BRANCH_ITEMS[own_branch])[requirement[own_branch] - 1]
            self.multiworld.state.collect(final)
        self.assertTrue(location.can_reach(self.multiworld.state),
                        f"{location_name} not reachable with its full requirement")
