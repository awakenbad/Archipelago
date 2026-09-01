import collections

from .bases import GTASATestBase

class TestSmallestSeedStillFits(GTASATestBase):
    options = {
        "end_goal": "the_green_sabre",
        "include_challenges": 0,
        "include_stadium_events": 0,
        "include_exports": 0,
        "include_ammunation_shop": 0,
        "tag_checks": 0,
        "snapshot_checks": 0,
        "horseshoe_checks": 0,
        "oyster_checks": 0,
    }

    def test_it_generates(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Max Bike Skill")), 1)
        self.assertEqual(len(self.get_items_by_name("Max Driving Skill")), 1)

class TestEverySliderAtItsFloor(GTASATestBase):
    run_default_tests = False

    options = {
        "starting_unlock": False,
        "end_goal": "the_green_sabre",
        "include_challenges": 0,
        "include_stadium_events": 0,
        "include_exports": 0,
        "include_ammunation_shop": 0,
        "include_street_races": False,
        "include_shooting_range": False,
        "tag_checks": 0,
        "snapshot_checks": 0,
        "horseshoe_checks": 0,
        "oyster_checks": 0,
        "school_medals": "off",
        "paramedic_checks": 1,
        "firefighter_checks": 1,
        "vigilante_checks": 1,
        "taxi_checks": 1,
        "burglary_checks": 0,
        "trucking_checks": 0,
        "valet_checks": 0,
        "pimping_checks": 0,
        "quarry_checks": 0,
        "courier_checks": 0,
        "freight_checks": 0,
    }

    def test_the_pool_exactly_fills_the_locations(self) -> None:
        unfilled = self.multiworld.get_unfilled_locations(self.player)
        self.assertEqual(len(self.multiworld.itempool), len(unfilled))

    def test_every_item_logic_needs_is_present(self) -> None:
        from ..items import gated_unlock_items, gating_skill_items

        pooled = collections.Counter(item.name for item in self.multiworld.itempool)
        pooled.update(item.name for item in self.multiworld.precollected_items[self.player])

        for name in gated_unlock_items(self.world) + sorted(gating_skill_items(self.world)):
            with self.subTest(name):
                self.assertGreaterEqual(pooled[name], 1)
