from BaseClasses import ItemClassification

from .bases import GTASATestBase
from ..client import ITEM_ID_TO_EFFECT
from ..items import ITEM_NAME_TO_ID, STREET_RACES_ITEM
from ..race_list import RACE_COUNT, RACE_GROUPS
from ..submission_tier_list import SUBMISSION_TIERS, get_tier_names

PLUGIN_EFFECT = "street_races"

EXPECTED_GROUPS = (("Los Santos", 0, 9), ("San Fierro", 9, 6), ("Las Venturas", 15, 4 + 6))

RACE_TIERS = [tier for tier in SUBMISSION_TIERS
              if tier.requires_option == "include_street_races"]

def race_names(regions: set[str] | None = None) -> list[str]:
    return [name for tier in RACE_TIERS if regions is None or tier.region in regions
            for name in get_tier_names(tier)]

class TestRaceData(GTASATestBase):
    def test_groups_match_the_marker_ranges(self) -> None:
        actual = tuple((group.region, group.first_index, len(group.names))
                       for group in RACE_GROUPS)
        self.assertEqual(actual, EXPECTED_GROUPS)
        self.assertEqual(RACE_COUNT, 25)

    def test_one_tier_per_group_with_matching_counts(self) -> None:
        self.assertEqual([(tier.region, tier.tier_count) for tier in RACE_TIERS],
                         [(region, count) for region, _, count in EXPECTED_GROUPS])

    def test_tier_slots_are_contiguous_and_do_not_overlap_anything(self) -> None:
        slots = [slot for tier in RACE_TIERS
                 for slot in range(tier.base_slot, tier.base_slot + tier.tier_count)]
        self.assertEqual(slots, list(range(257, 282)))

    def test_names_are_distinct(self) -> None:
        self.assertEqual(len(set(race_names())), 25)

class TestStreetRacesIncluded(GTASATestBase):
    options = {"starting_unlock": False}
    def test_exactly_one_item_is_generated(self) -> None:
        self.assertEqual(len(self.get_items_by_name(STREET_RACES_ITEM)), 1)

    def test_the_item_is_progression(self) -> None:
        self.assertTrue(self.get_items_by_name(STREET_RACES_ITEM)[0].advancement)

    def test_every_group_exists_on_the_shortest_goal(self) -> None:
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual([name for name in race_names() if name not in created], [])

    def test_the_item_alone_opens_every_race(self) -> None:
        state = self.multiworld.get_all_state(False)
        state.remove(self.get_item_by_name(STREET_RACES_ITEM))
        self.assertEqual([name for name in race_names()
                          if state.can_reach_location(name, self.player)], [])

        state = self.multiworld.state.copy()
        state.collect(self.get_item_by_name(STREET_RACES_ITEM), prevent_sweep=True)
        self.assertEqual([name for name in race_names()
                          if not state.can_reach_location(name, self.player)], [])

class TestStreetRacesToTheEnd(GTASATestBase):
    options = {"end_goal": "end_of_the_line", "starting_unlock": False}

    def test_all_twenty_five_exist(self) -> None:
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        missing = [name for name in race_names() if name not in created]
        self.assertEqual(missing, [])

    def test_none_are_reachable_without_the_item(self) -> None:
        state = self.multiworld.get_all_state(False)
        state.remove(self.get_item_by_name(STREET_RACES_ITEM))
        reachable = [name for name in race_names()
                     if state.can_reach_location(name, self.player)]
        self.assertEqual(reachable, [])

    def test_all_are_reachable_with_it(self) -> None:
        state = self.multiworld.get_all_state(False)
        unreachable = [name for name in race_names()
                       if not state.can_reach_location(name, self.player)]
        self.assertEqual(unreachable, [])

class TestStreetRacesTurnedOff(GTASATestBase):
    options = {"end_goal": "end_of_the_line", "include_street_races": False}

    def test_no_item_and_no_locations(self) -> None:
        self.assertEqual(self.get_items_by_name(STREET_RACES_ITEM), [])
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual([name for name in race_names() if name in created], [])


class TestStreetRacesWireContract(GTASATestBase):
    def test_the_item_id_reaches_the_plugin_as_the_expected_effect(self) -> None:
        item_id = ITEM_NAME_TO_ID[STREET_RACES_ITEM]
        self.assertIn(item_id, ITEM_ID_TO_EFFECT)
        self.assertEqual(ITEM_ID_TO_EFFECT[item_id], (PLUGIN_EFFECT, None))

    def test_races_sit_in_the_submission_tier_id_block(self) -> None:
        from ..locations import LOCATION_NAME_TO_ID
        from ..submission_tier_list import SUBMISSION_TIER_BASE_ID
        for tier in RACE_TIERS:
            for offset, name in enumerate(get_tier_names(tier)):
                with self.subTest(name):
                    self.assertEqual(LOCATION_NAME_TO_ID[name],
                                     SUBMISSION_TIER_BASE_ID + tier.base_slot + offset)

    def test_no_two_items_share_an_id(self) -> None:
        by_id: dict[int, list[str]] = {}
        for name, item_id in ITEM_NAME_TO_ID.items():
            by_id.setdefault(item_id, []).append(name)
        self.assertEqual({i: names for i, names in by_id.items() if len(names) > 1}, {})

    def test_no_two_locations_share_an_id(self) -> None:
        from ..locations import LOCATION_NAME_TO_ID
        by_id: dict[int, list[str]] = {}
        for name, location_id in LOCATION_NAME_TO_ID.items():
            by_id.setdefault(location_id, []).append(name)
        self.assertEqual({i: names for i, names in by_id.items() if len(names) > 1}, {})

    def test_classification_is_declared_for_every_item(self) -> None:
        from ..items import DEFAULT_ITEM_CLASSIFICATIONS
        missing = sorted(set(ITEM_NAME_TO_ID) - set(DEFAULT_ITEM_CLASSIFICATIONS))
        self.assertEqual(missing, [])
        self.assertEqual(DEFAULT_ITEM_CLASSIFICATIONS[STREET_RACES_ITEM],
                         ItemClassification.progression)
