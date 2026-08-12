from .bases import GTASATestBase

BMX_LOCATION = "LS Mission: BMX Challenge"
CYCLING_ITEM = "Max Cycling Skill"

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
    }

    def test_no_bmx_location(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, BMX_LOCATION)

    def test_no_cycling_item_in_pool(self) -> None:
        self.assertEqual(self.get_items_by_name(CYCLING_ITEM), [])
