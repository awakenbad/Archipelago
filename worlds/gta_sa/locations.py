from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import GTASAWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
REGION_ABBREVIATIONS = {
    "Los Santos": "LS",
    "Badlands": "BD",
    "San Fierro": "SF",
    "Las Venturas": "LV",
}

MISSION_DATA = [
    (11, "Big Smoke", "Los Santos"),
    (12, "Ryder", "Los Santos"),
    (13, "Tagging Up Turf", "Los Santos"),
    (14, "Cleaning The Hood", "Los Santos"),
    (39, "Badlands", "Badlands"),
    (49, "Wear Flowers In Your Hair", "San Fierro"),
    (75, "Monster", "Las Venturas"),
]

LOCATION_NAME_TO_ID = {
    f"{REGION_ABBREVIATIONS[region]} Mission: {name}": mission_id
    for mission_id, name, region in MISSION_DATA
}

class GTASALocation(Location):
    game = "Grand Theft Auto: San Andreas"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: GTASAWorld) -> None:
    create_regular_locations(world)

def create_regular_locations(world: GTASAWorld) -> None:
    for mission_id, name, region_name in MISSION_DATA:
        region = world.get_region(region_name)
        location_name = f"{REGION_ABBREVIATIONS[region_name]} Mission: {name}"
        location_id = LOCATION_NAME_TO_ID[location_name]
        region.add_locations({location_name: location_id}, GTASALocation)