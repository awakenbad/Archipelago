from Options import OptionError
from worlds.AutoWorld import World, WebWorld

from . import items, locations, mission_list, regions, rules
from . import options as gtasa_options
from .. import gta_sa

GENERATION_OPTION_NAMES = (
    "starting_point", "end_goal",
    "tag_checks", "snapshot_checks", "horseshoe_checks", "oyster_checks",
    "include_exports", "include_ammunation_shop", "include_challenges", "include_stadium_events",
    "courier_checks",
    "include_submissions",
    "paramedic_checks", "firefighter_checks", "vigilante_checks", "taxi_checks",
    "burglary_checks", "trucking_checks", "valet_checks", "pimping_checks",
    "quarry_checks", "gang_territory_target", "school_medals",
)

class GTASAWeb(WebWorld):
    option_groups = gtasa_options.option_groups


class GTASAWorld(World):
    """
    Grand Theft Auto: San Andreas is a 2004 open-world action-adventure game developed by Rockstar North.
    Set in 1992, the story follows Carl "CJ" Johnson, who returns to Los Santos after his mother's murder.
    Framed by corrupt cops, CJ travels across a massive fictional state to rebuild his gang and save his family.
    """

    game = "Grand Theft Auto: San Andreas"

    web = GTASAWeb()

    options_dataclass = gtasa_options.GTASAOptions
    options: gtasa_options.GTASAOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Los Santos"
    ut_can_gen_without_yaml = True
    ut_passthrough = None

    def generate_early(self) -> None:
        self.chosen_collectible_ids: set[int] = set()
        if hasattr(self.multiworld, "re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough:
            self.ut_passthrough = self.multiworld.re_gen_passthrough[self.game]
            for name, value in self.ut_passthrough.get("options", {}).items():
                option = getattr(self.options, name, None)
                if option is not None:
                    setattr(self.options, name, option.from_any(value))

        start = mission_list.get_start(self)
        goal = mission_list.get_goal(self)
        if start.story_index >= goal.story_index:
            raise OptionError(
                f"Grand Theft Auto: San Andreas ({self.player_name}): Starting Point "
                f"'{self.options.starting_point.current_key}' is not before End Goal "
                f"'{self.options.end_goal.current_key}', so the seed would have no story missions in it."
            )

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
        return {
            "death_link": self.options.death_link.value,
            "goal_mission_id": mission_list.get_goal_mission_id(self),
            "options": {name: getattr(self.options, name).value for name in GENERATION_OPTION_NAMES},
            "collectibles": sorted(self.chosen_collectible_ids),
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict) -> dict:
        return slot_data