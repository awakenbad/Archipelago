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


class TestSubmissionLevelLocations(GTASATestBase):
    """Paramedic/Firefighter/Vigilante pay out per level (1-12), not once on completion."""

    def test_every_level_of_every_activity_exists(self) -> None:
        for activity in ("Paramedic", "Firefighter", "Vigilante"):
            for level in range(1, 13):
                location_name = f"LS Mission: {activity} Level {level}"
                with self.subTest(location_name):
                    try:
                        self.world.get_location(location_name)
                    except KeyError:
                        self.fail(f"{location_name} should exist, but it doesn't.")

    def test_thirty_six_level_locations_are_created(self) -> None:
        level_locations = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if " Level " in location.name
        ]
        self.assertEqual(len(level_locations), 36)

    def test_levels_need_only_a_single_progressive_mission(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.multiworld.state.collect(progressive_missions[0])

        for activity in ("Paramedic", "Firefighter", "Vigilante"):
            for level in (1, 12):
                location_name = f"LS Mission: {activity} Level {level}"
                with self.subTest(location_name):
                    location = self.world.get_location(location_name)
                    self.assertTrue(location.can_reach(self.multiworld.state))

    def test_level_ids_match_the_plugin_slot_scheme(self) -> None:
        # The plugin sends slot = activity_index * 12 + (level - 1), client adds base 400.
        from ..submission_tier_list import SUBMISSION_TIER_BASE_ID
        from ..locations import LOCATION_NAME_TO_ID

        for activity_index, activity in enumerate(("Paramedic", "Firefighter", "Vigilante")):
            for level in range(1, 13):
                expected = SUBMISSION_TIER_BASE_ID + activity_index * 12 + (level - 1)
                name = f"LS Mission: {activity} Level {level}"
                with self.subTest(name):
                    self.assertEqual(LOCATION_NAME_TO_ID[name], expected)


class TestTieredSubmissionLocations(GTASATestBase):
    """Taxi and Burglary pay out per tier too, not just on completion."""

    def test_taxi_tiers_exist_every_five_fares(self) -> None:
        for tier in range(1, 11):
            name = f"LS Mission: Taxi Driver {tier * 5} Fares"
            with self.subTest(name):
                try:
                    self.world.get_location(name)
                except KeyError:
                    self.fail(f"{name} should exist, but it doesn't.")

    def test_burglary_tiers_exist_every_thousand_dollars(self) -> None:
        for tier in range(1, 11):
            name = f"LS Mission: Burglary ${tier * 1000:,} Stolen"
            with self.subTest(name):
                try:
                    self.world.get_location(name)
                except KeyError:
                    self.fail(f"{name} should exist, but it doesn't.")

    def test_all_tier_locations_exist(self) -> None:
        from ..submission_tier_list import (
            SUBMISSION_TIER_LOCATION_NAMES,
            SUBMISSION_TIER_SLOT_COUNT,
        )
        self.assertEqual(len(SUBMISSION_TIER_LOCATION_NAMES), SUBMISSION_TIER_SLOT_COUNT)

    def test_tier_slot_layout_matches_the_plugin(self) -> None:
        # Slot bases must match the SubmissionTierSpec constants in the mod's EntityIDs.h.
        from ..submission_tier_list import SUBMISSION_TIER_BASE_ID, SUBMISSION_TIER_LOCATION_NAMES
        from ..locations import LOCATION_NAME_TO_ID

        expected_first_slots = {
            0: "LS Mission: Paramedic Level 1",
            12: "LS Mission: Firefighter Level 1",
            24: "LS Mission: Vigilante Level 1",
            36: "LS Mission: Taxi Driver 5 Fares",
            46: "LS Mission: Burglary $1,000 Stolen",
        }
        for slot, name in expected_first_slots.items():
            with self.subTest(name):
                self.assertEqual(SUBMISSION_TIER_LOCATION_NAMES[slot], name)
                self.assertEqual(LOCATION_NAME_TO_ID[name], SUBMISSION_TIER_BASE_ID + slot)


class TestSubmissionTierSlotLayout(GTASATestBase):
    """Each submission owns a reserved, contiguous block of slots.

    Base slots are hand-written here and again as SubmissionTierSpec in the mod's EntityIDs.h.
    If a tier count changes without shifting every later base slot, the blocks overlap and one
    submission's checks silently arrive as another's - no crash, just wrong locations.
    """

    def test_blocks_are_contiguous_with_no_overlap_or_gaps(self) -> None:
        from ..submission_tier_list import SUBMISSION_TIERS

        expected_base = 0
        for tier_spec in SUBMISSION_TIERS:
            with self.subTest(tier_spec.name_template):
                self.assertEqual(tier_spec.base_slot, expected_base)
                expected_base = tier_spec.base_slot + tier_spec.tier_count

    def test_declared_slot_count_matches_the_blocks(self) -> None:
        from ..submission_tier_list import (
            SUBMISSION_TIERS,
            SUBMISSION_TIER_SLOT_COUNT,
            SUBMISSION_TIER_LOCATION_NAMES,
        )

        total = sum(tier_spec.tier_count for tier_spec in SUBMISSION_TIERS)
        self.assertEqual(total, SUBMISSION_TIER_SLOT_COUNT)
        self.assertEqual(len(SUBMISSION_TIER_LOCATION_NAMES), SUBMISSION_TIER_SLOT_COUNT)

    def test_every_tier_location_id_is_unique(self) -> None:
        from ..submission_tier_list import SUBMISSION_TIER_LOCATION_NAMES
        from ..locations import LOCATION_NAME_TO_ID

        ids = [LOCATION_NAME_TO_ID[name] for name in SUBMISSION_TIER_LOCATION_NAMES]
        self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(len(set(SUBMISSION_TIER_LOCATION_NAMES)), len(SUBMISSION_TIER_LOCATION_NAMES))


class TestTruckingIsScopedToBadlands(GTASATestBase):
    """Trucking is at RS Haul in Flint County, so it must not exist in a Los Santos-only seed."""

    def test_trucking_locations_are_not_created_for_the_los_santos_goal(self) -> None:
        trucking = [
            location.name
            for location in self.multiworld.get_locations(self.player)
            if "Trucking" in location.name
        ]
        self.assertEqual(trucking, [])


class TestTruckingWithBadlandsGoal(GTASATestBase):
    options = {"end_goal": "are_you_going_to_san_fierro"}

    def test_all_eight_trucking_tiers_exist(self) -> None:
        for tier in range(1, 9):
            name = f"BD Mission: Trucking Level {tier}"
            with self.subTest(name):
                try:
                    self.world.get_location(name)
                except KeyError:
                    self.fail(f"{name} should exist, but it doesn't.")

    def test_trucking_needs_tanker_commander_not_just_one_mission(self) -> None:
        # Tanker Commander sits at story position 32, so Trucking opens at 33.
        location = self.world.get_location("BD Mission: Trucking Level 1")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:32]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[32])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_trucking_slots_follow_burglary(self) -> None:
        from ..submission_tier_list import SUBMISSION_TIER_BASE_ID
        from ..locations import LOCATION_NAME_TO_ID

        self.assertEqual(LOCATION_NAME_TO_ID["BD Mission: Trucking Level 1"],
                         SUBMISSION_TIER_BASE_ID + 56)
        self.assertEqual(LOCATION_NAME_TO_ID["BD Mission: Trucking Level 8"],
                         SUBMISSION_TIER_BASE_ID + 63)
