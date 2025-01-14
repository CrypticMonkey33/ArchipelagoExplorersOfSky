from typing import TYPE_CHECKING, Optional, Set, List, Dict
import struct

from NetUtils import ClientStatus
from .Locations import EOSLocation
from .Items import EOS_item_table

import asyncio


import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class EoSClient(BizHawkClient):
    game = "Pokemon Mystery Dungeon: Explorers of Sky"
    system = "NDS"
    patch_suffix = ".apeos" #Might need to change the patch suffix
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]
    eUsed: List[int]
    room: int
    local_events: List[int]
    player_name: Optional[str]
    checked_flags: Dict[int, list] = {}

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.rom_slot_name = None
        self.seed_verify = False
        self.eUsed = []
        self.room = 0
        self.local_events = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x00, 15, "ROM")])
            rom_name = bytes([byte for byte in rom_name_bytes[0] if byte != 0]).decode("UTF-8")
            if not rom_name.startswith("POKEDUN SORAC2SP"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.rom_slot_name = rom_name
        self.seed_verify = False
        name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xDF0000, 16, "ROM")]))[0]
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.player_name

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger

        try:
            if ctx.seed_name is None:
                return
            if not self.seed_verify:
                # Need to figure out where we are putting the seed and then update this
                seed = await bizhawk.read(ctx.bizhawk_ctx, [(0x30F70, len(ctx.seed_name), "ROM")])
                seed = seed[0].decode("UTF-8")
                if seed != ctx.seed_name:
                    logger.info(
                        "ERROR: The ROM you loaded is for a different game of AP. "
                        "Please make sure the host has sent you the correct patch file,"
                        "and that you have opened the correct ROM."
                    )
                    raise bizhawk.ConnectorError("Loaded ROM is for Incorrect lobby.")
                self.seed_verify = True

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x4564, 59, "EWRAM"),
                    (0x2330, 2, "IWRAM"),
                    (0x3FE0, 1, "IWRAM"),
                    (0x304A, 1, "EWRAM"),
                    (0x304B, 1, "EWRAM"),
                    (0x304C, 4, "EWRAM"),
                    (0x3060, 6, "EWRAM"),
                    (0x4808, 2, "EWRAM"),
                    (0x4407, 1, "EWRAM"),
                    (0x2339, 1, "IWRAM"),
                ]
            )
            flags = read_state[0]
            #logo = bytes([byte for byte in read_state[6] if byte < 0x70]).decode("UTF-8")
            received_index = (read_state[7][0] << 8) + read_state[7][1]


            #if logo != "MLSSAP":
                #return

            locs_to_send = set()

            # Loop for receiving items. Item is written as an ID into 0x3057.
            # ASM reads the ID in a loop and give the player the item before resetting the RAM address to 0x0.
            # If RAM address isn't 0x0 yet break out and try again later to give the rest of the items
            for i in range(len(ctx.items_received) - received_index):
                item_data = items_by_id[ctx.items_received[received_index + i].item]
                b = await bizhawk.guarded_read(ctx.bizhawk_ctx, [(0x3057, 1, "EWRAM")], [(0x3057, [0x0], "EWRAM")])
                if b is None:
                    break
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x3057, [id_to_RAM(item_data.itemID)], "EWRAM"),
                        (0x4808, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100], "EWRAM"),
                    ],
                )
                await asyncio.sleep(0.1)

            # Check for set location flags. NEED TO UPDATE
            for byte_i, byte in enumerate(bytearray(flags)):
                for j in range(8):
                    if j in self.checked_flags[byte_i]:
                        continue
                    and_value = 1 << j
                    if byte & and_value != 0:
                        flag_id = byte_i * 8 + (j + 1)
                        room, item = find_key(roomCount, flag_id)
                        pointer_arr = await bizhawk.read(
                            ctx.bizhawk_ctx, [(ROOM_ARRAY_POINTER + ((room - 1) * 4), 4, "ROM")]
                        )
                        pointer = struct.unpack("<I", pointer_arr[0])[0]
                        pointer = pointer & 0xFFFFFF
                        offset = await bizhawk.read(ctx.bizhawk_ctx, [(pointer, 1, "ROM")])
                        offset = offset[0][0]
                        if offset != 0:
                            offset = 2
                        pointer += (item * 8) + 1 + offset
                        for key, value in beanstones.items():
                            if pointer == value:
                                pointer = key
                                break
                        if pointer in ctx.server_locations:
                            self.checked_flags[byte_i] += [j]
                            locs_to_send.add(pointer)

            if not ctx.finished_game and cackletta != 0 and current_room == 0x1C7:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass
