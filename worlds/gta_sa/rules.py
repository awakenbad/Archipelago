from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import HasAllCounts, Rule

if TYPE_CHECKING:
    from .world import GTASAWorld

def set_all_rules(world: GTASAWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def _mission_rule(world: GTASAWorld, mission_id: int) -> Rule:
    from .branches import effective_requirement
    from .items import PROGRESSIVE_BRANCH_ITEMS
    from .mission_list import get_start_index

    requirement = effective_requirement(mission_id, get_start_index(world))
    return HasAllCounts({PROGRESSIVE_BRANCH_ITEMS[branch]: count for branch, count in requirement.items()})

def _story_point_rule(world: GTASAWorld, position: int) -> Rule:
    from .mission_list import STORY_MISSION_ORDER

    if position <= 0:
        return HasAllCounts({})
    return _mission_rule(world, STORY_MISSION_ORDER[position - 1])

def set_all_entrance_rules(world: GTASAWorld) -> None:
    world.set_rule(world.get_entrance("Los Santos to Badlands"), _mission_rule(world, 38))
    world.set_rule(world.get_entrance("Badlands to San Fierro"), _mission_rule(world, 47))
    world.set_rule(world.get_entrance("San Fierro to Las Venturas"), _mission_rule(world, 63))
    world.set_rule(world.get_entrance("Las Venturas to Return to Los Santos"), _mission_rule(world, 102))

def set_all_location_rules(world: GTASAWorld) -> None:
    from .mission_list import (
        LOCATION_NAME_TO_MISSION_ID,
        STORY_MISSION_LOCATION_ORDER,
        get_start_index,
        get_story_mission_count,
    )

    start_index = get_start_index(world)
    location_cache = world.multiworld.regions.location_cache[world.player]

    for index, location_name in enumerate(STORY_MISSION_LOCATION_ORDER[:get_story_mission_count(world)]):
        if index < start_index:
            continue
        world.set_rule(world.get_location(location_name),
                       _mission_rule(world, LOCATION_NAME_TO_MISSION_ID[location_name]))

    from .submission_tier_list import get_tier_requirements
    for location_name, required_count in get_tier_requirements().items():
        if location_name not in location_cache:
            continue
        world.set_rule(world.get_location(location_name), _story_point_rule(world, required_count))

    world.set_rule(world.get_location("LS Mission: Los Santos Gym Fight School"), _story_point_rule(world, 5))

    sf_gym = "SF Mission: San Fierro Gym Fight School"
    if sf_gym in location_cache:
        world.set_rule(world.get_location(sf_gym), _story_point_rule(world, 36))

    lv_gym = "LV Mission: Las Venturas Gym Fight School"
    if lv_gym in location_cache:
        world.set_rule(world.get_location(lv_gym), _story_point_rule(world, 54))

    from .mission_list import get_optional_mission_requirements
    for location_name, required_count in get_optional_mission_requirements().items():
        if location_name not in location_cache:
            continue
        world.set_rule(world.get_location(location_name), _story_point_rule(world, required_count))

    from .export_list import EXPORT_LOCATION_NAMES, EXPORT_REQUIREMENT
    for location_name in EXPORT_LOCATION_NAMES:
        if location_name in location_cache:
            world.set_rule(world.get_location(location_name), _story_point_rule(world, EXPORT_REQUIREMENT))

    if world.options.include_oysters:
        from .oyster_list import OYSTER_LOCATION_NAMES, OYSTER_REQUIREMENT
        for location_name in OYSTER_LOCATION_NAMES:
            if location_name in location_cache:
                world.set_rule(world.get_location(location_name), _story_point_rule(world, OYSTER_REQUIREMENT))

    if world.options.include_horseshoes:
        from .horseshoe_list import HORSESHOE_LOCATION_NAMES, HORSESHOE_REQUIREMENT
        for location_name in HORSESHOE_LOCATION_NAMES:
            if location_name in location_cache:
                world.set_rule(world.get_location(location_name), _story_point_rule(world, HORSESHOE_REQUIREMENT))

    if world.options.include_ammunation_shop:
        from .shop_list import SHOP_LOCATION_NAMES, INCLUDED_SHOP_SLOTS
        for slot, required_count in INCLUDED_SHOP_SLOTS.items():
            world.set_rule(world.get_location(SHOP_LOCATION_NAMES[slot]), _story_point_rule(world, required_count))

def set_completion_condition(world: GTASAWorld) -> None:
    from .items import VICTORY_ITEM_NAME
    from rule_builder.rules import Has
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))
