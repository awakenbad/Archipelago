from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Item, ItemClassification
from Options import OptionError

from .branches import BRANCHES
from .challenge_list import CHALLENGES
from .skill_items import DEFAULT_SKILL_ITEMS, SKILL_ITEM_IDS, SKILL_ITEMS
from .stadium_list import STADIUM_EVENTS

if TYPE_CHECKING:
    from .world import GTASAWorld

PROGRESSIVE_BRANCH_ITEMS = {branch.name: f"Progressive {branch.name}" for branch in BRANCHES}

WEAPON_FILLER_ITEMS = [
    "Pistol",
    "Silenced Pistol",
    "Desert Eagle",
    "Shotgun",
    "Sawn-off Shotgun",
    "Combat Shotgun",
    "Micro Uzi",
    "MP5",
    "AK-47",
    "M4",
    "Tec-9",
    "Country Rifle",
    "Sniper Rifle",
    "Rocket Launcher",
    "Rocket Launcher HS",
    "Flamethrower",
    "Minigun",
    "Grenade",
    "Molotov Cocktail",
    "Tear Gas",
    "Satchel Charge",
]

TRAP_ITEMS = [
    "Flat Tires Trap",
    "Fat CJ Trap",
    "Wanted Level Trap",
    "Car Fire Trap",
    "Bad Weather Trap",
]

WEAPON_MASTERY_SKILLS = [
    "Pistol",
    "Silenced Pistol",
    "Desert Eagle",
    "Shotgun",
    "Sawn-off Shotgun",
    "Combat Shotgun",
    "Machine Pistol",
    "SMG",
    "AK-47",
    "M4",
    "Rifle",
]

WEAPON_MASTERY_ITEMS = [f"{name} Mastery" for name in WEAPON_MASTERY_SKILLS]

STREET_RACES_ITEM = "Street Races Unlock"

TAGS_UNLOCK_ITEM = "Tags Unlock"
OYSTERS_UNLOCK_ITEM = "Oysters Unlock"
HORSESHOES_UNLOCK_ITEM = "Horseshoes Unlock"

SUBMISSION_UNLOCK_ITEMS = [
    "Paramedic Unlock",
    "Firefighter Unlock",
    "Vigilante Unlock",
    "Taxi Unlock",
    "Pimping Unlock",
    "Burglary Unlock",
]

UTILITY_FILLER_ITEMS = [
    "Full Armor",
    "Car Repair",
]

ITEM_NAME_TO_ID = {
    "Money": 2,
    **{PROGRESSIVE_BRANCH_ITEMS[branch.name]: 100 + i for i, branch in enumerate(BRANCHES)},
    "Max Health Upgrade": 5,
    "Max Armor Upgrade": 6,
    "Fire Immunity": 7,
    "Infinite Sprint": 8,
    "Taxi Nitro": 9,
    "Boxing Style": 10,
    "Kung Fu Style": 3,
    "Kickboxing Style": 60,
    **{name: 11 + i for i, name in enumerate(WEAPON_FILLER_ITEMS)},
    # Weapons occupy 11-31; traps start at 40 to leave room for more weapons.
    **{name: 40 + i for i, name in enumerate(TRAP_ITEMS)},
    # Utility fillers start at 50, after the trap block.
    **{name: 50 + i for i, name in enumerate(UTILITY_FILLER_ITEMS)},
    # Weapon mastery starts at 61, after the Kickboxing style at 60.
    **{name: 61 + i for i, name in enumerate(WEAPON_MASTERY_ITEMS)},
    STREET_RACES_ITEM: 80,
    TAGS_UNLOCK_ITEM: 87,
    OYSTERS_UNLOCK_ITEM: 88,
    HORSESHOES_UNLOCK_ITEM: 89,
    **{name: 81 + i for i, name in enumerate(SUBMISSION_UNLOCK_ITEMS)},
    **SKILL_ITEM_IDS,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Money": ItemClassification.filler,
    **dict.fromkeys(PROGRESSIVE_BRANCH_ITEMS.values(), ItemClassification.progression),
    "Max Health Upgrade": ItemClassification.useful,
    "Max Armor Upgrade": ItemClassification.useful,
    "Fire Immunity": ItemClassification.useful,
    "Infinite Sprint": ItemClassification.useful,
    "Taxi Nitro": ItemClassification.useful,
    "Boxing Style": ItemClassification.useful,
    "Kung Fu Style": ItemClassification.useful,
    "Kickboxing Style": ItemClassification.useful,
    **dict.fromkeys(WEAPON_FILLER_ITEMS, ItemClassification.filler),
    **dict.fromkeys(TRAP_ITEMS, ItemClassification.trap),
    **dict.fromkeys(UTILITY_FILLER_ITEMS, ItemClassification.filler),
    **dict.fromkeys(WEAPON_MASTERY_ITEMS, ItemClassification.useful),
    STREET_RACES_ITEM: ItemClassification.progression,
    TAGS_UNLOCK_ITEM: ItemClassification.progression,
    OYSTERS_UNLOCK_ITEM: ItemClassification.progression,
    HORSESHOES_UNLOCK_ITEM: ItemClassification.progression,
    **dict.fromkeys(SUBMISSION_UNLOCK_ITEMS, ItemClassification.progression),
    # Skill items are useful by default and promoted to progression per seed - see
    # gating_skill_items(), which knows whether anything in scope actually needs them.
    **dict.fromkeys(SKILL_ITEM_IDS, ItemClassification.useful),
}

VICTORY_ITEM_NAME = "Victory"

class GTASAItem(Item):
    game = "Grand Theft Auto: San Andreas"

def create_victory_item(world: GTASAWorld) -> GTASAItem:
    return GTASAItem(VICTORY_ITEM_NAME, ItemClassification.progression, None, world.player)

def get_random_filler_item_name(world: GTASAWorld) -> str:
    if world.random.random() * 100 < world.options.trap_percentage:
        return world.random.choice(TRAP_ITEMS)
    return world.random.choice(["Money", *WEAPON_FILLER_ITEMS, *UTILITY_FILLER_ITEMS])

def gating_skill_items(world: GTASAWorld) -> set[str]:
    from .mission_list import get_included_regions, get_mission_region

    included_regions = get_included_regions(world)
    gating: set[str] = set()

    if world.options.include_challenges:
        for challenge in CHALLENGES:
            if challenge.gates and get_mission_region(challenge.location_id) in included_regions:
                gating.add(challenge.skill_item)

    if world.options.include_stadium_events:
        for event in STADIUM_EVENTS:
            if event.skill_item and get_mission_region(event.location_id) in included_regions:
                gating.add(event.skill_item)

    from .gym_list import GYM_SKILL_ITEM, GYMS
    for gym in GYMS:
        if get_mission_region(gym.location_id) in included_regions:
            gating.add(GYM_SKILL_ITEM)

    return gating

def create_item_with_correct_classification(world: GTASAWorld, name: str) -> GTASAItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    if name in SKILL_ITEM_IDS and name in gating_skill_items(world):
        classification = ItemClassification.progression
    return GTASAItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def gated_unlock_items(options) -> list[str]:
    from .submission_tier_list import unlocked_submission_items

    unlock_items: list[str] = []
    if options.include_street_races:
        unlock_items.append(STREET_RACES_ITEM)
    unlock_items += unlocked_submission_items(options)
    if options.tag_checks.value:
        unlock_items.append(TAGS_UNLOCK_ITEM)
    if options.oyster_checks.value:
        unlock_items.append(OYSTERS_UNLOCK_ITEM)
    if options.horseshoe_checks.value:
        unlock_items.append(HORSESHOES_UNLOCK_ITEM)
    return unlock_items

STARTING_UNLOCK_EXCLUSIONS = frozenset({OYSTERS_UNLOCK_ITEM})

def startable_unlock_items(unlock_items: list[str]) -> list[str]:
    return [name for name in unlock_items if name not in STARTING_UNLOCK_EXCLUSIONS]

def choose_starting_unlock(world: GTASAWorld, unlock_items: list[str]) -> str:
    if world.ut_passthrough is not None:
        chosen = world.ut_passthrough.get("starting_unlock", "")
        if chosen in unlock_items:
            return chosen
    return world.random.choice(unlock_items)

UPGRADE_ITEMS = [
    "Max Health Upgrade",
    "Max Armor Upgrade",
    "Fire Immunity",
    "Infinite Sprint",
    "Taxi Nitro",
    "Boxing Style",
]

def skill_item_names(world: GTASAWorld) -> tuple[list[str], list[str]]:
    from .mission_list import get_included_regions, get_mission_region

    gating = gating_skill_items(world)
    offered = list(DEFAULT_SKILL_ITEMS)
    if world.options.include_challenges:
        included_regions = get_included_regions(world)
        for challenge in CHALLENGES:
            if (challenge.skill_item not in offered
                    and get_mission_region(challenge.location_id) in included_regions):
                offered.append(challenge.skill_item)

    order = [item.name for item in SKILL_ITEMS]
    required = sorted(gating, key=order.index)
    optional = [name for name in offered if name not in gating]
    return required, optional

EARLY_ITEM_BRANCHES = (("Ryder", 1), ("Sweet", 2))

def set_early_items(world: GTASAWorld) -> None:
    state = CollectionState(world.multiworld)
    openings = sum(1 for location in world.multiworld.get_locations(world.player)
                   if location.address is not None and location.can_reach(state))

    early = world.multiworld.local_early_items[world.player]
    for branch, count in EARLY_ITEM_BRANCHES:
        if openings <= 0:
            break
        early[PROGRESSIVE_BRANCH_ITEMS[branch]] = min(count, openings)
        openings -= min(count, openings)

def create_all_items(world: GTASAWorld) -> None:
    from .branches import branch_pool_counts
    from .mission_list import get_goal, get_included_regions, get_start

    pool_counts = branch_pool_counts(get_start(world).story_index, get_goal(world).story_index)
    required: list[str] = []
    for branch in BRANCHES:
        required += [PROGRESSIVE_BRANCH_ITEMS[branch.name]] * pool_counts[branch.name]

    unlock_items = gated_unlock_items(world.options)

    startable = startable_unlock_items(unlock_items)
    if startable and world.options.starting_unlock:
        starting_unlock = choose_starting_unlock(world, startable)
        world.starting_unlock_item = starting_unlock
        world.multiworld.push_precollected(world.create_item(starting_unlock))
        unlock_items.remove(starting_unlock)

    required += unlock_items

    required_skills, optional_skills = skill_item_names(world)
    required += required_skills

    included_regions = get_included_regions(world)
    optional = list(UPGRADE_ITEMS)
    if "San Fierro" in included_regions:
        optional.append("Kung Fu Style")
    if "Las Venturas" in included_regions:
        optional.append("Kickboxing Style")
    optional += optional_skills

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    if len(required) > number_of_unfilled_locations:
        raise OptionError(
            f"Grand Theft Auto: San Andreas ({world.player_name}): these options leave only "
            f"{number_of_unfilled_locations} locations for {len(required)} required items. "
            "Turn on Include Tags, Include Snapshots or Include Ammu-Nation Shop, raise a "
            "submission slider, or pick a later End Goal."
        )

    names = required + optional[:number_of_unfilled_locations - len(required)]
    itempool: list[Item] = [world.create_item(name) for name in names]

    needed_number_of_filler_items = number_of_unfilled_locations - len(itempool)
    mastery_count = min(needed_number_of_filler_items, len(WEAPON_MASTERY_ITEMS))
    itempool += [world.create_item(name)
                 for name in world.random.sample(WEAPON_MASTERY_ITEMS, mastery_count)]

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items - mastery_count)]
    world.multiworld.itempool += itempool
