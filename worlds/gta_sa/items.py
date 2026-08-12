from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from Options import OptionError

from .branches import BRANCHES
from .challenge_list import CHALLENGES

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
    **{challenge.skill_item: challenge.skill_item_id for challenge in CHALLENGES},
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Money": ItemClassification.filler,
    **{name: ItemClassification.progression for name in PROGRESSIVE_BRANCH_ITEMS.values()},
    "Max Health Upgrade": ItemClassification.useful,
    "Max Armor Upgrade": ItemClassification.useful,
    "Fire Immunity": ItemClassification.useful,
    "Infinite Sprint": ItemClassification.useful,
    "Taxi Nitro": ItemClassification.useful,
    "Boxing Style": ItemClassification.useful,
    "Kung Fu Style": ItemClassification.useful,
    "Kickboxing Style": ItemClassification.useful,
    **{name: ItemClassification.filler for name in WEAPON_FILLER_ITEMS},
    **{name: ItemClassification.trap for name in TRAP_ITEMS},
    **{name: ItemClassification.filler for name in UTILITY_FILLER_ITEMS},
    **{name: ItemClassification.useful for name in WEAPON_MASTERY_ITEMS},
    **{challenge.skill_item: (ItemClassification.progression if challenge.gates else ItemClassification.useful)
       for challenge in CHALLENGES},
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

def create_item_with_correct_classification(world: GTASAWorld, name: str) -> GTASAItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GTASAItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: GTASAWorld) -> None:
    from .branches import branch_pool_counts
    from .mission_list import get_goal, get_included_regions, get_start

    pool_counts = branch_pool_counts(get_start(world).story_index, get_goal(world).story_index)
    itempool: list[Item] = []
    for branch in BRANCHES:
        item_name = PROGRESSIVE_BRANCH_ITEMS[branch.name]
        itempool += [world.create_item(item_name) for _ in range(pool_counts[branch.name])]

    itempool += [
        world.create_item("Max Health Upgrade"),
        world.create_item("Max Armor Upgrade"),
        world.create_item("Fire Immunity"),
        world.create_item("Infinite Sprint"),
        world.create_item("Taxi Nitro"),
        world.create_item("Boxing Style"),
    ]
    included_regions = get_included_regions(world)
    if "San Fierro" in included_regions:
        itempool.append(world.create_item("Kung Fu Style"))
    if "Las Venturas" in included_regions:
        itempool.append(world.create_item("Kickboxing Style"))

    if world.options.include_challenges:
        from .mission_list import get_mission_region
        added_skill_items: set[str] = set()
        for challenge in CHALLENGES:
            if challenge.skill_item in added_skill_items:
                continue
            if get_mission_region(challenge.location_id) in included_regions:
                itempool.append(world.create_item(challenge.skill_item))
                added_skill_items.add(challenge.skill_item)

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    if needed_number_of_filler_items < 0:
        raise OptionError(
            f"Grand Theft Auto: San Andreas ({world.player_name}): these options leave only "
            f"{number_of_unfilled_locations} locations for {number_of_items} required items. "
            "Set Include Submissions to Per Level, turn on Include Tags, Include Snapshots or "
            "Include Ammu-Nation Shop, or pick a later End Goal."
        )

    mastery_count = min(needed_number_of_filler_items, len(WEAPON_MASTERY_ITEMS))
    for name in world.random.sample(WEAPON_MASTERY_ITEMS, mastery_count):
        itempool.append(world.create_item(name))

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items - mastery_count)]
    world.multiworld.itempool += itempool
