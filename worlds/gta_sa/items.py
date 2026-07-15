from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GTASAWorld

ITEM_NAME_TO_ID = {
    "Money": 2,
    "M4": 3,
    "Progressive Mission": 4,
    "Max Health Upgrade": 5,
    "Max Armor Upgrade": 6,
    "Fire Immunity": 7,
    "Infinite Sprint": 8,
    "Taxi Nitro": 9,
    "Boxing Style": 10,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Money": ItemClassification.filler,
    "M4": ItemClassification.useful,
    "Progressive Mission": ItemClassification.progression,
    "Max Health Upgrade": ItemClassification.useful,
    "Max Armor Upgrade": ItemClassification.useful,
    "Fire Immunity": ItemClassification.useful,
    "Infinite Sprint": ItemClassification.useful,
    "Taxi Nitro": ItemClassification.useful,
    "Boxing Style": ItemClassification.useful,
}

class GTASAItem(Item):
    game = "Grand Theft Auto: San Andreas"

def get_random_filler_item_name(world: GTASAWorld) -> str:
    return "Money"

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