import unittest
from types import SimpleNamespace

from .bases import GTASATestBase
from ..options import GTASAOptions
from ..submission_tier_list import SUBMISSION_TIERS

class TestSliderRangesMatchTiers(unittest.TestCase):
    """The slider ranges are hand-written in options.py, so this pins them to SUBMISSION_TIERS."""

    def test_each_slider_is_one_to_tier_count(self) -> None:
        hints = GTASAOptions.__annotations__
        for spec in SUBMISSION_TIERS:
            if not spec.option_attr or spec.percentage_slider:
                continue
            with self.subTest(spec.option_attr):
                self.assertIn(spec.option_attr, hints, "option_attr has no matching GTASAOptions field")
                option_cls = hints[spec.option_attr]
                expected_start = 0 if spec.zero_disables else 1
                self.assertEqual(option_cls.range_start, expected_start,
                                 "zero_disables sliders must reach 0, the rest must start at 1")
                self.assertEqual(option_cls.range_end, spec.tier_count)
                self.assertEqual(option_cls.default, spec.tier_count, "default must be the full length")

    def test_percentage_slider_spans_zero_to_full_control(self) -> None:
        hints = GTASAOptions.__annotations__
        for spec in SUBMISSION_TIERS:
            if not spec.percentage_slider:
                continue
            with self.subTest(spec.option_attr):
                option_cls = hints[spec.option_attr]
                self.assertEqual(option_cls.range_start, 0, "0 must be reachable to turn the checks off")
                self.assertEqual(option_cls.range_end, spec.tier_count * spec.value_per_tier)

    def test_schools_are_uncapped(self) -> None:
        for spec in SUBMISSION_TIERS:
            if spec.label.endswith("School"):
                self.assertEqual(spec.option_attr, "", f"{spec.label} should have no slider")

class TestParamedicCap(GTASATestBase):
    options = {"include_submissions": "per_level", "paramedic_checks": 5}

    def test_keeps_first_five_levels(self) -> None:
        self.world.get_location("LS Paramedic: Level 5")

    def test_drops_the_rest(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Paramedic: Level 6")

class TestTaxiCap(GTASATestBase):
    # 3 tiers of a 5-fare submission = checks at 5, 10, 15 fares.
    options = {"include_submissions": "per_level", "taxi_checks": 3}

    def test_keeps_the_first_three_milestones(self) -> None:
        self.world.get_location("LS Taxi Driver: 3 Fares")

    def test_drops_beyond_them(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Taxi Driver: 4 Fares")

class TestSliderIgnoredOnCompletion(GTASATestBase):
    options = {"include_submissions": "on_completion", "paramedic_checks": 5}

    def test_only_the_final_tier_survives(self) -> None:
        self.world.get_location("LS Paramedic: Level 12")
        self.assertRaises(KeyError, self.world.get_location, "LS Paramedic: Level 5")

class TestPercentageSliderMapsToTiers(unittest.TestCase):

    def _count(self, spec, target: int) -> int:
        options = SimpleNamespace(**{spec.option_attr: SimpleNamespace(value=target)})
        return spec.included_tier_count(options)

    def test_target_floors_to_the_nearest_five_percent(self) -> None:
        spec = next(s for s in SUBMISSION_TIERS if s.percentage_slider)
        self.assertEqual(self._count(spec, 0), 0)
        self.assertEqual(self._count(spec, 34), 6)
        self.assertEqual(self._count(spec, 35), 7)
        self.assertEqual(self._count(spec, 100), spec.tier_count)

class TestGangTerritoryTarget(GTASATestBase):
    options = {"end_goal": "end_of_the_line", "include_submissions": "per_level", "gang_territory_target": 35}

    def test_keeps_tiers_up_to_the_target(self) -> None:
        self.world.get_location("RTLS Gang Territory: 35% Controlled")

    def test_drops_tiers_past_the_target(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "RTLS Gang Territory: 40% Controlled")

    def test_the_tier_needs_return_to_los_santos_progress(self) -> None:
        location = self.world.get_location("RTLS Gang Territory: 5% Controlled")

        self.collect_mission_requirement(104, hold_back="Return")
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.collect_mission_requirement(104)
        self.assertTrue(location.can_reach(self.multiworld.state))

class TestGangTerritoryOff(GTASATestBase):
    options = {"end_goal": "end_of_the_line", "include_submissions": "per_level", "gang_territory_target": 0}

    def test_no_gang_territory_locations(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "RTLS Gang Territory: 5% Controlled")

class TestGangTerritoryOnCompletion(GTASATestBase):
    options = {"end_goal": "end_of_the_line", "include_submissions": "on_completion", "gang_territory_target": 100}

    def test_only_the_story_threshold_survives(self) -> None:
        self.world.get_location("RTLS Gang Territory: 35% Controlled")
        self.assertRaises(KeyError, self.world.get_location, "RTLS Gang Territory: 100% Controlled")

class TestGangTerritoryOnlyOnEndOfTheLine(GTASATestBase):
    options = {"end_goal": "a_home_in_the_hills", "gang_territory_target": 100}

    def test_no_gang_territory_before_return_to_los_santos(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "RTLS Gang Territory: 5% Controlled")
