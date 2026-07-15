from worlds.AutoWorld import World

from . import items, locations, regions, rules
from . import options as gtasa_options
from .. import gta_sa


class GTASAWorld(World):
    """
    Grand Theft Auto: San Andreas is a 2004 open-world action-adventure game developed by Rockstar North.
    Set in 1992, the story follows Carl "CJ" Johnson, who returns to Los Santos after his mother's murder.
    Framed by corrupt cops, CJ travels across a massive fictional state to rebuild his gang and save his family.
    """

    game = "Grand Theft Auto: San Andreas"

    options_dataclass = gtasa_options.GTASAOptions
    options: gtasa_options.GTASAOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Los Santos"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)
    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.GTASAItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> dict:
        return {"death_link": self.options.death_link.value}