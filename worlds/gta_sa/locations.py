from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items
from . import mission_list
from .mission_list import LOCATION_NAME_TO_MISSION_ID
from .tag_list import TAG_BASE_ID, TAG_LOCATION_NAMES, TAG_REGION, get_earnable_tag_names
from .snapshot_list import SNAPSHOT_BASE_ID, SNAPSHOT_LOCATION_NAMES, SNAPSHOT_REGION
from .horseshoe_list import HORSESHOE_BASE_ID, HORSESHOE_LOCATION_NAMES, HORSESHOE_REGION
from .export_list import EXPORT_BASE_ID, EXPORT_LOCATION_NAMES, EXPORT_REGION
from .oyster_list import OYSTER_BASE_ID, OYSTER_LOCATION_NAMES, OYSTER_REGION
from .shop_list import (
    SHOP_BASE_ID,
    SHOP_LOCATION_NAMES,
    SHOP_REGION,
    INCLUDED_SHOP_SLOTS,
    required_story_count,
)
from .submission_tier_list import (
    SUBMISSION_TIER_BASE_ID,
    SUBMISSION_TIER_LOCATION_NAMES,
    get_included_tier_names_by_region,
)
from .challenge_list import CHALLENGE_LOCATION_IDS
from .stadium_list import STADIUM_LOCATION_IDS

if TYPE_CHECKING:
    from .world import GTASAWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.

LOCATION_NAME_TO_ID = dict(LOCATION_NAME_TO_MISSION_ID)
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
    if world.options.include_wang_cars:
        create_wang_cars_locations(world)
    elif world.options.include_exports.value:
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
    item_gated = (set(mission_list.get_optional_branch_mission_ids(mission_list.WANG_CARS_BRANCH))
                  if world.options.include_wang_cars else set())

    for mission_id, _, region_name in mission_list.MISSION_DATA:
        if mission_id in item_gated:
            continue
        if region_name not in included_regions:
            continue
        if mission_id in CHALLENGE_LOCATION_IDS and not world.options.include_challenges:
            continue
        if mission_id in STADIUM_LOCATION_IDS and not world.options.include_stadium_events:
            continue
        if mission_id == goal_mission_id:
            continue
        if optional_requirements.get(mission_id, 0) >= story_mission_count:
            continue
        story_index = mission_list.get_story_index(mission_id)
        if story_index is not None and story_index < start_index:
            continue
        region = world.get_region(region_name)
        location_name = mission_list.get_mission_location_name(mission_id)
        region.add_locations({location_name: LOCATION_NAME_TO_ID[location_name]}, GTASALocation)

def sample_collectibles(world: GTASAWorld, names: list[str], count: int) -> list[str]:
    if world.ut_passthrough is not None:
        chosen_ids = set(world.ut_passthrough.get("collectibles", ()))
        chosen = [name for name in names if LOCATION_NAME_TO_ID[name] in chosen_ids]
    else:
        count = min(count, len(names))
        chosen = world.random.sample(names, count)
    world.chosen_collectible_ids.update(LOCATION_NAME_TO_ID[name] for name in chosen)
    return chosen

def create_collectible_locations(world: GTASAWorld, region_name: str, names: list[str],
                                 count: int) -> None:
    region = world.get_region(region_name)
    chosen = sample_collectibles(world, names, count)
    region.add_locations(get_location_names_with_ids(chosen), GTASALocation)

def scoped_collectibles_included(world: GTASAWorld, region_name: str, requirement: int) -> bool:
    if region_name not in mission_list.get_included_regions(world):
        return False
    return requirement < mission_list.get_story_mission_count(world)

def create_scoped_collectible_locations(world: GTASAWorld, region_name: str, names: list[str],
                                        count: int, requirement: int) -> None:
    if not scoped_collectibles_included(world, region_name, requirement):
        return
    create_collectible_locations(world, region_name, names, count)

def create_tag_locations(world: GTASAWorld) -> None:
    from .tag_list import TAG_REQUIREMENT
    earnable = get_earnable_tag_names(mission_list.get_start_index(world))
    create_scoped_collectible_locations(world, TAG_REGION, earnable,
                                        world.options.tag_checks.value, TAG_REQUIREMENT)

def create_snapshot_locations(world: GTASAWorld) -> None:
    create_collectible_locations(world, SNAPSHOT_REGION, SNAPSHOT_LOCATION_NAMES,
                                 world.options.snapshot_checks.value)

def create_oyster_locations(world: GTASAWorld) -> None:
    create_collectible_locations(world, OYSTER_REGION, OYSTER_LOCATION_NAMES,
                                 world.options.oyster_checks.value)

def create_horseshoe_locations(world: GTASAWorld) -> None:
    create_collectible_locations(world, HORSESHOE_REGION, HORSESHOE_LOCATION_NAMES,
                                 world.options.horseshoe_checks.value)

def wang_cars_location_names(world: GTASAWorld) -> list[str]:
    from .export_list import get_included_export_names
    return (mission_list.get_optional_branch_location_names(mission_list.WANG_CARS_BRANCH)
            + get_included_export_names(world.options.include_exports.value))

def create_wang_cars_locations(world: GTASAWorld) -> None:
    region = world.get_region(world.origin_region_name)
    region.add_locations(get_location_names_with_ids(wang_cars_location_names(world)), GTASALocation)

def create_export_locations(world: GTASAWorld) -> None:
    from .export_list import EXPORT_REQUIREMENT, get_included_export_names
    if EXPORT_REGION not in mission_list.get_included_regions(world):
        return
    if EXPORT_REQUIREMENT >= mission_list.get_story_mission_count(world):
        return
    region = world.get_region(EXPORT_REGION)
    included = get_included_export_names(world.options.include_exports.value)
    region.add_locations(get_location_names_with_ids(included), GTASALocation)

def create_shop_locations(world: GTASAWorld) -> None:
    region = world.get_region(SHOP_REGION)
    story_mission_count = mission_list.get_story_mission_count(world)
    included_names = [
        SHOP_LOCATION_NAMES[slot]
        for slot, prerequisites in INCLUDED_SHOP_SLOTS.items()
        if required_story_count(prerequisites) < story_mission_count
    ]
    shop_locations = get_location_names_with_ids(included_names)
    region.add_locations(shop_locations, GTASALocation)