from .bases import GTASATestBase


class TestTagsEnabled(GTASATestBase):
    options = {
        "tag_checks": 100,
    }

    def test_all_100_tag_locations_exist(self) -> None:
        for i in range(1, 101):
            with self.subTest(i):
                try:
                    self.world.get_location(f"LS Tag: #{i}")
                except KeyError:
                    self.fail(f"LS Tag: #{i} should exist, but it doesn't.")

    def test_tags_need_the_unlock_item(self) -> None:
        from ..items import TAGS_UNLOCK_ITEM

        location = self.world.get_location("LS Tag: #50")

        state = self.multiworld.get_all_state(False)
        self.assertTrue(location.can_reach(state))

        state.remove(self.get_item_by_name(TAGS_UNLOCK_ITEM))
        self.assertFalse(location.can_reach(state))

    def test_the_mission_sprayed_six_need_only_the_mission(self) -> None:
        from ..items import TAGS_UNLOCK_ITEM
        from ..tag_list import MISSION_SPRAYED_TAGS

        state = self.multiworld.get_all_state(False)
        state.remove(self.get_item_by_name(TAGS_UNLOCK_ITEM))

        for number in MISSION_SPRAYED_TAGS:
            with self.subTest(number):
                self.assertTrue(self.world.get_location(f"LS Tag: #{number}").can_reach(state))

    def test_exactly_one_spray_can_exists(self) -> None:
        from ..items import TAGS_UNLOCK_ITEM

        self.assertEqual(len(self.get_items_by_name(TAGS_UNLOCK_ITEM)), 1)


class TestTagsDisabled(GTASATestBase):
    options = {
        "tag_checks": 0,
    }

    def test_no_tag_locations_exist(self) -> None:
        self.assertRaises(KeyError, self.world.get_location, "LS Tag: #1")
