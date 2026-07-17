import asyncio
from Utils import init_logging
init_logging("GTASAClient")

from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor, logger
from NetUtils import ClientStatus
from worlds.gta_sa.items import WEAPON_FILLER_ITEMS

def mission_check_to_location_id(mission_id: int) -> int:
    return mission_id

TAG_BASE_ID = 200

def tag_check_to_location_id(tag_index: int) -> int:
    return TAG_BASE_ID + tag_index

GOAL_LOCATION_ID = 38

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

    def _cmd_testcheck(self, location_id: str):
        loc_id = int(location_id)
        self.ctx.locations_checked.add(loc_id)
        asyncio.create_task(self.ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}]))
        self.output(f"Sent check for location {loc_id}")

    def _cmd_showlocations(self):
        self.output(f"Missing locations: {sorted(self.ctx.missing_locations)}")

class GTASAContext(CommonContext):
    game = "Grand Theft Auto: San Andreas"
    items_handling = 0b111
    command_processor = GTASACommandProcessor
    plugin_writer = None
    items_applied_count = 0
    death_link_enabled = False

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
                print(f"Unrecognized item ID: {item.item}")
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

    async def check_goal_complete(self) -> None:
        if not self.finished_game and GOAL_LOCATION_ID in self.checked_locations:
            self.finished_game = True
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    def on_deathlink(self, data: dict) -> None:
        super().on_deathlink(data)
        if self.plugin_writer:
            self.plugin_writer.write(b"GIVE:deathlink_kill\n")
            asyncio.create_task(self.plugin_writer.drain())

    def on_package(self, cmd: str, args: dict):
        if cmd == "ReceivedItems":
            self.apply_pending_items()
        elif cmd == "Connected":
            self.death_link_enabled = bool(args.get("slot_data", {}).get("death_link", False))
            asyncio.create_task(self.update_death_link(self.death_link_enabled))
            self.send_death_link_config()
            asyncio.create_task(self.check_goal_complete())
        elif cmd == "RoomUpdate":
            asyncio.create_task(self.check_goal_complete())

async def handle_plugin_connection(reader, writer, ctx: GTASAContext):
    print("Plugin connected.")
    ctx.plugin_writer = writer
    ctx.apply_pending_items()
    ctx.send_death_link_config()
    while True:
        line = await reader.readline()
        if not line:
            break
        msg = line.decode().strip()
        print(f"From plugin: {msg}")

        if msg == "PLAYER_DIED":
            asyncio.create_task(ctx.send_death(f"{ctx.username} died in San Andreas"))
            continue

        if not msg.startswith("CHECK:"):
            continue

        parts = msg.split(":")
        if len(parts) != 3:
            print(f"Malformed check message: {msg}")
            continue

        _, check_type, raw_id = parts
        check_id = int(raw_id)

        if check_type == "MISSION":
            if check_id == -1:
                print("Unrecognized mission key received, skipping check")
                continue
            location_id = mission_check_to_location_id(check_id)
        elif check_type == "PICKUP":
            location_id = PICKUP_INDEX_TO_LOCATION_ID.get(check_id)
            if location_id is None:
                print(f"Pickup index {check_id} has no mapped AP location yet")
                continue
        elif check_type == "TAG":
            location_id = tag_check_to_location_id(check_id)
        else:
            print(f"Unknown check type: {check_type}")
            continue

        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])

    print("Plugin disconnected.")
    ctx.plugin_writer = None
    writer.close()

async def main():
    print("DEBUG: creating context")
    ctx = GTASAContext(None, None)

    print("DEBUG: starting server_task")
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    print("DEBUG: starting input_task")
    input_task = asyncio.create_task(console_loop(ctx), name="input loop")

    print("DEBUG: about to start plugin socket server")
    try:
        plugin_server = await asyncio.start_server(
            lambda r, w: handle_plugin_connection(r, w, ctx),
            "127.0.0.1", 12345
        )
        print("DEBUG: plugin socket server started successfully on port 12345")
    except Exception as e:
        print(f"DEBUG: FAILED to start plugin socket server: {e!r}")
        raise

    asyncio.create_task(plugin_server.serve_forever())

    print("DEBUG: entering exit_event.wait()")
    await ctx.exit_event.wait()
    print("DEBUG: exit_event was set, shutting down")

    ctx.server_address = None
    await ctx.shutdown()
    print("DEBUG: shutdown complete, main() returning")

if __name__ == "__main__":
    asyncio.run(main())