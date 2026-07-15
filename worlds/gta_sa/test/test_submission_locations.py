from .bases import GTASATestBase

SUBMISSION_LOCATIONS = [
    "LS Mission: Paramedic Level 12",
    "LS Mission: Firefighter Level 12",
    "LS Mission: Vigilante Level 12",
    "LS Mission: Taxi Driver 50 Fares",
    "LS Mission: Burglary $10,000 Stolen",
]


class TestSubmissionLocationsExist(GTASATestBase):
    def test_all_submission_locations_exist(self) -> None:
        for location_name in SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")


class TestSubmissionLocationGating(GTASATestBase):
    def test_submission_locations_are_unreachable_with_no_progressive_missions(self) -> None:
        for location_name in SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                location = self.world.get_location(location_name)
                self.assertFalse(location.can_reach(self.multiworld.state))

    def test_submission_locations_only_need_a_single_progressive_mission(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.multiworld.state.collect(progressive_missions[0])

        for location_name in SUBMISSION_LOCATIONS:
            with self.subTest(location_name):
                location = self.world.get_location(location_name)
                self.assertTrue(location.can_reach(self.multiworld.state))
