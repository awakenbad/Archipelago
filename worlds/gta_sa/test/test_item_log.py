import asyncio
import unittest

from NetUtils import NetworkItem, NetworkSlot, SlotType

from .test_out_of_order import RecordingWriter
from ..items import ITEM_NAME_TO_ID

OUR_GAME = "Grand Theft Auto: San Andreas"
OTHER_GAME = "Hollow Knight"
OTHER_LOCATION_ID = 777
PROGRESSION = 1


def lines_for(items: list[NetworkItem], other_player_name: str = "Knight") -> list[str]:
    from ..client import GTASAContext

    async def run() -> list[str]:
        context = GTASAContext(None, None)
        writer = RecordingWriter()
        context.plugin_writer = writer
        context.slot = 1
        context.slot_info = {
            1: NetworkSlot("CJ", OUR_GAME, SlotType.player),
            2: NetworkSlot(other_player_name, OTHER_GAME, SlotType.player),
        }
        context.player_names = {1: "CJ", 2: other_player_name}
        context.update_data_package({"games": {
            OUR_GAME: {"item_name_to_id": ITEM_NAME_TO_ID, "location_name_to_id": {}},
            OTHER_GAME: {"item_name_to_id": {}, "location_name_to_id": {"King's Pass Geo": OTHER_LOCATION_ID}},
        }})
        context.items_received = items
        context.apply_pending_items()
        await asyncio.sleep(0)
        await context.shutdown()
        return writer.lines

    return asyncio.run(run())


class TestItemLogInfo(unittest.TestCase):
    def test_each_item_is_described_before_it_is_given(self) -> None:
        lines = lines_for([NetworkItem(ITEM_NAME_TO_ID["Money"], OTHER_LOCATION_ID, 2, PROGRESSION)])
        self.assertEqual(lines, [
            "ITEMINFO:0:1:Money\tKnight\tHollow Knight\tKing's Pass Geo\n",
            "GIVE:0:money:500\n",
        ])

    def test_names_the_game_cannot_draw_are_made_safe(self) -> None:
        lines = lines_for([NetworkItem(ITEM_NAME_TO_ID["Money"], OTHER_LOCATION_ID, 2, 0)],
                          other_player_name="Knïght\tTwo")
        self.assertEqual(lines[0], "ITEMINFO:0:0:Money\tKn?ght?Two\tHollow Knight\tKing's Pass Geo\n")
