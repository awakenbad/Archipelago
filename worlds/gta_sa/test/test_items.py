from .bases import GTASATestBase
from ..items import WEAPON_FILLER_ITEMS

SUBMISSION_REWARD_ITEMS = [
    "Max Health Upgrade",
    "Max Armor Upgrade",
    "Fire Immunity",
    "Infinite Sprint",
    "Taxi Nitro",
    "Boxing Style",
]


class TestProgressiveMissionItem(GTASATestBase):
    def test_pool_contains_26_progressive_missions(self) -> None:
        self.assertEqual(len(self.get_items_by_name("Progressive Mission")), 26)

    def test_progressive_mission_is_progression_not_useful(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.assertTrue(all(item.advancement for item in progressive_missions))
        self.assertFalse(any(item.useful for item in progressive_missions))


class TestSubmissionRewardItems(GTASATestBase):
    def test_each_submission_reward_item_appears_exactly_once(self) -> None:
        for item_name in SUBMISSION_REWARD_ITEMS:
            with self.subTest(item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_submission_reward_items_are_useful_not_progression(self) -> None:
        reward_items = self.get_items_by_name(SUBMISSION_REWARD_ITEMS)
        self.assertTrue(all(item.useful for item in reward_items))
        self.assertFalse(any(item.advancement for item in reward_items))


class TestFillerItems(GTASATestBase):
    def test_money_is_filler(self) -> None:
        money_items = self.get_items_by_name("Money")
        self.assertTrue(all(item.filler for item in money_items))

    def test_weapon_items_are_filler(self) -> None:
        weapon_items = self.get_items_by_name(WEAPON_FILLER_ITEMS)
        self.assertTrue(all(item.filler for item in weapon_items))

    def test_get_filler_item_name_returns_money_or_a_weapon(self) -> None:
        possible_filler_names = {"Money", *WEAPON_FILLER_ITEMS}
        for _ in range(50):
            with self.subTest():
                self.assertIn(self.world.get_filler_item_name(), possible_filler_names)
