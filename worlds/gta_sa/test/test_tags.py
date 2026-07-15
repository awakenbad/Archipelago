from .bases import GTASATestBase


class TestTagsEnabled(GTASATestBase):
    options = {
        "include_tags": True,
    }

    def test_all_100_tag_locations_exist(self) -> None:
        for i in range(1, 101):
            with self.subTest(i):
                try:
                    self.world.get_location(f"LS Tag: #{i}")
                except KeyError:
                    self.fail(f"LS Tag: #{i} should exist, but it doesn't.")

    def test_tags_are_reachable_with_nothing(self) -> None:
        # Los Santos is the origin region, and tags have no story-progress prerequisite.
        location = self.world.get_location("LS Tag: #1")
        self.assertTrue(location.can_reach(self.multiworld.state))


class TestTagsDisabled(GTASATestBase):
    options = {
        "include_tags": False,
    }

    def test_no_tag_locations_exist(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Tag: #1")
