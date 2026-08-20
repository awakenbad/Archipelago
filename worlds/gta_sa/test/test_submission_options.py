from .bases import GTASATestBase

# One per-level location and one final-tier location for each Los Santos submission. The final tier
# is what "on_completion" keeps, since reaching it means the whole activity is done.
MID_TIER_LOCATIONS = [
    "LS Mission: Paramedic Level 1",
    "LS Mission: Firefighter Level 1",
    "LS Mission: Vigilante Level 1",
    "LS Mission: Taxi Driver 5 Fares",
    "LS Mission: Burglary $1,000 Stolen",
    "LS Mission: Pimping Level 1",
]

FINAL_TIER_LOCATIONS = [
    "LS Mission: Paramedic Level 12",
    "LS Mission: Firefighter Level 12",
    "LS Mission: Vigilante Level 12",
    "LS Mission: Taxi Driver 50 Fares",
    "LS Mission: Burglary $10,000 Stolen",
    "LS Mission: Pimping Level 10",
]


class TestSubmissionsPerLevel(GTASATestBase):
    options = {
        "include_submissions": "per_level",
    }

    def test_every_tier_exists(self) -> None:
        for location_name in MID_TIER_LOCATIONS + FINAL_TIER_LOCATIONS:
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")


class TestSubmissionsOnCompletion(GTASATestBase):
    options = {
        "include_submissions": "on_completion",
    }

    def test_only_the_final_tier_exists(self) -> None:
        for location_name in FINAL_TIER_LOCATIONS:
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")

    def test_intermediate_tiers_are_gone(self) -> None:
        for location_name in MID_TIER_LOCATIONS:
            with self.subTest(location_name):
                self.assertRaises(KeyError, self.world.get_location, location_name)

    def test_one_location_per_submission(self) -> None:
        from ..submission_tier_list import SUBMISSION_TIER_LOCATION_NAMES

        tier_locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.name in set(SUBMISSION_TIER_LOCATION_NAMES)
        ]
        self.assertEqual(len(tier_locations), 7)


class TestFewestPossibleLocationsStillGenerates(GTASATestBase):
    """The tightest world you can ask for: one check per submission and no other optional source.

    Progressive Missions nearly fill the story locations on their own, so this configuration ends up
    with exactly as many locations as required items and no room for filler. Adding another
    guaranteed item would overflow it - items.py raises an OptionError saying so, and this test is
    what notices.
    """

    options = {
        "include_submissions": "on_completion",
        "tag_checks": 0,
        "snapshot_checks": 0,
        "include_ammunation_shop": False,
    }

    def test_it_generates(self) -> None:
        # Getting this far means create_items placed everything without overflowing.
        self.assertTrue(self.multiworld.itempool)


class TestSubmissionsUnreachableForTheGoalAreExcluded(GTASATestBase):
    options = {
        "end_goal": "yay_ka_boom_boom",
    }

    def test_boat_school_is_absent(self) -> None:
        self.assertRaises(KeyError, self.world.get_location,
                          "SF Mission: Boat School - Basic Seamanship (Bronze)")

    def test_driving_school_is_still_present(self) -> None:
        # Also San Fierro, but it opens at 39, well before this goal's position 53.
        self.world.get_location("SF Mission: Driving School - The 360 (Bronze)")

    def test_wang_cars_is_absent(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "SF Mission: Zeroing In")

    def test_back_to_school_is_still_present(self) -> None:
        self.world.get_location("SF Mission: Back to School")


class TestBoatSchoolExistsForALaterGoal(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
    }

    def test_boat_and_bike_school_exist(self) -> None:
        for location_name in ("SF Mission: Boat School - Basic Seamanship (Bronze)",
                              "LV Mission: Bike School - Jump & Stoppie (Gold)"):
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")
