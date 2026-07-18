from .bases import GTASATestBase

# Submissions reachable from the start of the game - gated by just 1 Progressive Mission.
FLAT_GATED_SUBMISSION_LOCATIONS = [
    "LS Mission: Paramedic Level 12",
    "LS Mission: Firefighter Level 12",
    "LS Mission: Vigilante Level 12",
    "LS Mission: Taxi Driver 50 Fares",
    "LS Mission: Burglary $10,000 Stolen",
]

ALL_SUBMISSION_LOCATIONS = FLAT_GATED_SUBMISSION_LOCATIONS + [
    "LS Mission: Los Santos Gym Fight School",
]


class TestSubmissionLocationsExist(GTASATestBase):
    def test_all_submission_locations_exist(self) -> None:
        for location_name in ALL_SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")


class TestSubmissionLocationGating(GTASATestBase):
    def test_submission_locations_are_unreachable_with_no_progressive_missions(self) -> None:
        for location_name in FLAT_GATED_SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                location = self.world.get_location(location_name)
                self.assertFalse(location.can_reach(self.multiworld.state))

    def test_submission_locations_only_need_a_single_progressive_mission(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.multiworld.state.collect(progressive_missions[0])

        for location_name in FLAT_GATED_SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                location = self.world.get_location(location_name)
                self.assertTrue(location.can_reach(self.multiworld.state))


class TestLosSantosGymGating(GTASATestBase):
    def test_requires_five_progressive_missions_not_just_one(self) -> None:
        location = self.world.get_location("LS Mission: Los Santos Gym Fight School")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:4]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[4])
        self.assertTrue(location.can_reach(self.multiworld.state))
