from .bases import GTASATestBase

# The first and last location of each Los Santos submission.
MID_TIER_LOCATIONS = [
    "LS Paramedic: Level 1",
    "LS Firefighter: Level 1",
    "LS Vigilante: Level 1",
    "LS Taxi Driver: 5 Fares",
    "LS Burglary: $1,000 Stolen",
    "LS Pimping: Level 1",
]

FINAL_TIER_LOCATIONS = [
    "LS Paramedic: Level 12",
    "LS Firefighter: Level 12",
    "LS Vigilante: Level 12",
    "LS Taxi Driver: 50 Fares",
    "LS Burglary: $10,000 Stolen",
    "LS Pimping: Level 10",
]


class TestEveryTierIsALocation(GTASATestBase):
    def test_every_tier_exists(self) -> None:
        for location_name in MID_TIER_LOCATIONS + FINAL_TIER_LOCATIONS:
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")


class TestSubmissionsUnreachableForTheGoalAreExcluded(GTASATestBase):
    options = {
        "end_goal": "yay_ka_boom_boom",
    }

    def test_boat_school_is_absent(self) -> None:
        self.assertRaises(KeyError, self.world.get_location,
                          "SF Boat School: Basic Seamanship (Bronze)")

    def test_driving_school_is_still_present(self) -> None:
        # Also San Fierro, but it opens at 39, well before this goal's position 53.
        self.world.get_location("SF Driving School: The 360 (Bronze)")

    def test_wang_cars_is_absent(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "SF Wang Cars: Zeroing In")

    def test_back_to_school_is_still_present(self) -> None:
        self.world.get_location("SF Driving School: Back to School")


class TestBoatSchoolExistsForALaterGoal(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
    }

    def test_boat_and_bike_school_exist(self) -> None:
        for location_name in ("SF Boat School: Basic Seamanship (Bronze)",
                              "LV Bike School: Jump & Stoppie (Gold)"):
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")
