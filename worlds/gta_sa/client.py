import asyncio
import functools
import importlib.resources
import os
import sys
import tempfile

import websockets

from Utils import init_logging
from CommonClient import server_loop, gui_enabled, logger
from NetUtils import ClientStatus

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION  # noqa
    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor

    class TrackerGameContext(CommonContext):
        pass

    tracker_loaded = False
    UT_VERSION = "Not found"
from .items import WEAPON_FILLER_ITEMS, WEAPON_MASTERY_SKILLS
from .branches import BRANCHES
from .skill_items import SKILL_ITEMS
from .shop_list import INCLUDED_SHOP_SLOTS, SHOP_BASE_ID
from .tag_list import TAG_BASE_ID, TAG_COUNT
from .snapshot_list import SNAPSHOT_BASE_ID, SNAPSHOT_COUNT
from .horseshoe_list import HORSESHOE_BASE_ID, HORSESHOE_COUNT
from .oyster_list import OYSTER_BASE_ID, OYSTER_COUNT
from .export_list import EXPORT_BASE_ID, EXPORT_COUNT
from .submission_tier_list import SUBMISSION_TIER_BASE_ID

COLLECTIBLE_BLOCKS = (
    ("TAG", TAG_BASE_ID, TAG_COUNT),
    ("SNAPSHOT", SNAPSHOT_BASE_ID, SNAPSHOT_COUNT),
    ("HORSESHOE", HORSESHOE_BASE_ID, HORSESHOE_COUNT),
    ("EXPORT", EXPORT_BASE_ID, EXPORT_COUNT),
    ("OYSTER", OYSTER_BASE_ID, OYSTER_COUNT),
)

CHECK_TYPE_BASE_IDS = {
    "TAG": TAG_BASE_ID,
    "SNAPSHOT": SNAPSHOT_BASE_ID,
    "HORSESHOE": HORSESHOE_BASE_ID,
    "EXPORT": EXPORT_BASE_ID,
    "OYSTER": OYSTER_BASE_ID,
    "SHOP": SHOP_BASE_ID,
    "SUBLEVEL": SUBMISSION_TIER_BASE_ID,
}

DEFAULT_GOAL_MISSION_ID = 38

EXPECTED_DISCONNECT_REASONS = (
    (ConnectionRefusedError, "the server refused the connection - check the address and port, and that it is running"),
    (asyncio.TimeoutError, "the connection timed out"),
    (websockets.exceptions.ConnectionClosed, "the server closed the connection"),
    (ConnectionResetError, "the server closed the connection"),
    (OSError, "the network connection dropped"),
)

def describe_disconnect(exception: BaseException | None) -> str | None:
    for exception_type, reason in EXPECTED_DISCONNECT_REASONS:
        if isinstance(exception, exception_type):
            return reason
    return None

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
    5: ("health_upgrade", None),
    6: ("armor_upgrade", None),
    7: ("fire_immunity", None),
    8: ("stamina_upgrade", None),
    9: ("taxi_nitro", None),
    10: ("boxing_style", None),
    3: ("kung_fu_style", None),
    60: ("kickboxing_style", None),
    **{61 + i: ("weapon_mastery", name) for i, name in enumerate(WEAPON_MASTERY_SKILLS)},
    # IDs must match items.py's ITEM_NAME_TO_ID scheme exactly (11 + index into the same list).
    **{11 + i: ("weapon", name) for i, name in enumerate(WEAPON_FILLER_ITEMS)},
    **{100 + i: ("progressive_mission", branch.name) for i, branch in enumerate(BRANCHES)},
    # Traps: 40 + index into items.py's TRAP_ITEMS.
    40: ("trap_tires", None),
    41: ("trap_fat", None),
    42: ("trap_wanted", None),
    43: ("trap_carfire", None),
    44: ("trap_weather", None),
    # Utility fillers: 50 + index into items.py's UTILITY_FILLER_ITEMS.
    50: ("armor_refill", None),
    51: ("car_repair", None),
    **{item.item_id: (item.effect, None) for item in SKILL_ITEMS},
}

class GTASACommandProcessor(ClientCommandProcessor):
    def _locate(self, wire_type: str, label: str, count: int, number: str) -> None:
        """Shared by the locate commands - they differ only in set, label and size."""
        if not self.ctx.plugin_writer:
            self.output("The game plugin is not connected.")
            return
        if not number:
            self.ctx.send_to_plugin(f"LOCATE:{wire_type}:-1\n")
            self.output(f"Cleared the {label} highlight.")
            return
        try:
            index = int(number)
        except ValueError:
            self.output(f"Not a number: {number}")
            return
        if not 1 <= index <= count:
            self.output(f"{label} number must be between 1 and {count}.")
            return
        self.ctx.send_to_plugin(f"LOCATE:{wire_type}:{index - 1}\n")
        self.output(f"Highlighting {label} #{index} on the in-game map.")

    def _cmd_tag(self, number: str = ""):
        """Highlight spray tag #<number> (1-100) on the in-game radar/map. Without a number, clears the highlight."""
        self._locate("TAG", "LS Tag", TAG_COUNT, number)

    def _cmd_snapshot(self, number: str = ""):
        """Highlight snapshot #<number> (1-50) on the in-game radar/map. Without a number, clears the highlight."""
        self._locate("SNAPSHOT", "SF Snapshot", SNAPSHOT_COUNT, number)

    def _cmd_horseshoe(self, number: str = ""):
        """Highlight horseshoe #<number> (1-50) on the in-game radar/map. Without a number, clears the highlight."""
        self._locate("HORSESHOE", "LV Horseshoe", HORSESHOE_COUNT, number)

    def _cmd_oyster(self, number: str = ""):
        """Highlight oyster #<number> (1-50) on the in-game radar/map. Without a number, clears the highlight."""
        self._locate("OYSTER", "Oyster", OYSTER_COUNT, number)

    def _cmd_showlocations(self):
        self.output(f"Missing locations: {sorted(self.ctx.missing_locations)}")

def _set_window_icon(manager) -> None:
    try:
        icon_bytes = importlib.resources.files(__package__).joinpath("icon.png").read_bytes()
    except Exception:
        return
    handle, path = tempfile.mkstemp(suffix="_gta_sa_icon.png")
    with os.fdopen(handle, "wb") as file:
        file.write(icon_bytes)
    manager.icon = path

class GTASAContext(TrackerGameContext):
    game = "Grand Theft Auto: San Andreas"
    tags = {"AP"}
    items_handling = 0b111
    command_processor = GTASACommandProcessor
    plugin_writer = None
    items_applied_count = 0
    death_link_enabled = False
    goal_mission_id = DEFAULT_GOAL_MISSION_ID
    shop_slot_contents: dict = {}
    shop_slot_flags: dict = {}

    def make_gui(self):
        ui = super().make_gui()

        class GTASAManager(ui):
            base_title = "Archipelago GTA: San Andreas Client" + (f" | UT {UT_VERSION}" if tracker_loaded else "")

            def build(self):
                container = super().build()
                _set_window_icon(self)
                return container

        return GTASAManager

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super(GTASAContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def send_to_plugin(self, message: str) -> None:
        writer = self.plugin_writer
        if writer is None:
            return
        try:
            writer.write(message.encode())
        except (ConnectionError, OSError):
            self.on_plugin_lost()
            return
        asyncio.create_task(self._drain_plugin(writer))

    async def _drain_plugin(self, writer: asyncio.StreamWriter) -> None:
        try:
            await writer.drain()
        except (ConnectionError, OSError):
            if writer is self.plugin_writer:
                self.on_plugin_lost()

    def handle_connection_loss(self, msg: str) -> None:
        exception = sys.exc_info()[1]
        reason = describe_disconnect(exception)
        if reason is None:
            super().handle_connection_loss(msg)
            return

        logger.warning(f"{msg} ({reason})")
        self._messagebox_connection_loss = self.gui_error(msg, exception)

    def is_connected_to_server(self) -> bool:
        return bool(self.server and self.server.socket.open and not self.server.socket.closed)

    def on_plugin_lost(self) -> None:
        if self.plugin_writer is None:
            return
        self.plugin_writer = None
        logger.info("Lost the connection to the game. Waiting for it to reconnect...")

    def apply_pending_items(self) -> None:
        """Push items to the plugin, each tagged with its position in items_received.

        The index is what makes this safe to repeat. The server replays the whole list on every
        connect, and items_applied_count only tracks what this process has sent - so it cannot be
        the thing that prevents double-granting. The plugin decides, against a mark stored in the
        GTA save, which indices it has already applied. That mark has to live in the save rather
        than here, because the save is what can roll back: loading an older one should legitimately
        re-grant the items it never saw.
        """
        if not self.plugin_writer:
            return

        for index, item in enumerate(self.items_received):
            if index < self.items_applied_count:
                continue

            effect = ITEM_ID_TO_EFFECT.get(item.item)
            if effect is None:
                logger.warning(f"Unrecognized item ID: {item.item}")
                continue

            effect_type, value = effect
            msg = f"GIVE:{index}:{effect_type}\n" if value is None else f"GIVE:{index}:{effect_type}:{value}\n"
            self.send_to_plugin(msg)
        self.items_applied_count = len(self.items_received)

    def send_death_link_config(self) -> None:
        self.send_to_plugin(f"CTRL:death_link:{int(self.death_link_enabled)}\n")

    def send_collectible_config(self) -> None:
        known = self.missing_locations | self.checked_locations
        if not known:
            return

        parts = []
        for name, base, count in COLLECTIBLE_BLOCKS:
            indices = sorted(loc - base for loc in known if base <= loc < base + count)
            if indices:
                parts.append(f"{name}={','.join(str(i) for i in indices)}")
        self.send_to_plugin(f"CTRL:collectibles:{';'.join(parts)}\n")

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
            sold = (SHOP_BASE_ID + slot) not in self.missing_locations
            self.send_to_plugin(f"SHOPITEM:{slot}:{'' if sold else text}\n")
            self.send_to_plugin(f"SHOPSOLD:{slot}:{int(sold)}\n")
            self.send_to_plugin(f"SHOPFLAGS:{slot}:{self.shop_slot_flags.get(slot, 0)}\n")

    async def report_goal_reached(self) -> None:
        if self.finished_game:
            return
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
        self.send_to_plugin(f"SENT:{text}\n")

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
        # CTRL, not GIVE: control messages carry no item index and must never be deduplicated
        # against one - a DeathLink kill is an event, not a thing you own a copy of.
        self.send_to_plugin("CTRL:deathlink_kill\n")

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd == "ReceivedItems":
            self.apply_pending_items()
        elif cmd == "Connected":
            self.goal_mission_id = args.get("slot_data", {}).get("goal_mission_id", DEFAULT_GOAL_MISSION_ID)
            self.death_link_enabled = bool(args.get("slot_data", {}).get("death_link", False))
            asyncio.create_task(self.update_death_link(self.death_link_enabled))
            self.send_death_link_config()
            self.send_collectible_config()
            self.scout_shop_locations()
        elif cmd == "RoomUpdate":
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
                self.shop_slot_flags[slot] = network_item.flags
            self.push_shop_contents()

async def handle_plugin_connection(reader, writer, ctx: GTASAContext):
    logger.info("Game plugin connected.")
    ctx.plugin_writer = writer
    # A freshly launched game knows nothing about what it has already been given, so replay the
    # full list and let it filter against its own saved mark. Sending only what this process has
    # not sent yet would starve it of exactly the items it needs to make that decision.
    ctx.items_applied_count = 0
    ctx.apply_pending_items()
    ctx.send_death_link_config()
    ctx.send_collectible_config()
    ctx.push_shop_contents()
    try:
        await read_plugin_messages(reader, ctx)
    except (ConnectionError, OSError):
        # The game was closed or crashed rather than shutting the socket down politely. Normal
        # enough that it does not deserve a traceback.
        pass
    finally:
        # Guard against a newer connection having already replaced ours - closing then would take
        # down a game that is currently running fine.
        if ctx.plugin_writer is writer:
            ctx.plugin_writer = None
            logger.info("Game disconnected. Waiting for it to reconnect...")
        try:
            writer.close()
        except (ConnectionError, OSError):
            pass

async def read_plugin_messages(reader, ctx: GTASAContext):
    while True:
        line = await reader.readline()
        if not line:
            return
        msg = line.decode(errors="replace").strip()

        if msg == "PLAYER_DIED":
            if ctx.death_link_enabled:
                asyncio.create_task(ctx.send_death(f"{ctx.username} died in San Andreas"))
            continue

        if not msg.startswith("CHECK:"):
            continue

        parts = msg.split(":")
        if len(parts) != 3:
            logger.warning(f"Malformed check message from plugin: {msg}")
            continue

        _, check_type, raw_id = parts
        try:
            check_id = int(raw_id)
        except ValueError:
            logger.warning(f"Non-numeric check ID from plugin: {msg}")
            continue

        if check_type == "MISSION":
            if check_id == -1:
                continue
            if check_id == ctx.goal_mission_id:
                await ctx.report_goal_reached()
                continue
            location_id = check_id
        elif check_type == "PICKUP":
            location_id = PICKUP_INDEX_TO_LOCATION_ID.get(check_id)
            if location_id is None:
                continue
        elif check_type in CHECK_TYPE_BASE_IDS:
            location_id = CHECK_TYPE_BASE_IDS[check_type] + check_id
        else:
            logger.warning(f"Unknown check type from plugin: {check_type}")
            continue

        ctx.locations_checked.add(location_id)
        if not ctx.is_connected_to_server():
            logger.info(f"Not connected to the server - check {location_id} will be sent on reconnect.")
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

def launch(*args):
    async def main():
        ctx = GTASAContext(None, None)

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        try:
            plugin_server = await asyncio.start_server(
                functools.partial(handle_plugin_connection, ctx=ctx),
                "127.0.0.1", 12345
            )
        except Exception as e:
            logger.error(f"Failed to start the plugin socket server: {e!r}")
            raise

        asyncio.create_task(plugin_server.serve_forever())

        if tracker_loaded:
            ctx.run_generator()

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()

        ctx.server_address = None
        await ctx.shutdown()

    init_logging("GTASAClient")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
