from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import GTASAWorld

ITEM_NAME_TO_ID = {
    "Progressive Map": 1,
    "Money": 2,
    "M4": 3,
    "Progressive Mission": 4,
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Progressive Map": ItemClassification.progression,
    "Money": ItemClassification.filler,
    "M4": ItemClassification.useful,
    "Progressive Mission": ItemClassification.progression,
}

class GTASAItem(Item):
    game = "Grand Theft Auto: San Andreas"

def get_random_filler_item_name(world: GTASAWorld) -> str:
    return "Money"

def create_item_with_correct_classification(world: GTASAWorld, name: str) -> GTASAItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return GTASAItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: GTASAWorld) -> None:
    itempool: list[Item] = [
        world.create_item("Progressive Mission"),
        world.create_item("Progressive Mission"),
        world.create_item("Progressive Mission"),
        world.create_item("Progressive Mission"),
    ]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool