from BaseClasses import CollectionState

from .bases import GTASATestBase

class TestHorseshoesEnabled(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
        "starting_unlock": False,
        "horseshoe_checks": 50,
    }

    def test_all_50_horseshoe_locations_exist(self) -> None:
        for i in range(1, 51):
            with self.subTest(i):
                try:
                    self.world.get_location(f"LV Horseshoe: #{i}")
                except KeyError:
                    self.fail(f"LV Horseshoe: #{i} should exist, but it doesn't.")

    def test_horseshoes_need_the_unlock_item(self) -> None:
        from ..items import HORSESHOES_UNLOCK_ITEM

        location = self.world.get_location("LV Horseshoe: #1")

        state = self.multiworld.get_all_state(False)
        self.assertTrue(location.can_reach(state))

        state.remove(self.get_item_by_name(HORSESHOES_UNLOCK_ITEM))
        self.assertFalse(location.can_reach(state))

    def test_the_unlock_item_is_the_only_gate(self) -> None:
        from ..items import HORSESHOES_UNLOCK_ITEM

        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(HORSESHOES_UNLOCK_ITEM))

        self.assertTrue(self.world.get_location("LV Horseshoe: #1").can_reach(state))

class TestHorseshoesDisabled(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
        "horseshoe_checks": 0,
    }

    def test_no_horseshoe_locations_exist(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LV Horseshoe: #1")

    def test_no_unlock_item_is_created(self) -> None:
        from ..items import HORSESHOES_UNLOCK_ITEM

        self.assertEqual(self.get_items_by_name(HORSESHOES_UNLOCK_ITEM), [])

class TestHorseshoesOnAGoalThatNeverReachesLasVenturas(GTASATestBase):
    options = {
        "starting_unlock": False,
        "horseshoe_checks": 50,
    }

    def test_the_locations_exist(self) -> None:
        self.assertEqual(len([location for location in self.multiworld.get_locations(self.player)
                              if location.name.startswith("LV Horseshoe")]), 50)

    def test_and_so_does_the_item_that_opens_them(self) -> None:
        from ..items import HORSESHOES_UNLOCK_ITEM

        self.assertEqual(len(self.get_items_by_name(HORSESHOES_UNLOCK_ITEM)), 1)
