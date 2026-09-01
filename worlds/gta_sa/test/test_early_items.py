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

class TestSanFierroStartAsksForTheSanFierroChain(GTASATestBase):
    options = {
        "starting_point": "san_fierro",
        "end_goal": "yay_ka_boom_boom",
    }

    def test_the_early_items_are_the_three_garage_missions(self) -> None:
        early = self.multiworld.local_early_items[self.player]
        self.assertEqual(dict(early), {PROGRESSIVE_BRANCH_ITEMS["Garage"]: 3})

    def test_nothing_early_is_missing_from_the_pool(self) -> None:
        pool = [item.name for item in self.multiworld.itempool]
        for name, count in self.multiworld.local_early_items[self.player].items():
            self.assertGreaterEqual(pool.count(name), count)

class TestBadlandsStartSpreadsAcrossThreeBranches(GTASATestBase):
    options = {
        "starting_point": "badlands",
        "end_goal": "are_you_going_to_san_fierro",
    }

    def test_the_early_items_open_badlands_and_both_missions_behind_it(self) -> None:
        early = self.multiworld.local_early_items[self.player]
        self.assertEqual(dict(early), {
            PROGRESSIVE_BRANCH_ITEMS["C.R.A.S.H."]: 1,
            PROGRESSIVE_BRANCH_ITEMS["Catalina"]: 1,
            PROGRESSIVE_BRANCH_ITEMS["The Truth"]: 1,
        })
