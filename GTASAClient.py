import asyncio
from Utils import init_logging
init_logging("GTASAClient")

from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor, logger
from NetUtils import ClientStatus
from worlds.gta_sa.items import WEAPON_FILLER_ITEMS
from worlds.gta_sa.shop_list import INCLUDED_SHOP_SLOTS

def mission_check_to_location_id(mission_id: int) -> int:
    return mission_id

TAG_BASE_ID = 200

def tag_check_to_location_id(tag_index: int) -> int:
    return TAG_BASE_ID + tag_index

SHOP_BASE_ID = 300

def shop_check_to_location_id(slot_index: int) -> int:
    return SHOP_BASE_ID + slot_index

SUBMISSION_TIER_BASE_ID = 400

def submission_tier_check_to_location_id(slot_index: int) -> int:
    return SUBMISSION_TIER_BASE_ID + slot_index

# Fallback only - the real goal location arrives via slot_data on connect.
DEFAULT_GOAL_LOCATION_ID = 38

def sanitize_for_game(text: str, limit: int) -> str:
    """The in-game font only renders plain ASCII, and its display columns are narrow.
    Also guarantees no newline sneaks into the line-delimited plugin protocol."""
    return "".join(ch if 32 <= ord(ch) < 127 else "?" for ch in text)[:limit]

PICKUP_INDEX_TO_LOCATION_ID = {
    0: 81000,
    1: 81001,
    2: 81002,
}
ITEM_ID_TO_EFFECT = {
    2: ("money", 500),
    4: ("progressive_mission", None),
    5: ("health_upgrade", None),
    6: ("armor_upgrade", None),
    7: ("fire_immunity", None),
    8: ("stamina_upgrade", None),
    9: ("taxi_nitro", None),
    10: ("boxing_style", None),
    # IDs must match items.py's ITEM_NAME_TO_ID scheme exactly (11 + index into the same list).
    **{11 + i: ("weapon", name) for i, name in enumerate(WEAPON_FILLER_ITEMS)},
    # Traps: 40 + index into items.py's TRAP_ITEMS.
    40: ("trap_tires", None),
    41: ("trap_fat", None),
    42: ("trap_wanted", None),
    43: ("trap_carfire", None),
    # Utility fillers: 50 + index into items.py's UTILITY_FILLER_ITEMS.
    50: ("armor_refill", None),
    51: ("car_repair", None),
}

class GTASACommandProcessor(ClientCommandProcessor):
    def _cmd_tag(self, number: str = ""):
        """Highlight spray tag #<number> (1-100) on the in-game radar/map. Without a number, clears the highlight."""
        if not self.ctx.plugin_writer:
            self.output("The game plugin is not connected.")
            return
        if not number:
            self.ctx.plugin_writer.write(b"LOCATE:TAG:-1\n")
            asyncio.create_task(self.ctx.plugin_writer.drain())
            self.output("Cleared the tag highlight.")
            return
        try:
            tag_number = int(number)
        except ValueError:
            self.output(f"Not a number: {number}")
            return
        if not 1 <= tag_number <= 100:
            self.output("Tag number must be between 1 and 100.")
            return
        self.ctx.plugin_writer.write(f"LOCATE:TAG:{tag_number - 1}\n".encode())
        asyncio.create_task(self.ctx.plugin_writer.drain())
        self.output(f"Highlighting LS Tag #{tag_number} on the in-game map.")

    def _cmd_showlocations(self):
        self.output(f"Missing locations: {sorted(self.ctx.missing_locations)}")

class GTASAContext(CommonContext):
    game = "Grand Theft Auto: San Andreas"
    items_handling = 0b111
    command_processor = GTASACommandProcessor
    plugin_writer = None
    items_applied_count = 0
    death_link_enabled = False
    goal_location_id = DEFAULT_GOAL_LOCATION_ID
    shop_slot_contents: dict = {}

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super(GTASAContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def apply_pending_items(self) -> None:
        if not self.plugin_writer:
            return

        new_items = self.items_received[self.items_applied_count:]
        for item in new_items:
            effect = ITEM_ID_TO_EFFECT.get(item.item)
            if effect is None:
                logger.warning(f"Unrecognized item ID: {item.item}")
                continue

            effect_type, value = effect
            msg = f"GIVE:{effect_type}\n" if value is None else f"GIVE:{effect_type}:{value}\n"
            self.plugin_writer.write(msg.encode())
            asyncio.create_task(self.plugin_writer.drain())
        self.items_applied_count = len(self.items_received)

    def send_death_link_config(self) -> None:
        if not self.plugin_writer:
            return
        self.plugin_writer.write(f"GIVE:death_link:{int(self.death_link_enabled)}\n".encode())
        asyncio.create_task(self.plugin_writer.drain())

    def scout_shop_locations(self) -> None:
        """Ask the server what item sits at each Ammu-Nation slot, so the plugin can display it."""
        shop_ids = [SHOP_BASE_ID + slot for slot in INCLUDED_SHOP_SLOTS]
        existing = [i for i in shop_ids if i in self.missing_locations or i in self.checked_locations]
        if existing:
            asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": existing, "create_as_hint": 0}]))

    def push_shop_contents(self) -> None:
        if not self.plugin_writer or not self.shop_slot_contents:
            return
        for slot, text in self.shop_slot_contents.items():
            # Already-checked slots are pushed as empty, which reverts them to vanilla stock
            # in-game (real weapon, no interception) - the check is gone, the shop moves on.
            active = (SHOP_BASE_ID + slot) in self.missing_locations
            self.plugin_writer.write(f"SHOPITEM:{slot}:{text if active else ''}\n".encode())
        asyncio.create_task(self.plugin_writer.drain())

    async def check_goal_complete(self) -> None:
        if not self.finished_game and self.goal_location_id in self.checked_locations:
            self.finished_game = True
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    def push_sent_item(self, item_id: int, receiver_slot: int) -> None:
        """Announce in-game that a check we just found belonged to someone else's world."""
        if not self.plugin_writer:
            return
        try:
            item_name = self.item_names.lookup_in_slot(item_id, receiver_slot)
        except Exception:
            item_name = f"Item {item_id}"
        player_name = self.player_names.get(receiver_slot, "another player")
        text = sanitize_for_game(f"Sent {item_name} to {player_name}", 60)
        self.plugin_writer.write(f"SENT:{text}\n".encode())
        asyncio.create_task(self.plugin_writer.drain())

    def on_print_json(self, args: dict) -> None:
        super().on_print_json(args)
        if args.get("type") != "ItemSend":
            return

        item = args.get("item")
        receiver = args.get("receiving")
        if item is None or receiver is None:
            return

        # NetworkItem.player is the SENDING player for ItemSend packets.
        sender = getattr(item, "player", None)
        item_id = getattr(item, "item", None)
        if sender is None and isinstance(item, dict):
            sender, item_id = item.get("player"), item.get("item")
        if sender is None or item_id is None:
            return

        # Only our own finds, and only when they belong to somebody else - items we send to
        # ourselves are already announced when the plugin applies them.
        if sender != self.slot or receiver == self.slot:
            return

        self.push_sent_item(item_id, receiver)

    def on_deathlink(self, data: dict) -> None:
        super().on_deathlink(data)
        if self.plugin_writer:
            self.plugin_writer.write(b"GIVE:deathlink_kill\n")
            asyncio.create_task(self.plugin_writer.drain())

    def on_package(self, cmd: str, args: dict):
        if cmd == "ReceivedItems":
            self.apply_pending_items()
        elif cmd == "Connected":
            self.goal_location_id = args.get("slot_data", {}).get("goal_location_id", DEFAULT_GOAL_LOCATION_ID)
            self.death_link_enabled = bool(args.get("slot_data", {}).get("death_link", False))
            asyncio.create_task(self.update_death_link(self.death_link_enabled))
            self.send_death_link_config()
            self.scout_shop_locations()
            asyncio.create_task(self.check_goal_complete())
        elif cmd == "RoomUpdate":
            asyncio.create_task(self.check_goal_complete())
            self.push_shop_contents()
        elif cmd == "LocationInfo":
            for network_item in args["locations"]:
                if not SHOP_BASE_ID <= network_item.location < SHOP_BASE_ID + 100:
                    continue
                slot = network_item.location - SHOP_BASE_ID
                name = self.item_names.lookup_in_slot(network_item.item, network_item.player)
                if network_item.player != self.slot:
                    name += f" ({self.player_names.get(network_item.player, '?')})"
                self.shop_slot_contents[slot] = sanitize_for_game(name, 40)
            self.push_shop_contents()

async def handle_plugin_connection(reader, writer, ctx: GTASAContext):
    logger.info("Game plugin connected.")
    ctx.plugin_writer = writer
    ctx.apply_pending_items()
    ctx.send_death_link_config()
    ctx.push_shop_contents()
    while True:
        line = await reader.readline()
        if not line:
            break
        msg = line.decode().strip()

        if msg == "PLAYER_DIED":
            asyncio.create_task(ctx.send_death(f"{ctx.username} died in San Andreas"))
            continue

        if not msg.startswith("CHECK:"):
            continue

        parts = msg.split(":")
        if len(parts) != 3:
            logger.warning(f"Malformed check message from plugin: {msg}")
            continue

        _, check_type, raw_id = parts
        check_id = int(raw_id)

        if check_type == "MISSION":
            if check_id == -1:
                continue
            location_id = mission_check_to_location_id(check_id)
        elif check_type == "PICKUP":
            location_id = PICKUP_INDEX_TO_LOCATION_ID.get(check_id)
            if location_id is None:
                continue
        elif check_type == "TAG":
            location_id = tag_check_to_location_id(check_id)
        elif check_type == "SHOP":
            location_id = shop_check_to_location_id(check_id)
        elif check_type == "SUBLEVEL":
            location_id = submission_tier_check_to_location_id(check_id)
        else:
            logger.warning(f"Unknown check type from plugin: {check_type}")
            continue

        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

    logger.info("Game plugin disconnected.")
    ctx.plugin_writer = None
    writer.close()

async def main():
    ctx = GTASAContext(None, None)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    input_task = asyncio.create_task(console_loop(ctx), name="input loop")

    try:
        plugin_server = await asyncio.start_server(
            lambda r, w: handle_plugin_connection(r, w, ctx),
            "127.0.0.1", 12345
        )
        logger.info("Listening for the game plugin on 127.0.0.1:12345")
    except Exception as e:
        logger.error(f"Failed to start the plugin socket server: {e!r}")
        raise

    asyncio.create_task(plugin_server.serve_forever())

    await ctx.exit_event.wait()

    ctx.server_address = None
    await ctx.shutdown()

if __name__ == "__main__":
    asyncio.run(main())