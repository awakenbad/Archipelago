from .bases import GTASATestBase
from ..items import TRAP_ITEMS, UTILITY_FILLER_ITEMS, WEAPON_FILLER_ITEMS

SUBMISSION_REWARD_ITEMS = [
    "Max Health Upgrade",
    "Max Armor Upgrade",
    "Fire Immunity",
    "Infinite Sprint",
    "Taxi Nitro",
    "Boxing Style",
]


class TestProgressiveMissionItem(GTASATestBase):
    def test_pool_contains_27_progressive_missions_for_the_los_santos_goal(self) -> None:
        # Default goal is The Green Sabre, so only the Los Santos positions (0-26) are in play.
        self.assertEqual(len(self.get_items_by_name("Progressive Mission")), 27)

    def test_progressive_mission_is_progression_not_useful(self) -> None:
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.assertTrue(all(item.advancement for item in progressive_missions))
        self.assertFalse(any(item.useful for item in progressive_missions))


class TestProgressiveMissionItemWithBadlandsGoal(GTASATestBase):
    options = {"end_goal": "are_you_going_to_san_fierro"}

    def test_pool_grows_to_36_progressive_missions(self) -> None:
        # Los Santos 0-26 plus Badlands 27-35.
        self.assertEqual(len(self.get_items_by_name("Progressive Mission")), 36)


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

    def test_get_filler_item_name_returns_money_a_weapon_or_a_trap(self) -> None:
        possible_filler_names = {"Money", *WEAPON_FILLER_ITEMS, *TRAP_ITEMS, *UTILITY_FILLER_ITEMS}
        for _ in range(50):
            with self.subTest():
                self.assertIn(self.world.get_filler_item_name(), possible_filler_names)
