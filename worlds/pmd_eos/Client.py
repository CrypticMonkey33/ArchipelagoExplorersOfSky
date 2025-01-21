from typing import TYPE_CHECKING, Optional, Set, List, Dict
import struct
import binascii

from NetUtils import ClientStatus
from .Locations import EOSLocation, EOS_location_table, location_Dict_by_id
from .Items import EOS_item_table, ItemData, item_table_by_id

import asyncio

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class EoSClient(BizHawkClient):
    game = "Pokemon Mystery Dungeon Explorers of Sky"
    system = "NDS"
    patch_suffix = ".apeos"  # Might need to change the patch suffix
    local_checked_locations: Set[int]
    goal_flag: int
    rom_slot_name: Optional[str]
    eUsed: List[int]
    room: int
    local_events: List[int]
    player_name: Optional[str]
    checked_flags: Dict[int, list] = {}
    test_rom_mem_domain = "Main RAM"
    ram_mem_domain = "Main RAM"

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
            rom_name_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x3FFA80, 16, self.test_rom_mem_domain)])
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
        name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE000, 16, self.test_rom_mem_domain)]))[0]
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name

        for i in range(25):
            self.checked_flags[i] = []

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.player_name

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        open_list_address = 0x08456D# the address in Script Vars where the open list offset is
        conquest_list_address = 0x09847D  # the address in Script Vars where the conquest list offset it
        dung_lists_start_add = 0x2AB9EC
        dialga_complete = False

        try:
            if ctx.seed_name is None:
                return
            if not self.seed_verify:
                # Need to figure out where we are putting the seed and then update this
                seed = await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE0A0, len(ctx.seed_name), self.test_rom_mem_domain)])
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
                    (conquest_list_address, 2, self.ram_mem_domain),  # conquest list in Script_Vars
                    (open_list_address, 2, self.ram_mem_domain),  # open list in Script_Vars
                    # (0x416A580, 2, self.ram_mem_domain)   # open memory location that we can put the list of collected items in
                ]
            )
            # read the memory offsets to get the correct memory address for the dungeon lists
            open_list_offset = read_state[1]
            conquest_list_offset = read_state[0]

            open_list_total_offset = (open_list_offset[0] << 8 | open_list_offset[1])
            conquest_list_total_offset = (conquest_list_offset[0] << 8 | conquest_list_offset[1])
            # read the open and conquest lists with the offsets we found
            read_state_second = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (conquest_list_total_offset + dung_lists_start_add, 24,
                     self.ram_mem_domain),  # conquest list in Script_Vars_Values
                    (open_list_total_offset + dung_lists_start_add, 24,
                     self.ram_mem_domain),  # open list in Script_Vars_Values
                    # (0x416A580, 2, "MAINROM")  # open memory location that we can put the list of collected items in
                ]
            )
            # read the state of the dungeon lists
            open_list = read_state_second[1]
            conquest_list = read_state_second[0]

            locs_to_send = set()

            new_open_list: bytes = bytes()
            new_conquest_list: bytes = bytes()

            # need to flip the words in the byte string due to it reading the wrong Endian
            for byte_i, byte in enumerate(conquest_list):
                mod_byte_i = byte_i % 4
                remain_byte_i = byte_i // 4
                flip_word = conquest_list[(4*remain_byte_i) + (3-mod_byte_i)]|0
                new_conquest_list += int.to_bytes(flip_word)

            for byte_i, byte in enumerate(open_list):
                mod_byte_i = byte_i % 4
                remain_byte_i = byte_i // 4
                flip_word = open_list[(4*remain_byte_i) + (3-mod_byte_i)]
                new_open_list += int.to_bytes(flip_word)

            # Loop for receiving items.
            for i in range(len(ctx.items_received)):
                # get the item data from our item table
                item_data = item_table_by_id[ctx.items_received[i].item]
                item_memory_offset = item_data.memory_offset
                # Since our open list is a byte array and our memory offset is bit based
                # We have to grab our significant byte digits
                sig_digit = item_memory_offset // 8
                non_sig_digit = item_memory_offset % 8
                if ((new_open_list[sig_digit] >> non_sig_digit) & 1) == 0:
                    # Since we are writing bytes, we need to add the bit to the specific byte
                    write_byte = new_open_list[sig_digit] | (1 << non_sig_digit)
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (open_list_total_offset + dung_lists_start_add
                             + ((4*sig_digit%4)+(3-sig_digit//4)), [write_byte], self.ram_mem_domain)
                        ],
                    )
                await asyncio.sleep(0.1)



            # Check for set location flags.
            for byte_i, byte in enumerate(bytearray(new_conquest_list)):
                for j in range(8):
                    if j in self.checked_flags[byte_i]:
                        continue  # if the number already exists in the dictionary, it's already been checked. Move on
                    if ((byte >> j) & 1) == 1:  # check if the bit j in each byte is on, meaning dungeon cleared
                        self.checked_flags[byte_i] += [j]
                        # Note to self, change the Location table to be a Dictionary, so I don't have to loop
                        byte_number = (byte_i * 8) + j
                        if byte_number == 43:
                            dialga_complete = True
                        if byte_number in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[byte_number].id)
#44
            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            if not ctx.finished_game and dialga_complete:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass
