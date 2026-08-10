from .bases import GTASATestBase

class TestStoryMissionGating(GTASATestBase):
    def test_first_mission_needs_nothing(self) -> None:
        big_smoke = self.world.get_location("LS Mission: Big Smoke")
        self.assertTrue(big_smoke.can_reach(self.multiworld.state))

    def test_mid_game_mission_needs_its_branch_requirement(self) -> None:
        self.assert_branch_gated("LS Mission: Wrong Side of the Tracks", 29)

    def test_green_sabre_needs_its_full_requirement(self) -> None:
        self.assert_branch_gated("LS Mission: The Green Sabre", 38)

    def test_completion_needs_the_goal_requirement(self) -> None:
        self.assertBeatable(False)
        self.collect_mission_requirement(38)
        self.assertBeatable(True)

class TestRegionEntranceGating(GTASATestBase):
    def test_badlands_opens_when_green_sabre_is_reachable(self) -> None:
        self.collect_mission_requirement(38, hold_back="Sweet")
        self.assertFalse(self.can_reach_entrance("Los Santos to Badlands"))

        self.collect_mission_requirement(38)
        self.assertTrue(self.can_reach_entrance("Los Santos to Badlands"))

    def test_san_fierro_and_las_venturas_are_not_yet_reachable(self) -> None:
        for item_name in ("Progressive Sweet Mission", "Progressive Ryder Mission",
                          "Progressive Big Smoke Mission", "Progressive OG Loc Mission",
                          "Progressive C.R.A.S.H. Mission", "Progressive Cesar Mission"):
            self.collect_by_name(item_name)
        self.assertFalse(self.can_reach_entrance("Badlands to San Fierro"))
        self.assertFalse(self.can_reach_entrance("San Fierro to Las Venturas"))

class TestGoalScoping(GTASATestBase):

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
        # 9 story missions plus the 8 Trucking tiers.
        self.assertEqual(len(badlands_location_names), 17)

    def test_final_badlands_mission_needs_its_requirement(self) -> None:
        self.assert_branch_gated("BD Mission: Are You Going to San Fierro?", 47)

    def test_completion_needs_the_goal_requirement(self) -> None:
        self.assertBeatable(False)
        self.collect_mission_requirement(47)
        self.assertBeatable(True)
