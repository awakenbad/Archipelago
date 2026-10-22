import unittest

from ..client import GTASAContext, collectible_lists


class FakeContext:
    def __init__(self, checked_locations, goal_mission_id=38) -> None:
        self.checked_locations = checked_locations
        self.goal_mission_id = goal_mission_id
        self.sent = []

    def send_to_plugin(self, message: str) -> None:
        self.sent.append(message)

    send_checked_collectibles = GTASAContext.send_checked_collectibles


class TestCollectibleLists(unittest.TestCase):
    def test_ids_become_per_type_indices(self) -> None:
        self.assertEqual(collectible_lists({203, 800, 849, 969, 12, 305}), "TAG=3;OYSTER=0,49;STUNT_JUMP=69")

    def test_a_block_does_not_swallow_its_neighbour(self) -> None:
        self.assertEqual(collectible_lists({299, 300, 549, 550}), "TAG=99;SNAPSHOT=49")


class TestCheckedCollectiblesMessage(unittest.TestCase):
    def test_only_checked_locations_are_sent(self) -> None:
        context = FakeContext({616, 843})
        context.send_checked_collectibles()

        self.assertEqual(context.sent, ["CTRL:collectibles_checked:HORSESHOE=16;OYSTER=43\n"])

    def test_nothing_is_sent_before_anything_is_checked(self) -> None:
        context = FakeContext(set())
        context.send_checked_collectibles()

        self.assertEqual(context.sent, [])

    def test_one_hundred_percent_keeps_blips_for_checks_sent_elsewhere(self) -> None:
        context = FakeContext({616, 843}, goal_mission_id=160)
        context.send_checked_collectibles()

        self.assertEqual(context.sent, [])
