from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from . import mission_list
from .mission_list import REGION_ABBREVIATIONS, MISSION_DATA
from .tag_list import TAG_BASE_ID, TAG_LOCATION_NAMES, TAG_REGION, get_earnable_tag_names
from .snapshot_list import SNAPSHOT_BASE_ID, SNAPSHOT_LOCATION_NAMES, SNAPSHOT_REGION
from .horseshoe_list import HORSESHOE_BASE_ID, HORSESHOE_LOCATION_NAMES, HORSESHOE_REGION
from .export_list import EXPORT_BASE_ID, EXPORT_LOCATION_NAMES, EXPORT_REGION
from .oyster_list import OYSTER_BASE_ID, OYSTER_LOCATION_NAMES, OYSTER_REGION
from .shop_list import SHOP_BASE_ID, SHOP_LOCATION_NAMES, SHOP_REGION, INCLUDED_SHOP_SLOTS
from .submission_tier_list import (
    SUBMISSION_TIER_BASE_ID,
    SUBMISSION_TIER_LOCATION_NAMES,
    get_included_tier_names_by_region,
)

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
    name: SNAPSHOT_BASE_ID + i for i, name in enumerate(SNAPSHOT_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: HORSESHOE_BASE_ID + i for i, name in enumerate(HORSESHOE_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: EXPORT_BASE_ID + i for i, name in enumerate(EXPORT_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: OYSTER_BASE_ID + i for i, name in enumerate(OYSTER_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: SHOP_BASE_ID + i for i, name in enumerate(SHOP_LOCATION_NAMES)
})
LOCATION_NAME_TO_ID.update({
    name: SUBMISSION_TIER_BASE_ID + i
    for i, name in enumerate(SUBMISSION_TIER_LOCATION_NAMES)
})

class GTASALocation(Location):
    game = "Grand Theft Auto: San Andreas"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: GTASAWorld) -> None:
    create_regular_locations(world)
    create_submission_tier_locations(world)
    create_victory_location(world)
    if world.options.tag_checks.value:
        create_tag_locations(world)
    if world.options.snapshot_checks.value:
        create_snapshot_locations(world)
    if world.options.horseshoe_checks.value:
        create_horseshoe_locations(world)
    if world.options.include_exports:
        create_export_locations(world)
    if world.options.oyster_checks.value:
        create_oyster_locations(world)
    if world.options.include_ammunation_shop:
        create_shop_locations(world)

def create_victory_location(world: GTASAWorld) -> None:
    location_name = mission_list.get_goal_location_name(world)
    region = world.get_region(mission_list.get_goal_region(world))
    victory = GTASALocation(world.player, location_name, None, region)

    victory.place_locked_item(items.create_victory_item(world))
    region.locations.append(victory)

def create_submission_tier_locations(world: GTASAWorld) -> None:
    # Tiered submissions live in different regions (Trucking is in the Badlands), so skip the
    # ones whose region this seed's goal never requires visiting.
    included_regions = mission_list.get_included_regions(world)
    story_mission_count = mission_list.get_story_mission_count(world)
    for region_name, location_names in get_included_tier_names_by_region(
        world.options, story_mission_count, mission_list.get_start_index(world)
    ).items():
        if region_name not in included_regions:
            continue
        region = world.get_region(region_name)
        region.add_locations(get_location_names_with_ids(location_names), GTASALocation)

def create_regular_locations(world: GTASAWorld) -> None:
    included_regions = mission_list.get_included_regions(world)
    goal_mission_id = mission_list.get_goal_mission_id(world)
    story_mission_count = mission_list.get_story_mission_count(world)
    start_index = mission_list.get_start_index(world)
    optional_requirements = mission_list.get_optional_branch_requirements_by_id()

    for mission_id, name, region_name in MISSION_DATA:
        if region_name not in included_regions:
            continue
        if mission_id == goal_mission_id:
            continue
        if optional_requirements.get(mission_id, 0) >= story_mission_count:
            continue
        story_index = mission_list.get_story_index(mission_id)
        if story_index is not None and story_index < start_index:
            continue
        region = world.get_region(region_name)
        location_name = f"{REGION_ABBREVIATIONS[region_name]} Mission: {name}"
        location_id = LOCATION_NAME_TO_ID[location_name]
        region.add_locations({location_name: location_id}, GTASALocation)

def sample_collectibles(world: GTASAWorld, names: list[str], count: int) -> list[str]:
    if world.ut_passthrough is not None:
        chosen_ids = set(world.ut_passthrough.get("collectibles", ()))
        chosen = [name for name in names if LOCATION_NAME_TO_ID[name] in chosen_ids]
    else:
        count = min(count, len(names))
        chosen = world.random.sample(names, count)
    world.chosen_collectible_ids.update(LOCATION_NAME_TO_ID[name] for name in chosen)
    return chosen

def create_tag_locations(world: GTASAWorld) -> None:
    region = world.get_region(TAG_REGION)
    earnable = get_earnable_tag_names(mission_list.get_start_index(world))
    chosen = sample_collectibles(world, earnable, world.options.tag_checks.value)
    region.add_locations(get_location_names_with_ids(chosen), GTASALocation)

def create_snapshot_locations(world: GTASAWorld) -> None:
    # San Fierro is only generated for goals that reach it, so an out-of-scope seed simply has no
    # snapshots regardless of the option.
    if SNAPSHOT_REGION not in mission_list.get_included_regions(world):
        return
    region = world.get_region(SNAPSHOT_REGION)
    chosen = sample_collectibles(world, SNAPSHOT_LOCATION_NAMES, world.options.snapshot_checks.value)
    region.add_locations(get_location_names_with_ids(chosen), GTASALocation)

def create_export_locations(world: GTASAWorld) -> None:
    if EXPORT_REGION not in mission_list.get_included_regions(world):
        return
    from .export_list import EXPORT_REQUIREMENT
    if EXPORT_REQUIREMENT >= mission_list.get_story_mission_count(world):
        return
    region = world.get_region(EXPORT_REGION)
    region.add_locations(get_location_names_with_ids(EXPORT_LOCATION_NAMES), GTASALocation)

def create_oyster_locations(world: GTASAWorld) -> None:
    if OYSTER_REGION not in mission_list.get_included_regions(world):
        return
    from .oyster_list import OYSTER_REQUIREMENT
    if OYSTER_REQUIREMENT >= mission_list.get_story_mission_count(world):
        return
    region = world.get_region(OYSTER_REGION)
    chosen = sample_collectibles(world, OYSTER_LOCATION_NAMES, world.options.oyster_checks.value)
    region.add_locations(get_location_names_with_ids(chosen), GTASALocation)

def create_horseshoe_locations(world: GTASAWorld) -> None:
    if HORSESHOE_REGION not in mission_list.get_included_regions(world):
        return
    region = world.get_region(HORSESHOE_REGION)
    chosen = sample_collectibles(world, HORSESHOE_LOCATION_NAMES, world.options.horseshoe_checks.value)
    region.add_locations(get_location_names_with_ids(chosen), GTASALocation)

def create_shop_locations(world: GTASAWorld) -> None:
    region = world.get_region(SHOP_REGION)
    included_names = [SHOP_LOCATION_NAMES[slot] for slot in INCLUDED_SHOP_SLOTS]
    shop_locations = get_location_names_with_ids(included_names)
    region.add_locations(shop_locations, GTASALocation)