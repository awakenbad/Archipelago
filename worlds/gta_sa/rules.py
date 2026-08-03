from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import GTASAWorld

def set_all_rules(world: GTASAWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: GTASAWorld) -> None:
    from .mission_list import get_missions_required

    los_santos_to_badlands = world.get_entrance("Los Santos to Badlands")
    badlands_to_san_fierro = world.get_entrance("Badlands to San Fierro")
    san_fierro_to_las_venturas = world.get_entrance("San Fierro to Las Venturas")

    # Badlands opens when The Green Sabre (story position 26) has actually been completed.
    world.set_rule(los_santos_to_badlands, Has("Progressive Mission", get_missions_required(world, 27)))
    # San Fierro opens when Are You Going to San Fierro? (story position 35) is done.
    world.set_rule(badlands_to_san_fierro, Has("Progressive Mission", get_missions_required(world, 36)))
    # Las Venturas opens when Yay Ka-Boom-Boom (story position 53) is done.
    world.set_rule(san_fierro_to_las_venturas, Has("Progressive Mission", get_missions_required(world, 54)))
    # The Los Santos endgame opens when A Home in the Hills (story position 75) is done.
    world.set_rule(world.get_entrance("Las Venturas to Return to Los Santos"),
                   Has("Progressive Mission", get_missions_required(world, 76)))

def set_all_location_rules(world: GTASAWorld) -> None:
    from .mission_list import (
        STORY_MISSION_LOCATION_ORDER,
        get_missions_required,
        get_start_index,
        get_story_mission_count,
    )

    start_index = get_start_index(world)

    for index, location_name in enumerate(STORY_MISSION_LOCATION_ORDER[:get_story_mission_count(world)]):
        if index < start_index:
            continue
        location = world.get_location(location_name)
        world.set_rule(location, Has("Progressive Mission", get_missions_required(world, index)))

    # Tiered submissions. Every tier carries the same requirement as starting the activity
    # itself - Has(1) for the ones available from the off, more for Trucking, which needs
    # Tanker Commander done first. Out-of-scope regions have no locations to gate.
    from .submission_tier_list import get_tier_requirements

    for location_name, required_count in get_tier_requirements().items():
        if location_name not in world.multiworld.regions.location_cache[world.player]:
            continue
        location = world.get_location(location_name)
        world.set_rule(location, Has("Progressive Mission", get_missions_required(world, required_count)))

    # The gym is the only submission that isn't enterable until Drive-thru (position 4)
    world.set_rule(
        world.get_location("LS Mission: Los Santos Gym Fight School"),
        Has("Progressive Mission", get_missions_required(world, 5)),
    )

    sf_gym = "SF Mission: San Fierro Gym Fight School"
    if sf_gym in world.multiworld.regions.location_cache[world.player]:
        world.set_rule(world.get_location(sf_gym), Has("Progressive Mission", get_missions_required(world, 36)))

    lv_gym = "LV Mission: Las Venturas Gym Fight School"
    if lv_gym in world.multiworld.regions.location_cache[world.player]:
        world.set_rule(world.get_location(lv_gym), Has("Progressive Mission", get_missions_required(world, 54)))

    from .mission_list import get_optional_mission_requirements

    for location_name, required_count in get_optional_mission_requirements().items():
        if location_name not in world.multiworld.regions.location_cache[world.player]:
            continue
        world.set_rule(world.get_location(location_name),
                       Has("Progressive Mission", get_missions_required(world, required_count)))

    from .export_list import EXPORT_LOCATION_NAMES, EXPORT_REQUIREMENT
    for location_name in EXPORT_LOCATION_NAMES:
        if location_name in world.multiworld.regions.location_cache[world.player]:
            world.set_rule(world.get_location(location_name),
                           Has("Progressive Mission", get_missions_required(world, EXPORT_REQUIREMENT)))

    if world.options.include_oysters:
        from .oyster_list import OYSTER_LOCATION_NAMES, OYSTER_REQUIREMENT
        for location_name in OYSTER_LOCATION_NAMES:
            if location_name in world.multiworld.regions.location_cache[world.player]:
                world.set_rule(world.get_location(location_name),
                               Has("Progressive Mission", get_missions_required(world, OYSTER_REQUIREMENT)))

    if world.options.include_horseshoes:
        from .horseshoe_list import HORSESHOE_LOCATION_NAMES, HORSESHOE_REQUIREMENT
        for location_name in HORSESHOE_LOCATION_NAMES:
            if location_name not in world.multiworld.regions.location_cache[world.player]:
                continue
            world.set_rule(world.get_location(location_name),
                           Has("Progressive Mission", get_missions_required(world, HORSESHOE_REQUIREMENT)))

    if world.options.include_ammunation_shop:
        from .shop_list import SHOP_LOCATION_NAMES, INCLUDED_SHOP_SLOTS
        for slot, required_count in INCLUDED_SHOP_SLOTS.items():
            location = world.get_location(SHOP_LOCATION_NAMES[slot])
            world.set_rule(location, Has("Progressive Mission", get_missions_required(world, required_count)))

def set_completion_condition(world: GTASAWorld) -> None:
    from .items import VICTORY_ITEM_NAME
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))