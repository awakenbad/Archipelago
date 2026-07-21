from .bases import GTASATestBase


class TestStoryMissionGating(GTASATestBase):
    def test_first_mission_needs_nothing(self) -> None:
        big_smoke = self.world.get_location("LS Mission: Big Smoke")
        self.assertTrue(big_smoke.can_reach(self.multiworld.state))

    def test_mid_game_mission_requires_exact_progressive_mission_count(self) -> None:
        # Wrong Side of the Tracks sits at story position 12.
        location = self.world.get_location("LS Mission: Wrong Side of the Tracks")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:11]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[11])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_green_sabre_requires_26_progressive_missions(self) -> None:
        location = self.world.get_location("LS Mission: The Green Sabre")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:25]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[25])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_completion_requires_26_progressive_missions(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:25]:
            self.multiworld.state.collect(item)
        self.assertBeatable(False)

        self.multiworld.state.collect(progressive_missions[25])
        self.assertBeatable(True)


class TestRegionEntranceGating(GTASATestBase):
    def test_badlands_requires_27_progressive_missions(self) -> None:
        # The Green Sabre (position 26) must actually be completed, so the entrance needs 27.
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:26]:
            self.multiworld.state.collect(item)
        self.assertFalse(self.can_reach_entrance("Los Santos to Badlands"))

        self.multiworld.state.collect(progressive_missions[26])
        self.assertTrue(self.can_reach_entrance("Los Santos to Badlands"))

    def test_san_fierro_and_las_venturas_are_not_yet_reachable(self) -> None:
        self.collect_by_name("Progressive Mission")
        self.assertFalse(self.can_reach_entrance("Badlands to San Fierro"))
        self.assertFalse(self.can_reach_entrance("San Fierro to Las Venturas"))


class TestGoalScoping(GTASATestBase):
    """The Green Sabre goal must not generate Badlands content.

    Locations past the goal would still receive items - including other players'
    progression - which this seed never requires the player to reach.
    """

    def test_badlands_locations_are_not_created(self) -> None:
        badlands_location_names = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.name.startswith("BD ")
        ]
        self.assertEqual(badlands_location_names, [])

    def test_badlands_region_holds_no_locations(self) -> None:
        self.assertEqual(len(self.world.get_region("Badlands").locations), 0)


class TestGoalScopingWithBadlandsGoal(GTASATestBase):
    options = {"end_goal": "are_you_going_to_san_fierro"}

    def test_badlands_locations_are_created(self) -> None:
        badlands_location_names = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.name.startswith("BD ")
        ]
        self.assertEqual(len(badlands_location_names), 9)

    def test_final_badlands_mission_requires_35_progressive_missions(self) -> None:
        location = self.world.get_location("BD Mission: Are You Going to San Fierro?")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:34]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[34])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_completion_requires_35_progressive_missions(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:34]:
            self.multiworld.state.collect(item)
        self.assertBeatable(False)

        self.multiworld.state.collect(progressive_missions[34])
        self.assertBeatable(True)
