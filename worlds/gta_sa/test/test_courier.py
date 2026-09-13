from .bases import GTASATestBase

ROBOIS = [f"LS Courier: Roboi's Food Mart Level {tier}" for tier in (1, 2, 3, 4)]
HIPPY = [f"SF Courier: Hippy Shopper Level {tier}" for tier in (1, 2, 3, 4)]
BURGER_SHOT = [f"LV Courier: Burger Shot Level {tier}" for tier in (1, 2, 3, 4)]

ALL_TIERS = ROBOIS + HIPPY + BURGER_SHOT

UNLOCK_ITEM = "Courier Unlock"

class TestCourierEnabled(GTASATestBase):
    options = {
        "starting_unlock": False,
        "courier_checks": 4,
        "end_goal": "end_of_the_line",
    }

    def test_every_city_has_three_levels(self) -> None:
        for name in ALL_TIERS:
            with self.subTest(name):
                self.world.get_location(name)

    def test_none_are_open_without_the_unlock(self) -> None:
        for name in ALL_TIERS:
            with self.subTest(name):
                self.assertFalse(self.world.get_location(name).can_reach(self.multiworld.state))

    def test_the_one_unlock_opens_all_three_cities(self) -> None:
        self.collect_by_name(UNLOCK_ITEM)
        for name in ALL_TIERS:
            with self.subTest(name):
                self.assertTrue(self.world.get_location(name).can_reach(self.multiworld.state))

    def test_exactly_one_unlock_is_generated(self) -> None:
        self.assertEqual(len(self.get_items_by_name(UNLOCK_ITEM)), 1)

    def test_the_plugin_is_told_to_gate_it(self) -> None:
        self.assertIn(UNLOCK_ITEM, self.world.fill_slot_data()["gated_unlocks"])


class TestCourierOff(GTASATestBase):
    options = {
        "courier_checks": 0,
        "end_goal": "end_of_the_line",
    }

    def test_no_courier_locations(self) -> None:
        for name in ALL_TIERS:
            with self.subTest(name):
                self.assertRaises(KeyError, self.world.get_location, name)

    def test_other_submissions_are_untouched(self) -> None:
        self.world.get_location("SF Valet: 3 Cars Parked")

    def test_no_unlock_item_and_the_bikes_are_not_gated(self) -> None:
        self.assertEqual(self.get_items_by_name(UNLOCK_ITEM), [])
        self.assertNotIn(UNLOCK_ITEM, self.world.fill_slot_data()["gated_unlocks"])


class TestCourierSliderTrimsLevels(GTASATestBase):
    options = {
        "courier_checks": 2,
        "end_goal": "end_of_the_line",
    }

    def test_keeps_the_first_two_levels_of_every_city(self) -> None:
        for names in (ROBOIS, HIPPY, BURGER_SHOT):
            with self.subTest(names[0]):
                self.world.get_location(names[0])
                self.world.get_location(names[1])

    def test_drops_the_rest(self) -> None:
        for names in (ROBOIS, HIPPY, BURGER_SHOT):
            with self.subTest(names[2]):
                self.assertRaises(KeyError, self.world.get_location, names[2])
                self.assertRaises(KeyError, self.world.get_location, names[3])


class TestCourierSurvivesTheShortestGoal(GTASATestBase):
    options = {
        "courier_checks": 4,
        "end_goal": "the_green_sabre",
    }

    def test_all_three_cities_exist_in_a_los_santos_seed(self) -> None:
        for name in ALL_TIERS:
            with self.subTest(name):
                self.world.get_location(name)
