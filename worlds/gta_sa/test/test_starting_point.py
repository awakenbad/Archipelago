import unittest

from Options import OptionError
from test.general import setup_multiworld

from ..mission_list import MILESTONES, STORY_MISSION_LOCATION_ORDER
from ..tag_list import MISSION_SPRAYED_TAGS, TAG_LOCATION_NAMES
from ..world import GTASAWorld
from .bases import GTASATestBase


def get_valid_start_goal_pairs():
    starts = [milestone for milestone in MILESTONES if milestone.start_option_value is not None]
    goals = [milestone for milestone in MILESTONES if milestone.goal_option_value is not None]
    return [(start, goal) for start in starts for goal in goals if start.story_index < goal.story_index]


class TestStartingPointGrid(unittest.TestCase):
    """Every start/goal pair has to generate, with a pool sized to the gap between the two.

    A new milestone row is offered as both ends of a seed at once, so this grid is what catches
    a row that only works from one side.
    """

    def test_every_pair_generates_a_correctly_sized_pool(self) -> None:
        for start, goal in get_valid_start_goal_pairs():
            with self.subTest(start=start.start_option_value, goal=goal.goal_option_value):
                multiworld = setup_multiworld(GTASAWorld, options={
                    "starting_point": start.start_option_value,
                    "end_goal": goal.goal_option_value,
                })
                pool = [item for item in multiworld.itempool if item.name == "Progressive Mission"]
                self.assertEqual(len(pool), goal.story_index - start.story_index)

    def test_no_pair_creates_a_mission_before_its_start(self) -> None:
        for start, goal in get_valid_start_goal_pairs():
            with self.subTest(start=start.start_option_value, goal=goal.goal_option_value):
                multiworld = setup_multiworld(GTASAWorld, options={
                    "starting_point": start.start_option_value,
                    "end_goal": goal.goal_option_value,
                })
                created = {location.name for location in multiworld.get_locations(1)}
                already_passed = set(STORY_MISSION_LOCATION_ORDER[:start.story_index])
                self.assertEqual(created & already_passed, set())

    def test_every_pair_can_reach_all_of_its_locations(self) -> None:
        # The failure this guards against is a location that logic believes is reachable while the
        # save has already consumed it - it generates cleanly and dies at fill.
        for start, goal in get_valid_start_goal_pairs():
            with self.subTest(start=start.start_option_value, goal=goal.goal_option_value):
                multiworld = setup_multiworld(GTASAWorld, options={
                    "starting_point": start.start_option_value,
                    "end_goal": goal.goal_option_value,
                })
                state = multiworld.get_all_state(False)
                unreachable = [
                    location.name
                    for location in multiworld.get_locations(1)
                    if not location.can_reach(state)
                ]
                self.assertEqual(unreachable, [])


class TestFlyingSchoolBoundary(unittest.TestCase):
    """Learning to Fly is the one story mission that also pays out as submission tiers.

    Passing the mission passes every lesson, so a start beyond it must not create those ten
    locations - they would be unearnable, and fill could put progression behind them.
    """

    def test_lessons_are_dropped_only_past_learning_to_fly(self) -> None:
        learning_to_fly = STORY_MISSION_LOCATION_ORDER.index("LV Mission: Learning to Fly")
        for start, goal in get_valid_start_goal_pairs():
            if goal.story_index <= learning_to_fly:
                continue
            with self.subTest(start=start.start_option_value, goal=goal.goal_option_value):
                multiworld = setup_multiworld(GTASAWorld, options={
                    "starting_point": start.start_option_value,
                    "end_goal": goal.goal_option_value,
                    "include_submissions": "per_level",
                })
                created = {location.name for location in multiworld.get_locations(1)}
                lessons = {name for name in created if "Flying School" in name}
                if start.story_index > learning_to_fly:
                    self.assertEqual(lessons, set())
                else:
                    self.assertEqual(len(lessons), 10)


class TestMissionSprayedTags(unittest.TestCase):
    """Tagging Up Turf sprays six tags itself, so a later start has already spent them."""

    def test_later_starts_drop_them_and_a_los_santos_start_keeps_them(self) -> None:
        sprayed = {TAG_LOCATION_NAMES[number - 1] for number in MISSION_SPRAYED_TAGS}
        for milestone in MILESTONES:
            if milestone.start_option_value is None:
                continue
            with self.subTest(start=milestone.start_option_value):
                multiworld = setup_multiworld(GTASAWorld, options={
                    "starting_point": milestone.start_option_value,
                    "end_goal": "end_of_the_line",
                    "include_tags": True,
                })
                created = {location.name for location in multiworld.get_locations(1)}
                if milestone.story_index == 0:
                    self.assertEqual(sprayed - created, set())
                else:
                    self.assertEqual(sprayed & created, set())

class TestStartGoalValidation(unittest.TestCase):
    def test_start_at_or_past_the_goal_is_rejected(self) -> None:
        with self.assertRaises(OptionError):
            setup_multiworld(GTASAWorld, options={
                "starting_point": "las_venturas",
                "end_goal": "yay_ka_boom_boom",
            })


class TestBadlandsStart(GTASATestBase):
    options = {"starting_point": "badlands", "end_goal": "a_home_in_the_hills"}

    def test_los_santos_story_missions_are_not_created(self) -> None:
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(created & set(STORY_MISSION_LOCATION_ORDER[:27]), set())

    def test_los_santos_side_content_survives(self) -> None:
        # Los Santos never re-locks, so everything there that isn't a passed story mission stays.
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        for location_name in (
            "LS Mission: Los Santos Gym Fight School",
            "LS Tag: #4",
            "Ammu-Nation: Pistol",
            "LS Mission: Paramedic Level 1",
        ):
            self.assertIn(location_name, created)

    def test_los_santos_side_content_needs_nothing(self) -> None:
        # Its requirements all sit below the starting point, so they clamp to zero.
        for location_name in ("LS Mission: Los Santos Gym Fight School", "Ammu-Nation: Sawn-off Shotgun"):
            location = self.world.get_location(location_name)
            self.assertTrue(location.can_reach(self.multiworld.state))

    def test_first_badlands_mission_needs_nothing(self) -> None:
        location = self.world.get_location("BD Mission: Badlands")
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_are_you_going_to_san_fierro_requires_eight(self) -> None:
        # Story position 35, minus the 27 the starting point already spent.
        location = self.world.get_location("BD Mission: Are You Going to San Fierro?")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:7]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.multiworld.state.collect(progressive_missions[7])
        self.assertTrue(location.can_reach(self.multiworld.state))

    def test_completion_requires_48_progressive_missions(self) -> None:
        # A Home in the Hills is story position 75, minus the 27 the starting point spent.
        progressive_missions = self.get_items_by_name("Progressive Mission")
        self.assertEqual(len(progressive_missions), 49)

        for item in progressive_missions[:47]:
            self.multiworld.state.collect(item)
        self.assertBeatable(False)

        self.multiworld.state.collect(progressive_missions[47])
        self.assertBeatable(True)


class TestLasVenturasStart(GTASATestBase):
    options = {"starting_point": "las_venturas", "end_goal": "a_home_in_the_hills"}

    def test_earlier_regions_keep_their_side_content(self) -> None:
        # Map access is cumulative, so San Fierro and the Badlands are still open.
        created = {location.name for location in self.multiworld.get_locations(self.player)}
        for location_name in (
            "SF Snapshot: #1",
            "BD Mission: Trucking Level 1",
            "SF Mission: Valet 3 Cars Parked",
            "SF Mission: Driving School - The 360",
        ):
            self.assertIn(location_name, created)

    def test_flying_school_lessons_are_still_earnable(self) -> None:
        # Learning to Fly sits at story position 58, past this start, so the lessons remain ahead.
        location = self.world.get_location("LV Mission: Flying School - Takeoff")
        progressive_missions = self.get_items_by_name("Progressive Mission")

        for item in progressive_missions[:3]:
            self.multiworld.state.collect(item)
        self.assertFalse(location.can_reach(self.multiworld.state))

        self.collect_by_name("Progressive Mission")
        self.assertTrue(location.can_reach(self.multiworld.state))
