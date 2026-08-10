from test.bases import WorldTestBase

from ..branches import branch_of, effective_requirement
from ..items import PROGRESSIVE_BRANCH_ITEMS
from ..mission_list import get_start_index
from ..world import GTASAWorld

class GTASATestBase(WorldTestBase):
    game = "Grand Theft Auto: San Andreas"
    world: GTASAWorld

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
