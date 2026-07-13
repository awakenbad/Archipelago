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
    (15, "Drive-Thru", "Los Santos"),
    (16, "Nines And AK's", "Los Santos"),
    (17, "Drive-By", "Los Santos"),
    (18, "Sweet's Girl", "Los Santos"),
    (19, "Cesar Vialpando", "Los Santos"),
    (19, "Los Sepulcros", "Los Santos"),
    (20, "Doberman", "Los Santos"),
    (21, "Gray Imports", "Los Santos"),
    (22, "Home Invasion", "Los Santos"),
    (23, "Catalyst", "Los Santos"),
    (24, "Robbing Uncle Sam", "Los Santos"),
    (25, "OG Loc", "Los Santos"),
    (26, "Running Dog", "Los Santos"),
    (27, "Wrong Side of the Tracks", "Los Santos"),
    (28, "Just Business", "Los Santos"),
    (29, "Life's a Beach", "Los Santos"),
    (30, "Madd Dogg's Rhymes", "Los Santos"),
    (31, "Management Issues", "Los Santos"),
    (32, "House Party", "Los Santos"),
    (33, "Lowrider (High Stakes)", "Los Santos"),
    (34, "Reuniting The Families", "Los Santos"),
    (35, "The Green Sabre", "Los Santos"),
    (36, "Badlands", "Badlands"),
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