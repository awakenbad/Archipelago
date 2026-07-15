from .bases import GTASATestBase


class TestStoryMissionGating(GTASATestBase):
    def test_first_mission_needs_nothing(self) -> None:
        big_smoke = self.world.get_location("LS Mission: Big Smoke")
        self.assertTrue(big_smoke.can_reach(self.multiworld.state))

    def test_mid_game_mission_requires_exact_progressive_mission_count(self) -> None:
        location = self.world.get_location("LS Mission: Wrong Side of the Tracks")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:16]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[16])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_last_mission_requires_25_not_all_26_progressive_missions(self) -> None:
        location = self.world.get_location("LS Mission: The Green Sabre")
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.assertEqual(len(progressive_missions), 26)

        for item in progressive_missions[:25]:
            self.multiworld.state.collect(item)
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_completion_requires_25_progressive_missions(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:24]:
            self.multiworld.state.collect(item)
        self.assertBeatable(False)

        self.multiworld.state.collect(progressive_missions[24])
        self.assertBeatable(True)


class TestRegionEntranceGating(GTASATestBase):
    def test_badlands_requires_23_progressive_missions(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:22]:
            self.multiworld.state.collect(item)
        self.assertFalse(self.can_reach_entrance("Los Santos to Badlands"))

        self.multiworld.state.collect(progressive_missions[22])
        self.assertTrue(self.can_reach_entrance("Los Santos to Badlands"))

    def test_san_fierro_and_las_venturas_are_not_yet_reachable(self) -> None:
        self.collect_by_name("Progressive Mission")
        self.assertFalse(self.can_reach_entrance("Badlands to San Fierro"))
        self.assertFalse(self.can_reach_entrance("San Fierro to Las Venturas"))
