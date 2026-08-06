import unittest

from .bases import GTASATestBase
from ..options import GTASAOptions
from ..submission_tier_list import SUBMISSION_TIERS


class TestSliderRangesMatchTiers(unittest.TestCase):
    """The slider ranges are hand-written in options.py, so this pins them to SUBMISSION_TIERS."""

    def test_each_slider_is_one_to_tier_count(self) -> None:
        hints = GTASAOptions.__annotations__
        for spec in SUBMISSION_TIERS:
            if not spec.option_attr:
                continue
            with self.subTest(spec.option_attr):
                self.assertIn(spec.option_attr, hints, "option_attr has no matching GTASAOptions field")
                option_cls = hints[spec.option_attr]
                self.assertEqual(option_cls.range_start, 1)
                self.assertEqual(option_cls.range_end, spec.tier_count)
                self.assertEqual(option_cls.default, spec.tier_count, "default must be the full length")

    def test_schools_are_uncapped(self) -> None:
        for spec in SUBMISSION_TIERS:
            if "School" in spec.name_template:
                self.assertEqual(spec.option_attr, "", f"{spec.name_template} should have no slider")


class TestParamedicCap(GTASATestBase):
    options = {"include_submissions": "per_level", "paramedic_checks": 5}

    def test_keeps_first_five_levels(self) -> None:
        self.world.get_location("LS Mission: Paramedic Level 5")

    def test_drops_the_rest(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Mission: Paramedic Level 6")


class TestTaxiCap(GTASATestBase):
    # 3 tiers of a 5-fare submission = checks at 5, 10, 15 fares.
    options = {"include_submissions": "per_level", "taxi_checks": 3}

    def test_keeps_the_first_three_milestones(self) -> None:
        self.world.get_location("LS Mission: Taxi Driver 15 Fares")

    def test_drops_beyond_them(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Mission: Taxi Driver 20 Fares")


class TestSliderIgnoredOnCompletion(GTASATestBase):
    options = {"include_submissions": "on_completion", "paramedic_checks": 5}

    def test_only_the_final_tier_survives(self) -> None:
        self.world.get_location("LS Mission: Paramedic Level 12")
        self.assertRaises(KeyError, self.world.get_location, "LS Mission: Paramedic Level 5")
