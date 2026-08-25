from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasAllCounts, Rule

if TYPE_CHECKING:
    from .world import GTASAWorld

def set_all_rules(world: GTASAWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def _mission_rule(world: GTASAWorld, *mission_ids: int) -> Rule:
    from .branches import effective_requirement
    from .items import PROGRESSIVE_BRANCH_ITEMS
    from .mission_list import get_start_index

    start_index = get_start_index(world)
    merged: dict[str, int] = {}
    for mission_id in mission_ids:
        for branch, count in effective_requirement(mission_id, start_index).items():
            if count > merged.get(branch, 0):
                merged[branch] = count
    return HasAllCounts({PROGRESSIVE_BRANCH_ITEMS[branch]: count for branch, count in merged.items()})

def _story_point_rule(world: GTASAWorld, position: int) -> Rule:
    from .mission_list import STORY_MISSION_ORDER

    if position <= 0:
        return HasAllCounts({})
    return _mission_rule(world, STORY_MISSION_ORDER[position - 1])

def _gate_at_story_points(world: GTASAWorld, requirements: dict[str, int]) -> None:
    location_cache = world.multiworld.regions.location_cache[world.player]
    for location_name, required_count in requirements.items():
        if location_name not in location_cache:
            continue
        world.set_rule(world.get_location(location_name), _story_point_rule(world, required_count))

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

    from .export_list import EXPORT_LOCATION_NAMES, EXPORT_REQUIREMENT
    from .horseshoe_list import HORSESHOE_LOCATION_NAMES, HORSESHOE_REQUIREMENT
    from .mission_list import get_optional_mission_requirements
    from .oyster_list import OYSTER_LOCATION_NAMES, OYSTER_REQUIREMENT
    from .tag_list import TAG_LOCATION_NAMES
    from .submission_tier_list import get_tier_requirements

    _gate_at_story_points(world, get_tier_requirements())
    _gate_at_story_points(world, get_optional_mission_requirements())

    from .gym_list import GYM_SKILL_ITEM, GYMS
    for gym in GYMS:
        if gym.location_name not in location_cache:
            continue
        world.set_rule(world.get_location(gym.location_name),
                       And(_story_point_rule(world, gym.required_count), Has(GYM_SKILL_ITEM)))

    _gate_at_story_points(world, dict.fromkeys(EXPORT_LOCATION_NAMES, EXPORT_REQUIREMENT))
    _gate_at_story_points(world, dict.fromkeys(OYSTER_LOCATION_NAMES, OYSTER_REQUIREMENT))
    from .items import TAGS_UNLOCK_ITEM
    from .tag_list import MISSION_SPRAYED_TAGS, MISSION_SPRAYED_TAGS_STORY_INDEX

    sprayed_by_mission = {TAG_LOCATION_NAMES[number - 1] for number in MISSION_SPRAYED_TAGS}
    reach_tagging_up_turf = _story_point_rule(world, MISSION_SPRAYED_TAGS_STORY_INDEX + 1)

    for location_name in TAG_LOCATION_NAMES:
        if location_name not in location_cache:
            continue
        if location_name in sprayed_by_mission:
            world.set_rule(world.get_location(location_name), reach_tagging_up_turf)
        else:
            world.set_rule(world.get_location(location_name), Has(TAGS_UNLOCK_ITEM))
    _gate_at_story_points(world, dict.fromkeys(HORSESHOE_LOCATION_NAMES, HORSESHOE_REQUIREMENT))

    if world.options.include_ammunation_shop:
        from .shop_list import SHOP_LOCATION_NAMES, INCLUDED_SHOP_SLOTS
        for slot, prerequisites in INCLUDED_SHOP_SLOTS.items():
            location_name = SHOP_LOCATION_NAMES[slot]
            if location_name not in location_cache:
                continue
            world.set_rule(world.get_location(location_name),
                           _mission_rule(world, *(LOCATION_NAME_TO_MISSION_ID[name] for name in prerequisites)))

    if world.options.include_street_races:
        from .items import STREET_RACES_ITEM
        from .submission_tier_list import SUBMISSION_TIERS, get_tier_names
        for tier_spec in SUBMISSION_TIERS:
            if tier_spec.requires_option != "include_street_races":
                continue
            for location_name in get_tier_names(tier_spec):
                if location_name not in location_cache:
                    continue
                world.set_rule(world.get_location(location_name),
                               And(_story_point_rule(world, tier_spec.required_progressive_missions),
                                   Has(STREET_RACES_ITEM)))

    from .submission_tier_list import SUBMISSION_TIERS, get_tier_names, unlock_item_for_tier
    for tier_spec in SUBMISSION_TIERS:
        unlock_item = unlock_item_for_tier(tier_spec)
        if not unlock_item:
            continue
        for location_name in get_tier_names(tier_spec):
            if location_name not in location_cache:
                continue
            world.set_rule(world.get_location(location_name),
                           And(_story_point_rule(world, tier_spec.required_progressive_missions),
                               Has(unlock_item)))

    from .challenge_list import CHALLENGES
    from .mission_list import get_mission_location_name
    from .stadium_list import STADIUM_EVENTS

    skill_gated: list[tuple[int, str]] = []
    if world.options.include_challenges:
        skill_gated += [(c.location_id, c.skill_item) for c in CHALLENGES if c.gates]
    if world.options.include_stadium_events:
        skill_gated += [(e.location_id, e.skill_item) for e in STADIUM_EVENTS if e.skill_item is not None]

    for location_id, skill_item in skill_gated:
        location_name = get_mission_location_name(location_id)
        if location_name in location_cache:
            world.set_rule(world.get_location(location_name), Has(skill_item))

def set_completion_condition(world: GTASAWorld) -> None:
    from .items import VICTORY_ITEM_NAME
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))
