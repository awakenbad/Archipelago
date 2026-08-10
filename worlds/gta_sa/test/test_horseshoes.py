from .bases import GTASATestBase

class TestHorseshoesEnabled(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
        "include_horseshoes": True,
    }

    def test_all_50_horseshoe_locations_exist(self) -> None:
        for i in range(1, 51):
            with self.subTest(i):
                try:
                    self.world.get_location(f"LV Horseshoe: #{i}")
                except KeyError:
                    self.fail(f"LV Horseshoe: #{i} should exist, but it doesn't.")

    def test_horseshoes_need_las_venturas_open(self) -> None:
        horseshoe = self.world.get_location("LV Horseshoe: #1")

        self.collect_mission_requirement(63, hold_back="Triads")
        self.assertFalse(horseshoe.can_reach(self.multiworld.state))

        self.collect_mission_requirement(63)
        self.assertTrue(horseshoe.can_reach(self.multiworld.state))

class TestHorseshoesDisabled(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
        "include_horseshoes": False,
    }

    def test_no_horseshoe_locations_exist(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LV Horseshoe: #1")

class TestHorseshoesOutOfScope(GTASATestBase):
    """A Los Santos goal never reaches Las Venturas, so the option has nothing to create."""

    options = {
        "include_horseshoes": True,
    }

    def test_no_horseshoe_locations_exist(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LV Horseshoe: #1")
