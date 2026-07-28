import collections
import unittest

from ..locations import LOCATION_NAME_TO_ID


class TestLocationIdsAreUnique(unittest.TestCase):
    """Each location kind gets its own ID block, and the blocks must not overlap.

    They silently did once: submission tiers grew past 100 slots and ran into the snapshot block, so
    Bike School's checks arrived as snapshot IDs and never registered. Nothing failed loudly - the
    plugin sent a valid ID that simply belonged to another location. This is the guard for that.
    """

    def test_no_two_locations_share_an_id(self) -> None:
        by_id = collections.defaultdict(list)
        for name, location_id in LOCATION_NAME_TO_ID.items():
            by_id[location_id].append(name)

        collisions = {i: names for i, names in by_id.items() if len(names) > 1}
        self.assertEqual(collisions, {}, f"location IDs are shared: {collisions}")

    def test_each_block_stays_inside_its_own_range(self) -> None:
        from ..export_list import EXPORT_BASE_ID, EXPORT_COUNT
        from ..horseshoe_list import HORSESHOE_BASE_ID, HORSESHOE_COUNT
        from ..oyster_list import OYSTER_BASE_ID, OYSTER_COUNT
        from ..snapshot_list import SNAPSHOT_BASE_ID, SNAPSHOT_COUNT
        from ..submission_tier_list import SUBMISSION_TIER_BASE_ID, SUBMISSION_TIER_SLOT_COUNT
        from ..tag_list import TAG_BASE_ID, TAG_COUNT

        blocks = [
            ("tags", TAG_BASE_ID, TAG_COUNT),
            ("snapshots", SNAPSHOT_BASE_ID, SNAPSHOT_COUNT),
            ("horseshoes", HORSESHOE_BASE_ID, HORSESHOE_COUNT),
            ("exports", EXPORT_BASE_ID, EXPORT_COUNT),
            ("oysters", OYSTER_BASE_ID, OYSTER_COUNT),
            ("submission tiers", SUBMISSION_TIER_BASE_ID, SUBMISSION_TIER_SLOT_COUNT),
        ]
        spans = [(base, base + count - 1, name) for name, base, count in blocks]
        spans.sort()

        for (start, end, name), (next_start, _, next_name) in zip(spans, spans[1:]):
            with self.subTest(f"{name} -> {next_name}"):
                self.assertLess(
                    end, next_start,
                    f"{name} ends at {end}, which runs into {next_name} starting at {next_start}",
                )
