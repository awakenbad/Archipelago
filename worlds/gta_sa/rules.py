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
    los_santos_to_badlands = world.get_entrance("Los Santos to Badlands")
    badlands_to_san_fierro = world.get_entrance("Badlands to San Fierro")
    san_fierro_to_las_venturas = world.get_entrance("San Fierro to Las Venturas")

    # Badlands opens when The Green Sabre (story position 26) has actually been completed.
    world.set_rule(los_santos_to_badlands, Has("Progressive Mission", 27))
    # San Fierro has no locations yet - keep its entrance above the total Progressive Mission
    # pool (36) so it stays unreachable until the region is actually populated. Revisit both
    # thresholds when their regions get locations.
    world.set_rule(badlands_to_san_fierro, Has("Progressive Mission", 37))
    world.set_rule(san_fierro_to_las_venturas, Has("Progressive Mission", 50))

def set_all_location_rules(world: GTASAWorld) -> None:
    story_mission_order = [
        "LS Mission: Big Smoke",                  # 0
        "LS Mission: Ryder",                      # 1
        "LS Mission: Tagging Up Turf",            # 2
        "LS Mission: Cleaning The Hood",          # 3
        "LS Mission: Drive-Thru",                 # 4
        "LS Mission: Nines And AK's",             # 5  - opens the parallel strands
        "LS Mission: Drive-By",                   # 6
        "LS Mission: Sweet's Girl",               # 7
        "LS Mission: Cesar Vialpando",            # 8
        "LS Mission: Lowrider (High Stakes)",     # 9  - only needs Cesar Vialpando
        "LS Mission: OG Loc",                     # 10
        "LS Mission: Running Dog",                # 11
        "LS Mission: Wrong Side of the Tracks",   # 12
        "LS Mission: Just Business",              # 13
        "LS Mission: Home Invasion",              # 14
        "LS Mission: Catalyst",                   # 15
        "LS Mission: Robbing Uncle Sam",          # 16
        "LS Mission: Life's a Beach",             # 17
        "LS Mission: Madd Dogg's Rhymes",         # 18
        "LS Mission: Management Issues",          # 19
        "LS Mission: House Party",                # 20
        "LS Mission: Burning Desire",             # 21 - needs Madd Dogg's Rhymes
        "LS Mission: Gray Imports",               # 22 - needs Burning Desire
        "LS Mission: Doberman",                   # 23 - needs Cesar Vialpando + Burning Desire
        "LS Mission: Los Sepulcros",              # 24 - needs Doberman
        "LS Mission: Reuniting The Families",     # 25
        "LS Mission: The Green Sabre",            # 26

        "BD Mission: Badlands",                   # 27
        "BD Mission: Local Liquor Store",         # 28
        "BD Mission: Body Harvest",               # 29
        "BD Mission: Small Town Bank",            # 30
        "BD Mission: Wu Zi Mu",                   # 31 - unlocks after 2 robberies
        "BD Mission: Tanker Commander",           # 32
        "BD Mission: Against All Odds",           # 33
        "BD Mission: Farewell, My Love...",       # 34
        "BD Mission: Are You Going to San Fierro?", # 35
    ]
    from .mission_list import get_story_mission_count

    for index, location_name in enumerate(story_mission_order[:get_story_mission_count(world)]):
        location = world.get_location(location_name)
        required_count = index
        world.set_rule(location, Has("Progressive Mission", required_count))

    # Tiered submissions (Paramedic/Firefighter/Vigilante levels, Taxi fares, Burglary loot):
    # every one of these can be started from the beginning of the game, so each tier carries the
    # same requirement as the activity itself.
    from .submission_tier_list import SUBMISSION_TIER_LOCATION_NAMES

    for location_name in SUBMISSION_TIER_LOCATION_NAMES:
        location = world.get_location(location_name)
        world.set_rule(location, Has("Progressive Mission", 1))

    # The gym is the only submission that isn't enterable until Drive-thru (position 4)
    world.set_rule(
        world.get_location("LS Mission: Los Santos Gym Fight School"),
        Has("Progressive Mission", 5),
    )

    if world.options.include_ammunation_shop:
        from .shop_list import SHOP_LOCATION_NAMES, INCLUDED_SHOP_SLOTS
        for slot, required_count in INCLUDED_SHOP_SLOTS.items():
            location = world.get_location(SHOP_LOCATION_NAMES[slot])
            world.set_rule(location, Has("Progressive Mission", required_count))

def set_completion_condition(world: GTASAWorld) -> None:
    # The required count is the goal mission's story position (see story_mission_order).
    if world.options.end_goal == "are_you_going_to_san_fierro":
        world.set_completion_rule(Has("Progressive Mission", 35))
    else:
        world.set_completion_rule(Has("Progressive Mission", 26))