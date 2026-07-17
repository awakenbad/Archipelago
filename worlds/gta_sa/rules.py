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
        "LS Mission: Big Smoke",
        "LS Mission: Ryder",
        "LS Mission: Tagging Up Turf",
        "LS Mission: Cleaning The Hood",
        "LS Mission: Drive-Thru",
        "LS Mission: Nines And AK's",
        "LS Mission: Drive-By",
        "LS Mission: Sweet's Girl",
        "LS Mission: Cesar Vialpando",
        "LS Mission: Los Sepulcros",
        "LS Mission: Doberman",
        "LS Mission: Gray Imports",
        "LS Mission: Home Invasion",
        "LS Mission: Catalyst",
        "LS Mission: Robbing Uncle Sam",
        "LS Mission: OG Loc",
        "LS Mission: Running Dog",
        "LS Mission: Wrong Side of the Tracks",
        "LS Mission: Just Business",
        "LS Mission: Life's a Beach",
        "LS Mission: Madd Dogg's Rhymes",
        "LS Mission: Management Issues",
        "LS Mission: House Party",
        "LS Mission: Lowrider (High Stakes)",
        "LS Mission: Reuniting The Families",
        "LS Mission: The Green Sabre",
    ]
    for index, location_name in enumerate(story_mission_order):
        location = world.get_location(location_name)
        required_count = index
        world.set_rule(location, Has("Progressive Mission", required_count))

    submission_locations = [
        "LS Mission: Paramedic Level 12",
        "LS Mission: Firefighter Level 12",
        "LS Mission: Vigilante Level 12",
        "LS Mission: Taxi Driver 50 Fares",
        "LS Mission: Burglary $10,000 Stolen",
    ]
    for location_name in submission_locations:
        location = world.get_location(location_name)
        world.set_rule(location, Has("Progressive Mission", 1))

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
    world.set_completion_rule(Has("Progressive Mission", 25))