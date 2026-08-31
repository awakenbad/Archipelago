import unittest

from BaseClasses import MultiWorld

from .bases import ELIGIBLE_UNLOCKS, generate
from ..world import GTASAWorld

COLLECTIBLE_HEAVY_OPTIONS = {
    "end_goal": "end_of_the_line",
    "tag_checks": 30,
    "snapshot_checks": 20,
    "horseshoe_checks": 25,
    "oyster_checks": 25,
    "include_exports": "lists_1_2_and_3",
    "include_ammunation_shop": True,
    "starting_unlock": True,
}

def location_ids(multiworld: MultiWorld) -> set[int]:
    return {loc.address for loc in multiworld.get_locations(1) if loc.address is not None}

def granted_unlock(multiworld: MultiWorld) -> str:
    granted = [item.name for item in multiworld.precollected_items[1] if item.name in ELIGIBLE_UNLOCKS]
    assert len(granted) == 1, granted
    return granted[0]

class TestUniversalTrackerRegen(unittest.TestCase):
    def test_passthrough_reproduces_location_set_under_a_different_seed(self):
        original = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=1)
        slot_data = original.worlds[1].fill_slot_data()
        passthrough = GTASAWorld.interpret_slot_data(slot_data)

        regen = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=2, passthrough=passthrough)

        self.assertEqual(location_ids(original), location_ids(regen))
        self.assertEqual(slot_data, regen.worlds[1].fill_slot_data())

    def test_control_a_different_seed_alone_diverges(self):
        first = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=1)
        second = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=2)
        self.assertNotEqual(location_ids(first), location_ids(second))

    def test_passthrough_holds_when_options_would_change_counts(self):
        original = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=1)
        slot_data = original.worlds[1].fill_slot_data()
        passthrough = GTASAWorld.interpret_slot_data(slot_data)

        different_counts = {**COLLECTIBLE_HEAVY_OPTIONS, "tag_checks": 5, "oyster_checks": 50}
        regen = generate(different_counts, seed=2, passthrough=passthrough)

        self.assertEqual(location_ids(original), location_ids(regen))

class TestUniversalTrackerStartingUnlock(unittest.TestCase):
    def test_regen_opens_with_the_same_unlock(self):
        original = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=1)
        passthrough = GTASAWorld.interpret_slot_data(original.worlds[1].fill_slot_data())

        regen = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=2, passthrough=passthrough)

        self.assertEqual(granted_unlock(original), granted_unlock(regen))

    def test_the_held_back_unlock_is_the_one_missing_from_the_regenerated_pool(self):
        original = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=1)
        passthrough = GTASAWorld.interpret_slot_data(original.worlds[1].fill_slot_data())

        regen = generate(COLLECTIBLE_HEAVY_OPTIONS, seed=2, passthrough=passthrough)

        pooled = {item.name for item in regen.itempool if item.name in ELIGIBLE_UNLOCKS}
        self.assertEqual(ELIGIBLE_UNLOCKS - pooled, {granted_unlock(original)})

    def test_control_seeds_alone_disagree_on_the_unlock(self):
        drawn = {granted_unlock(generate(COLLECTIBLE_HEAVY_OPTIONS, seed=s)) for s in range(1, 12)}
        self.assertGreater(len(drawn), 1)

NON_DEFAULT_TOGGLES = {
    "end_goal": "end_of_the_line",
    "include_street_races": False,
    "freight_checks": 0,
    "starting_unlock": False,
    "include_shooting_range": False,
    "include_stadium_events": False,
}

class TestUniversalTrackerRestoresEveryOption(unittest.TestCase):
    def test_a_yamlless_regen_reproduces_the_location_set(self):
        original = generate(NON_DEFAULT_TOGGLES, seed=1)
        passthrough = GTASAWorld.interpret_slot_data(original.worlds[1].fill_slot_data())

        regen = generate({"end_goal": "end_of_the_line"}, seed=2, passthrough=passthrough)

        self.assertEqual(location_ids(original), location_ids(regen))

    def test_every_declared_option_is_carried(self):
        from ..options import GTASAOptions
        from ..world import SLOT_DATA_OPTION_NAMES

        self.assertEqual(set(SLOT_DATA_OPTION_NAMES), set(GTASAOptions.__annotations__))
