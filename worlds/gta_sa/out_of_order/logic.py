from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import HasAllCounts, HasFromList, Rule

from .edges import OUT_OF_ORDER_EDGES
from .triggers import EXPORT_TRIGGER, OPTIONAL_TRIGGERS, TIER_TRIGGERS, WANG_CARS_TRIGGERS

if TYPE_CHECKING:
    from ..world import GTASAWorld

END_OF_THE_LINE = 112


def apply_option_overrides(world: GTASAWorld) -> None:
    from ..options import EndGoal, StartingPoint

    world.options.starting_point.value = StartingPoint.option_los_santos
    world.options.end_goal.value = EndGoal.option_end_of_the_line


def requirement(mission_id: int) -> dict[str, int]:
    from ..branches import requirement_with_edges

    return requirement_with_edges(mission_id, OUT_OF_ORDER_EDGES)


def mission_rule(world: GTASAWorld, *mission_ids: int) -> Rule:
    from ..items import PROGRESSIVE_BRANCH_ITEMS

    merged: dict[str, int] = {}
    for mission_id in mission_ids:
        for branch, count in requirement(mission_id).items():
            if count > merged.get(branch, 0):
                merged[branch] = count
    return HasAllCounts({PROGRESSIVE_BRANCH_ITEMS[branch]: count for branch, count in merged.items()})


def story_point_rule(world: GTASAWorld, position: int) -> Rule:
    from ..mission_list import STORY_MISSION_ORDER

    if position <= 0:
        return HasAllCounts({})
    return mission_rule(world, STORY_MISSION_ORDER[position - 1])


def end_of_the_line_rule(world: GTASAWorld) -> Rule:
    from ..items import PROGRESSIVE_BRANCH_ITEMS

    return HasFromList(*PROGRESSIVE_BRANCH_ITEMS.values(),
                       count=world.options.end_of_the_line_requirement.value)


def early_branch_order(world: GTASAWorld, budget: int) -> list[str]:
    from ..branches import early_branch_order as linear_early_branch_order
    from ..mission_list import get_goal, get_start

    return linear_early_branch_order(get_start(world).story_index, get_goal(world).story_index,
                                     budget, OUT_OF_ORDER_EDGES)


def _gate(world: GTASAWorld, location_names: list[str], mission_ids: tuple[int, ...]) -> None:
    location_cache = world.multiworld.regions.location_cache[world.player]
    rule = mission_rule(world, *mission_ids)
    for location_name in location_names:
        if location_name in location_cache:
            world.set_rule(world.get_location(location_name), rule)


def set_location_rules(world: GTASAWorld) -> None:
    from ..export_list import EXPORT_LOCATION_NAMES
    from ..mission_list import get_mission_location_name
    from ..submission_tier_list import SUBMISSION_TIERS, get_tier_names

    for tier_spec in SUBMISSION_TIERS:
        if tier_spec.base_slot in TIER_TRIGGERS:
            _gate(world, get_tier_names(tier_spec), TIER_TRIGGERS[tier_spec.base_slot])

    optional = dict(OPTIONAL_TRIGGERS)
    if not world.options.include_wang_cars:
        optional.update(WANG_CARS_TRIGGERS)
        _gate(world, EXPORT_LOCATION_NAMES, EXPORT_TRIGGER)
    for mission_id, trigger in optional.items():
        _gate(world, [get_mission_location_name(mission_id)], trigger)

    world.set_rule(world.get_location(get_mission_location_name(END_OF_THE_LINE)), end_of_the_line_rule(world))
