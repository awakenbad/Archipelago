from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from . import mission_list
from .mission_list import REGION_ABBREVIATIONS, MISSION_DATA
from .tag_list import TAG_BASE_ID, TAG_LOCATION_NAMES, TAG_REGION
from .shop_list import SHOP_BASE_ID, SHOP_LOCATION_NAMES, SHOP_REGION, INCLUDED_SHOP_SLOTS

if TYPE_CHECKING:
    from .world import GTASAWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

LOCATION_NAME_TO_ID = {
    f"{REGION_ABBREVIATIONS[region]} Mission: {name}": mission_id
    for mission_id, name, region in MISSION_DATA
}
LOCATION_NAME_TO_ID.update({
    name: TAG_BASE_ID + i for i, name in enumerate(TAG_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: SHOP_BASE_ID + i for i, name in enumerate(SHOP_LOCATION_NAMES)
})

class GTASALocation(Location):
    game = "Grand Theft Auto: San Andreas"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: GTASAWorld) -> None:
    create_regular_locations(world)
    if world.options.include_tags:
        create_tag_locations(world)
    if world.options.include_ammunation_shop:
        create_shop_locations(world)

def create_regular_locations(world: GTASAWorld) -> None:
    for mission_id, name, region_name in MISSION_DATA:
        region = world.get_region(region_name)
        location_name = f"{REGION_ABBREVIATIONS[region_name]} Mission: {name}"
        location_id = LOCATION_NAME_TO_ID[location_name]
        region.add_locations({location_name: location_id}, GTASALocation)

def create_tag_locations(world: GTASAWorld) -> None:
    region = world.get_region(TAG_REGION)
    tag_locations = get_location_names_with_ids(TAG_LOCATION_NAMES)
    region.add_locations(tag_locations, GTASALocation)

def create_shop_locations(world: GTASAWorld) -> None:
    region = world.get_region(SHOP_REGION)
    included_names = [SHOP_LOCATION_NAMES[slot] for slot in INCLUDED_SHOP_SLOTS]
    shop_locations = get_location_names_with_ids(included_names)
    region.add_locations(shop_locations, GTASALocation)