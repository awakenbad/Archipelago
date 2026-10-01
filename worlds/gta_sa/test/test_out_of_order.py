import unittest

from .bases import GTASATestBase
from ..branches import branch_of
from ..items import PROGRESSIVE_BRANCH_ITEMS
from ..mission_list import STORY_MISSION_ORDER, get_mission_location_name

OUT_OF_ORDER = {"starting_unlock": False, "mission_order": "out_of_order", "end_of_the_line_requirement": 5}


class OutOfOrderTestBase(GTASATestBase):
    options = OUT_OF_ORDER

    def give(self, branch: str, count: int) -> None:
        for item in self.get_items_by_name(PROGRESSIVE_BRANCH_ITEMS[branch])[:count]:
            self.multiworld.state.collect(item)

    def reachable(self, location_name: str) -> bool:
        return self.world.get_location(location_name).can_reach(self.multiworld.state)

    def mission_reachable(self, mission_id: int) -> bool:
        return self.reachable(get_mission_location_name(mission_id))

    def tier_location(self, base_slot: int) -> str:
        from ..submission_tier_list import SUBMISSION_TIERS, get_tier_names

        spec = next(spec for spec in SUBMISSION_TIERS if spec.base_slot == base_slot)
        return get_tier_names(spec)[0]


class TestStartingPointAndEndGoalAreIgnored(GTASATestBase):
    options = {"starting_unlock": False, "mission_order": "out_of_order",
               "starting_point": "las_venturas", "end_goal": "yay_ka_boom_boom"}

    def test_the_seed_plays_los_santos_to_end_of_the_line(self) -> None:
        self.assertEqual(self.world.options.starting_point.current_key, "los_santos")
        self.assertEqual(self.world.options.end_goal.current_key, "end_of_the_line")

    def test_slot_data_carries_the_overwritten_values(self) -> None:
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["goal_mission_id"], 112)
        self.assertEqual(slot_data["options"]["starting_point"], 0)
        self.assertEqual(slot_data["options"]["end_goal"], 4)


class TestEndOfTheLine(OutOfOrderTestBase):
    def test_it_opens_on_the_required_number_of_progressive_items_from_any_branch(self) -> None:
        self.give("Sweet", 2)
        self.give("Garage", 1)
        self.give("Toreno", 1)
        self.assertFalse(self.mission_reachable(112), "End of the Line reachable with 4 of 5 items")

        self.give("Woozie", 1)
        self.assertTrue(self.mission_reachable(112), "End of the Line not reachable with 5 items")


class TestEndOfTheLineAtItsCap(OutOfOrderTestBase):
    options = {**OUT_OF_ORDER, "end_of_the_line_requirement": 83}


class TestEndOfTheLineAtItsMinimum(OutOfOrderTestBase):
    options = {**OUT_OF_ORDER, "end_of_the_line_requirement": 1}


class TestEveryRegionIsOpen(OutOfOrderTestBase):
    def test_no_region_needs_an_item(self) -> None:
        for region_name in ("Badlands", "San Fierro", "Las Venturas", "Return to Los Santos"):
            with self.subTest(region_name):
                self.assertTrue(self.can_reach_region(region_name))


class TestOutOfOrderEdges(OutOfOrderTestBase):
    def test_are_you_going_to_san_fierro_needs_only_the_truth(self) -> None:
        self.give("The Truth", 1)
        self.assertFalse(self.mission_reachable(47))
        self.give("The Truth", 2)
        self.assertTrue(self.mission_reachable(47))

    def test_photo_opportunity_waits_for_deconstruction(self) -> None:
        self.give("Triads", 6)
        self.give("Garage", 2)
        self.assertFalse(self.mission_reachable(58))
        self.give("Garage", 3)
        self.assertTrue(self.mission_reachable(58))

    def test_jizzy_waits_for_photo_opportunity(self) -> None:
        self.give("Loco Syndicate", 3)
        self.give("Garage", 3)
        self.assertFalse(self.mission_reachable(59))
        self.give("Triads", 1)
        self.assertTrue(self.mission_reachable(59))

    def test_wu_zi_mu_needs_only_cesar(self) -> None:
        self.give("Cesar", 2)
        self.assertTrue(self.mission_reachable(48))

    def test_vertical_bird_needs_only_mansion(self) -> None:
        self.give("Mansion", 1)
        self.assertTrue(self.mission_reachable(103))

    def give_los_santos_for_reuniting(self) -> None:
        for branch, count in (("Big Smoke", 4), ("Ryder", 4), ("OG Loc", 4), ("Cesar", 1), ("C.R.A.S.H.", 2)):
            self.give(branch, count)

    def test_riot_needs_grove_4_life_and_the_fourth_mansion_item(self) -> None:
        self.give_los_santos_for_reuniting()
        self.give("Sweet", 13)
        self.give("Mansion", 3)
        self.assertFalse(self.mission_reachable(108))
        self.give("Mansion", 4)
        self.assertTrue(self.mission_reachable(108))

    def test_los_desperados_waits_for_riot(self) -> None:
        self.give_los_santos_for_reuniting()
        self.give("Sweet", 14)
        self.give("Mansion", 3)
        self.assertFalse(self.mission_reachable(109))
        self.give("Mansion", 4)
        self.assertTrue(self.mission_reachable(109))


class TestSideContentTriggers(OutOfOrderTestBase):
    def test_trucking_waits_for_the_fourth_robbery(self) -> None:
        self.give("Catalina", 3)
        self.assertFalse(self.reachable(self.tier_location(96)))
        self.give("Catalina", 4)
        self.assertTrue(self.reachable(self.tier_location(96)))

    def test_driving_school_needs_the_garage_missions_and_the_truth(self) -> None:
        self.give("Garage", 3)
        self.assertFalse(self.reachable(self.tier_location(109)))
        self.give("The Truth", 2)
        self.assertTrue(self.reachable(self.tier_location(109)))

    def test_zero_needs_wear_flowers_and_the_truth(self) -> None:
        self.give("Garage", 1)
        self.assertFalse(self.mission_reachable(72))
        self.give("The Truth", 2)
        self.assertTrue(self.mission_reachable(72))


class TestWangCarsOffOutOfOrder(OutOfOrderTestBase):
    options = {**OUT_OF_ORDER, "include_wang_cars": False, "include_exports": 3}

    def test_wang_cars_and_exports_need_back_to_school(self) -> None:
        from ..export_list import EXPORT_LOCATION_NAMES

        self.give("Garage", 3)
        self.assertFalse(self.mission_reachable(67))
        self.assertFalse(self.reachable(EXPORT_LOCATION_NAMES[0]))
        self.give("The Truth", 2)
        self.assertTrue(self.mission_reachable(67))
        self.assertTrue(self.reachable(EXPORT_LOCATION_NAMES[0]))


class RecordingWriter:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write(self, data: bytes) -> None:
        self.lines.append(data.decode())

    async def drain(self) -> None:
        pass

    def close(self) -> None:
        pass

    async def wait_closed(self) -> None:
        pass


class TestClientTellsThePlugin(unittest.TestCase):
    def config_lines(self, mission_order: int, requirement: int) -> list[str]:
        import asyncio
        from ..client import GTASAContext

        async def run() -> list[str]:
            context = GTASAContext(None, None)
            writer = RecordingWriter()
            context.plugin_writer = writer
            context.mission_order = mission_order
            context.end_of_the_line_requirement = requirement
            context.send_plugin_config()
            await asyncio.sleep(0)
            await context.shutdown()
            return writer.lines

        return asyncio.run(run())

    def test_out_of_order_and_the_end_of_the_line_count_are_sent(self) -> None:
        lines = self.config_lines(1, 60)
        self.assertIn("CTRL:mission_order:1\n", lines)
        self.assertIn("CTRL:eotl_missions:60\n", lines)

    def test_linear_is_sent_too(self) -> None:
        self.assertIn("CTRL:mission_order:0\n", self.config_lines(0, 0))


class TestOutOfOrderTables(unittest.TestCase):
    def test_every_edge_names_story_missions_in_other_branches(self) -> None:
        from ..out_of_order.edges import OUT_OF_ORDER_EDGES

        story = set(STORY_MISSION_ORDER)
        for mission_id, prerequisites in OUT_OF_ORDER_EDGES.items():
            self.assertIn(mission_id, story)
            for prerequisite in prerequisites:
                with self.subTest(mission=mission_id, prerequisite=prerequisite):
                    self.assertIn(prerequisite, story)
                    self.assertNotEqual(branch_of(mission_id), branch_of(prerequisite))
