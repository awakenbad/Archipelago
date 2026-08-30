from .bases import GTASATestBase

BMX_LOCATION = "LS Challenge: BMX"
CYCLING_ITEM = "Max Cycling Skill"
NRG_LOCATION = "SF Challenge: NRG-500"
BIKE_ITEM = "Max Bike Skill"
CHILIAD_LOCATION = "BD Challenge: Chiliad"

class TestChallengesEnabled(GTASATestBase):
    options = {
        "include_challenges": 1,
    }

    def test_bmx_location_exists(self) -> None:
        self.world.get_location(BMX_LOCATION)

    def test_bmx_needs_the_cycling_item(self) -> None:
        location = self.world.get_location(BMX_LOCATION)
        self.assertFalse(location.can_reach(self.multiworld.state),
                         "BMX Challenge should not be reachable without Max Cycling Skill")

        self.collect_by_name(CYCLING_ITEM)
        self.assertTrue(location.can_reach(self.multiworld.state),
                        "BMX Challenge should be reachable once Max Cycling Skill is received")

    def test_cycling_item_is_in_the_pool(self) -> None:
        self.assertEqual(len(self.get_items_by_name(CYCLING_ITEM)), 1)

    def test_out_of_scope_challenges_absent(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, NRG_LOCATION)
        self.assertRaises(KeyError, self.world.get_location, CHILIAD_LOCATION)

    def test_bike_item_is_generated_even_with_nothing_to_gate(self) -> None:
        from BaseClasses import ItemClassification
        bike_items = self.get_items_by_name(BIKE_ITEM)
        self.assertEqual(len(bike_items), 1)
        self.assertEqual(bike_items[0].classification, ItemClassification.useful)


class TestChallengesReachingSanFierro(GTASATestBase):
    options = {
        "include_challenges": 1,
        "end_goal": "end_of_the_line",
    }

    def test_nrg_is_not_gated_by_the_bike_item(self) -> None:
        location = self.world.get_location(NRG_LOCATION)
        self.collect_all_but(BIKE_ITEM)
        self.assertTrue(location.can_reach(self.multiworld.state),
                        "NRG-500 Challenge should be reachable once San Fierro is reached, no bike item needed")

    def test_bike_item_is_progression_because_dirt_track_needs_it(self) -> None:
        from BaseClasses import ItemClassification
        bike_items = self.get_items_by_name(BIKE_ITEM)
        self.assertEqual(len(bike_items), 1)
        self.assertEqual(bike_items[0].classification, ItemClassification.progression)

    def test_one_cycling_item_gates_both_bmx_and_chiliad(self) -> None:
        self.assertEqual(len(self.get_items_by_name(CYCLING_ITEM)), 1)

        bmx = self.world.get_location(BMX_LOCATION)
        chiliad = self.world.get_location(CHILIAD_LOCATION)
        self.collect_all_but(CYCLING_ITEM)
        self.assertFalse(bmx.can_reach(self.multiworld.state))
        self.assertFalse(chiliad.can_reach(self.multiworld.state))

        self.collect_by_name(CYCLING_ITEM)
        self.assertTrue(bmx.can_reach(self.multiworld.state))
        self.assertTrue(chiliad.can_reach(self.multiworld.state))


class TestChallengesFromLaterStart(GTASATestBase):
    options = {
        "include_challenges": 1,
        "starting_point": "las_venturas",
        "end_goal": "end_of_the_line",
    }

    def test_bmx_still_present_and_gated(self) -> None:
        location = self.world.get_location(BMX_LOCATION)
        self.assertFalse(location.can_reach(self.multiworld.state))
        self.collect_by_name(CYCLING_ITEM)
        self.assertTrue(location.can_reach(self.multiworld.state))


class TestChallengesDisabled(GTASATestBase):
    options = {
        "include_challenges": 0,
        "end_goal": "end_of_the_line",
    }

    def test_no_challenge_locations(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, BMX_LOCATION)
        self.assertRaises(KeyError, self.world.get_location, NRG_LOCATION)

    def test_no_challenge_items_in_pool(self) -> None:
        self.assertEqual(self.get_items_by_name(CYCLING_ITEM), [])

    def test_the_pinned_skill_items_survive(self) -> None:
        self.assertEqual(len(self.get_items_by_name(BIKE_ITEM)), 1)
