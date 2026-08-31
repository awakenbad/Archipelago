from BaseClasses import CollectionState

from ..items import PROGRESSIVE_BRANCH_ITEMS
from .bases import GTASATestBase

RYDER = PROGRESSIVE_BRANCH_ITEMS["Ryder"]
SWEET = PROGRESSIVE_BRANCH_ITEMS["Sweet"]

def openings(test) -> int:
    empty = CollectionState(test.multiworld)
    return sum(1 for location in test.multiworld.get_locations(test.player)
               if location.address is not None and location.can_reach(empty))

def early_total(test) -> int:
    return sum(test.multiworld.local_early_items[test.player].values())

class TestRoomySeedAsksForAllThree(GTASATestBase):
    def test_the_full_request_survives(self) -> None:
        early = self.multiworld.local_early_items[self.player]
        self.assertEqual(early[RYDER], 1)
        self.assertEqual(early[SWEET], 2)

class TestNarrowOpeningIsCapped(GTASATestBase):
    options = {
        "starting_unlock": False,
        "courier_checks": 0,
        "end_goal": "the_green_sabre",
    }

    def test_the_opening_is_a_single_location(self) -> None:
        self.assertEqual(openings(self), 1)

    def test_no_more_is_asked_for_than_the_opening_holds(self) -> None:
        self.assertLessEqual(early_total(self), openings(self))

    def test_the_one_early_item_is_ryder(self) -> None:
        early = self.multiworld.local_early_items[self.player]
        self.assertEqual(early.get(RYDER), 1)
        self.assertNotIn(SWEET, early)
