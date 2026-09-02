from .bases import GTASATestBase

WANG_CARS_MISSIONS = (
    "SF Wang Cars: Zeroing In",
    "SF Wang Cars: Test Drive",
    "SF Wang Cars: Customs Fast Track",
    "SF Wang Cars: Puncture Wounds",
)

AN_EXPORT = "SF Export: Patriot"

class TestWangCarsOn(GTASATestBase):
    options = {
        "starting_unlock": False,
        "end_goal": "a_home_in_the_hills",
        "include_exports": 3,
        "include_wang_cars": True,
    }

    def test_exactly_one_unlock_item_is_created(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        self.assertEqual(len(self.get_items_by_name(WANG_CARS_UNLOCK_ITEM)), 1)

    def test_nothing_opens_without_it(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        state = self.multiworld.get_all_state(False)
        state.remove(self.get_item_by_name(WANG_CARS_UNLOCK_ITEM))
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                self.assertFalse(self.world.get_location(location_name).can_reach(state))

    def test_the_item_is_the_only_gate(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        self.collect_mission_requirement(47)
        self.collect(self.get_items_by_name(WANG_CARS_UNLOCK_ITEM))
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                self.assertTrue(
                    self.world.get_location(location_name).can_reach(self.multiworld.state))

    def test_the_seed_tells_the_plugin_wang_cars_is_in_play(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["wang_cars"], 1)

    def test_the_seed_names_the_item_as_gated(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        self.assertIn(WANG_CARS_UNLOCK_ITEM, self.world.fill_slot_data()["gated_unlocks"])

class TestWangCarsOff(GTASATestBase):
    options = {
        "starting_unlock": False,
        "end_goal": "a_home_in_the_hills",
        "include_exports": 3,
        "include_wang_cars": False,
    }

    def test_no_unlock_item_is_created(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        self.assertEqual(self.get_items_by_name(WANG_CARS_UNLOCK_ITEM), [])

    def test_the_locations_are_still_there_on_their_vanilla_story_gate(self) -> None:
        self.collect_mission_requirement(63)
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                self.assertTrue(
                    self.world.get_location(location_name).can_reach(self.multiworld.state))

    def test_and_the_plugin_is_told_wang_cars_is_out(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["wang_cars"], 0)
        self.assertNotIn(WANG_CARS_UNLOCK_ITEM, slot_data["gated_unlocks"])

class TestWangCarsOnTheEarliestGoal(GTASATestBase):
    options = {
        "starting_unlock": False,
        "end_goal": "the_green_sabre",
        "include_exports": 3,
        "include_wang_cars": True,
    }

    def test_the_locations_exist_anyway(self) -> None:
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")

    def test_the_item_opens_them_from_a_standing_start(self) -> None:
        from BaseClasses import CollectionState
        from ..items import WANG_CARS_UNLOCK_ITEM

        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(WANG_CARS_UNLOCK_ITEM))
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                self.assertTrue(self.world.get_location(location_name).can_reach(state))

    def test_they_are_shut_without_it(self) -> None:
        from ..items import WANG_CARS_UNLOCK_ITEM

        state = self.multiworld.get_all_state(False)
        state.remove(self.get_item_by_name(WANG_CARS_UNLOCK_ITEM))
        for location_name in (*WANG_CARS_MISSIONS, AN_EXPORT):
            with self.subTest(location_name):
                self.assertFalse(self.world.get_location(location_name).can_reach(state))
