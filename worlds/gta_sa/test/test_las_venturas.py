from .bases import GTASATestBase

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
SAINT_MARKS = "LV Mission: Saint Mark's Bistro"
GOAL = "LV Mission: A Home in the Hills"

# Story positions. The heist takes none of them, so the goal sits directly after Saint Mark's.
MEAT_BUSINESS_POSITION = 68
MADD_DOGG_POSITION = 70
SAINT_MARKS_POSITION = 74
GOAL_POSITION = 75

class TestHomeInTheHillsGoal(GTASATestBase):
    options = {
        "end_goal": "a_home_in_the_hills",
    }

    def test_wang_cars_exists_and_needs_yay_ka_boom_boom(self) -> None:
        location = self.world.get_location("SF Mission: Zeroing In")

        self.collect_mission_requirement(63, hold_back="Triads")
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.collect_mission_requirement(63)
        self.assertTrue(location.can_reach(self.multiworld.state))

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

    def test_the_heist_opens_off_explosive_situation(self) -> None:
        self.collect_mission_requirement(85, hold_back="Four Dragons Casino")
        for location_name in HEIST_MISSION_NAMES[:-1]:
            with self.subTest(location_name):
                self.assertFalse(self.world.get_location(location_name).can_reach(self.multiworld.state))

        self.collect_mission_requirement(85)
        for location_name in HEIST_MISSION_NAMES[:-1]:
            with self.subTest(location_name):
                self.assertTrue(self.world.get_location(location_name).can_reach(self.multiworld.state))

    def test_breaking_the_bank_waits_for_saint_marks_bistro(self) -> None:
        robbery = self.world.get_location(HEIST_MISSION_NAMES[-1])

        self.collect_mission_requirement(92, hold_back="Caligula's Palace")
        self.assertFalse(robbery.can_reach(self.multiworld.state))

        self.collect_mission_requirement(92)
        self.assertTrue(robbery.can_reach(self.multiworld.state))

    def test_madd_dogg_opens_off_the_meat_business(self) -> None:
        # gated behind the later casino missions.
        madd_dogg = self.world.get_location(MADD_DOGG)
        self.collect_mission_requirement(95)
        self.assertTrue(madd_dogg.can_reach(self.multiworld.state))

    def test_the_goal_sits_directly_after_saint_marks_bistro(self) -> None:
        self.assert_branch_gated(GOAL, 102)

    def test_saint_marks_bistro_comes_last_of_the_las_venturas_missions(self) -> None:
        from ..challenge_list import CHALLENGE_LOCATION_IDS
        from ..mission_list import get_mission_location_name, get_optional_mission_requirements
        from ..stadium_list import STADIUM_LOCATION_IDS

        optional_names = set(get_optional_mission_requirements())
        challenge_names = {get_mission_location_name(mission_id)
                           for mission_id in CHALLENGE_LOCATION_IDS | STADIUM_LOCATION_IDS}
        self.collect_mission_requirement(92)

        las_venturas_missions = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.name.startswith("LV ")
            and location.name not in (SAINT_MARKS, GOAL)
            and location.name not in optional_names
            and location.name not in challenge_names
        ]
        for location in las_venturas_missions:
            with self.subTest(location.name):
                self.assertTrue(location.can_reach(self.multiworld.state))

        self.assertTrue(self.world.get_location(SAINT_MARKS).can_reach(self.multiworld.state))

    def test_the_pool_covers_every_branch_mission(self) -> None:
        from ..branches import branch_pool_counts
        from ..items import PROGRESSIVE_BRANCH_ITEMS

        total = sum(len(self.get_items_by_name(name)) for name in PROGRESSIVE_BRANCH_ITEMS.values())
        self.assertEqual(total, sum(branch_pool_counts(0, GOAL_POSITION + 1).values()))

    def test_las_venturas_is_unreachable_before_san_fierro_is_finished(self) -> None:
        monster = self.world.get_location("LV Mission: Monster")

        self.collect_mission_requirement(75, hold_back="Triads")
        self.assertFalse(monster.can_reach(self.multiworld.state))

        self.collect_mission_requirement(75)
        self.assertTrue(monster.can_reach(self.multiworld.state))

class TestEarlierGoalsHaveNoLasVenturas(GTASATestBase):
    def test_green_sabre_seed_has_no_las_venturas_locations(self) -> None:
        las_venturas = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if location.name.startswith("LV ")
        ]
        self.assertEqual(las_venturas, [])
