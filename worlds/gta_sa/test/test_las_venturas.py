from .bases import GTASATestBase

# Optional side content with unverified GXT keys: no locations, no story positions, and no
# Progressive Mission spent (see OPTIONAL_MISSION_IDS in the mod's EntityIDs.h).
HEIST_MISSION_NAMES = [
    "LV Mission: Architectural Espionage",
    "LV Mission: Key To Her Heart",
    "LV Mission: Dam And Blast",
    "LV Mission: Cop Wheels",
    "LV Mission: Up, Up and Away!",
    "LV Mission: Breaking the Bank at Caligula's",
]

MEAT_BUSINESS = "LV Mission: The Meat Business"
MADD_DOGG = "LV Mission: Madd Dogg"
GOAL = "LV Mission: A Home in the Hills"

# Story positions. The heist takes none of them, so the goal sits directly after High Noon.
MEAT_BUSINESS_POSITION = 68
MADD_DOGG_POSITION = 70
GOAL_POSITION = 75


class TestHomeInTheHillsGoal(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
    }

    def test_las_venturas_missions_exist(self) -> None:
        for location_name in ("LV Mission: Monster", "LV Mission: Learning to Fly",
                              "LV Mission: Fish in a Barrel", MADD_DOGG):
            with self.subTest(location_name):
                try:
                    self.world.get_location(location_name)
                except KeyError:
                    self.fail(f"{location_name} should exist, but it doesn't.")

    def test_the_goal_is_an_unrandomizable_event(self) -> None:
        location = self.world.get_location(GOAL)
        self.assertIsNone(location.address)
        self.assertEqual(location.item.name, "Victory")

    def test_the_heist_missions_have_no_locations(self) -> None:
        for location_name in HEIST_MISSION_NAMES:
            with self.subTest(location_name):
                self.assertRaises(KeyError, self.world.get_location, location_name)

    def test_madd_dogg_opens_off_the_meat_business(self) -> None:
        # Madd Dogg and Fish in a Barrel both open off The Meat Business, so Madd Dogg must not be
        # gated behind the later casino missions.
        progressive_missions = self.get_items_by_name("Progressive Mission")
        madd_dogg = self.world.get_location(MADD_DOGG)

        for item in progressive_missions[:MADD_DOGG_POSITION]:
            self.multiworld.state.collect(item)
        self.assertTrue(madd_dogg.can_reach(self.multiworld.state))

    def test_the_goal_sits_directly_after_high_noon(self) -> None:
        """The heist takes no story position, because finishing it is not required for the goal."""
        progressive_missions = self.get_items_by_name("Progressive Mission")
        goal = self.world.get_location(GOAL)

        for item in progressive_missions[:GOAL_POSITION - 1]:
            self.multiworld.state.collect(item)
        self.assertFalse(goal.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[GOAL_POSITION - 1])
        self.assertTrue(goal.can_reach(self.multiworld.state))

    def test_the_pool_covers_every_story_position(self) -> None:
        # One Progressive Mission per position, or the run cannot be finished.
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.assertEqual(len(progressive_missions), GOAL_POSITION + 1)

    def test_las_venturas_is_unreachable_before_san_fierro_is_finished(self) -> None:
        monster = self.world.get_location("LV Mission: Monster")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:53]:
            self.multiworld.state.collect(item)
        self.assertFalse(monster.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[53])
        self.assertTrue(monster.can_reach(self.multiworld.state))


class TestEarlierGoalsHaveNoLasVenturas(GTASATestBase):
    def test_green_sabre_seed_has_no_las_venturas_locations(self) -> None:
        las_venturas = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.name.startswith("LV ")
        ]
        self.assertEqual(las_venturas, [])
