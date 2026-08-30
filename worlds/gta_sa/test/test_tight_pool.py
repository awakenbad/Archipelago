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
