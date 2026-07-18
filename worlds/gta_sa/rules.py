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

    world.set_rule(los_santos_to_badlands, Has("Progressive Mission", 23))
    world.set_rule(badlands_to_san_fierro, Has("Progressive Mission", 30))
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
    ]
    for index, location_name in enumerate(story_mission_order):
        location = world.get_location(location_name)
        required_count = index
        world.set_rule(location, Has("Progressive Mission", required_count))

    # Submissions whose vehicle can simply be found in the world from the start.
    submission_locations = [
        "LS Mission: Paramedic Level 12",
        "LS Mission: Firefighter Level 12",
        "LS Mission: Vigilante Level 12",
        "LS Mission: Taxi Driver 50 Fares",
    ]
    for location_name in submission_locations:
        location = world.get_location(location_name)
        world.set_rule(location, Has("Progressive Mission", 1))

    # These two have real in-game prerequisites, so they're gated on the story mission that
    # unlocks them (its position + 1, i.e. that mission must actually be completed):
    # the gym isn't enterable until Drive-Thru (position 4), and burglary isn't available
    # until Home Invasion (position 14) introduces the Boxville van.
    world.set_rule(
        world.get_location("LS Mission: Los Santos Gym Fight School"),
        Has("Progressive Mission", 5),
    )
    world.set_rule(
        world.get_location("LS Mission: Burglary $10,000 Stolen"),
        Has("Progressive Mission", 15),
    )

    if world.options.include_ammunation_shop:
        from .shop_list import SHOP_LOCATION_NAMES, INCLUDED_SHOP_SLOTS
        for slot, required_count in INCLUDED_SHOP_SLOTS.items():
            location = world.get_location(SHOP_LOCATION_NAMES[slot])
            world.set_rule(location, Has("Progressive Mission", required_count))

def set_completion_condition(world: GTASAWorld) -> None:
    world.set_completion_rule(Has("Progressive Mission", 26))