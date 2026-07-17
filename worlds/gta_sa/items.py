from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GTASAWorld

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

UTILITY_FILLER_ITEMS = [
    "Full Armor",
    "Car Repair",
]

ITEM_NAME_TO_ID = {
    "Money": 2,
    "Progressive Mission": 4,
    "Max Health Upgrade": 5,
    "Max Armor Upgrade": 6,
    "Fire Immunity": 7,
    "Infinite Sprint": 8,
    "Taxi Nitro": 9,
    "Boxing Style": 10,
    **{name: 11 + i for i, name in enumerate(WEAPON_FILLER_ITEMS)},
    # Weapons occupy 11-31; traps start at 40 to leave room for more weapons.
    **{name: 40 + i for i, name in enumerate(TRAP_ITEMS)},
    # Utility fillers start at 50, after the trap block.
    **{name: 50 + i for i, name in enumerate(UTILITY_FILLER_ITEMS)},
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Money": ItemClassification.filler,
    "Progressive Mission": ItemClassification.progression,
    "Max Health Upgrade": ItemClassification.useful,
    "Max Armor Upgrade": ItemClassification.useful,
    "Fire Immunity": ItemClassification.useful,
    "Infinite Sprint": ItemClassification.useful,
    "Taxi Nitro": ItemClassification.useful,
    "Boxing Style": ItemClassification.useful,
    **{name: ItemClassification.filler for name in WEAPON_FILLER_ITEMS},
    **{name: ItemClassification.trap for name in TRAP_ITEMS},
    **{name: ItemClassification.filler for name in UTILITY_FILLER_ITEMS},
}

class GTASAItem(Item):
    game = "Grand Theft Auto: San Andreas"

def get_random_filler_item_name(world: GTASAWorld) -> str:
    if world.random.random() * 100 < world.options.trap_percentage:
        return world.random.choice(TRAP_ITEMS)
    return world.random.choice(["Money", *WEAPON_FILLER_ITEMS, *UTILITY_FILLER_ITEMS])

def create_item_with_correct_classification(world: GTASAWorld, name: str) -> GTASAItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GTASAItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: GTASAWorld) -> None:
    itempool: list[Item] = (
        [world.create_item("Progressive Mission") for _ in range(26)]
        + [
            world.create_item("Max Health Upgrade"),
            world.create_item("Max Armor Upgrade"),
            world.create_item("Fire Immunity"),
            world.create_item("Infinite Sprint"),
            world.create_item("Taxi Nitro"),
            world.create_item("Boxing Style"),
        ]
    )
    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
