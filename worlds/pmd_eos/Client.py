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
    checked_dungeon_flags: Dict[int, list] = {}
    checked_general_flags: Dict[int, list] = {}
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
            rom_name_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x3FFA80, 16, self.ram_mem_domain)])
            rom_name = bytes([byte for byte in rom_name_bytes[0] if byte != 0]).decode("UTF-8")
            if not rom_name.startswith("POKEDUN SORAC2SP"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.rom_slot_name = rom_name
        self.seed_verify = False
        name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE000, 16, self.ram_mem_domain)]))[0]
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name

        for i in range(25):
            self.checked_dungeon_flags[i] = []

        for i in range(16):
            self.checked_general_flags[i] = []

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        ctx.auth = self.player_name

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        #open_list_address = 0x08456D  # the address in Script Vars where the open list offset is
        #conquest_list_address = 0x09847D  # the address in Script Vars where the conquest list offset it
        #dung_lists_start_add = 0x2AB9EC
        dialga_complete = False

        try:
            if ctx.seed_name is None:
                return
            if not self.seed_verify:
                # Need to figure out where we are putting the seed and then update this
                seed = await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE0A0, 8, self.ram_mem_domain)])
                seed = seed[0].decode("UTF-8")[0:7]
                seed_name = ctx.seed_name[0:7]
                if seed != seed_name:
                    logger.info(
                        "ERROR: The ROM you loaded is for a different game of AP. "
                        "Please make sure the host has sent you the correct patch file,"
                        "and that you have opened the correct ROM."
                    )
                    raise bizhawk.ConnectorError("Loaded ROM is for Incorrect lobby.")
                self.seed_verify = True

            #read_state = await bizhawk.read(
            #    ctx.bizhawk_ctx,
            #    [
            #        (conquest_list_address, 2, self.ram_mem_domain),  # conquest list in Script_Vars
            #        (open_list_address, 2, self.ram_mem_domain),  # open list in Script_Vars
            #        # (0x416A580, 2, self.ram_mem_domain)
            #        # open memory location that we can put the list of collected items in
            #    ]
            #)
            # read the memory offsets to get the correct memory address for the dungeon lists
            #open_list_offset = read_state[1]  # 0x0194
            #conquest_list_offset = read_state[0]  # 0x01F4

            open_list_total_offset: int = await (self.load_script_variable_raw(79, ctx))
            conquest_list_total_offset: int = await (self.load_script_variable_raw(82, ctx))
            scenario_balance_offset = await (self.load_script_variable_raw(19, ctx))
            performance_progress_offset = await (self.load_script_variable_raw(78, ctx))
            generic_checks_offset = await (self.load_script_variable_raw(5, ctx))
            received_items_offset = await (self.load_script_variable_raw(16, ctx))
            # read the open and conquest lists with the offsets we found
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (conquest_list_total_offset, 24, self.ram_mem_domain),  # conquest list in Script_Vars_Values
                    (open_list_total_offset, 24, self.ram_mem_domain),  # open list in Script_Vars_Values
                    (scenario_balance_offset, 1, self.ram_mem_domain),
                    (performance_progress_offset, 1, self.ram_mem_domain),
                    (generic_checks_offset, 16, self.ram_mem_domain),
                    (received_items_offset, 2, self.ram_mem_domain)
                ]
            )
            # read the state of the dungeon lists
            open_list = read_state[1]
            conquest_list = read_state[0]
            scenario_balance_byte = read_state[2]
            performance_progress_bitfield = read_state[3]
            generic_checks_bitfield = read_state[4]
            received_index = int.from_bytes(read_state[5])

            locs_to_send = set()

            # Loop for receiving items.
            for i in range(len(ctx.items_received) - received_index):
                # get the item data from our item table
                item_data = item_table_by_id[ctx.items_received[received_index + i].item]
                if "Dungeons" in item_data.group:
                    item_memory_offset = item_data.memory_offset
                    # Since our open list is a byte array and our memory offset is bit based
                    # We have to grab our significant byte digits
                    sig_digit = item_memory_offset // 8
                    non_sig_digit = item_memory_offset % 8
                    if ((open_list[sig_digit] >> non_sig_digit) & 1) == 0:
                        # Since we are writing bytes, we need to add the bit to the specific byte
                        write_byte = open_list[sig_digit] | (1 << non_sig_digit)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (open_list_total_offset + sig_digit, int.to_bytes(write_byte),
                                 self.ram_mem_domain)],
                        )
                    await asyncio.sleep(0.1)
                elif "Progressive" in item_data.group:
                    if item_data.name == "Bag Upgrade":

                        if ((performance_progress_bitfield[0] >> 2) & 1) == 0:
                            write_byte = int.from_bytes(performance_progress_bitfield) + (0x1 << 2)
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        else:

                            write_byte = scenario_balance_byte[0] + 0x1
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (scenario_balance_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (received_items_offset, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100],
                         self.ram_mem_domain),
                    ]
                )


            # Check for set location flags.
            for byte_i, byte in enumerate(bytearray(conquest_list)):
                for j in range(8):
                    if j in self.checked_dungeon_flags[byte_i]:
                        continue  # if the number already exists in the dictionary, it's already been checked. Move on
                    if ((byte >> j) & 1) == 1:  # check if the bit j in each byte is on, meaning dungeon cleared
                        self.checked_dungeon_flags[byte_i] += [j]
                        # Note to self, change the Location table to be a Dictionary, so I don't have to loop
                        bit_number_dung = (byte_i * 8) + j
                        if bit_number_dung == 43:
                            dialga_complete = True
                        if bit_number_dung in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_dung].id)

            for byte_m, byte in enumerate(bytearray(generic_checks_bitfield)):
                for k in range(8):
                    if k in self.checked_general_flags[byte_m]:
                        continue
                    if ((byte >> k) & 1) == 1:
                        self.checked_general_flags[byte_m] += [k]
                        bit_number_gen = (byte_m * 8) + k + 200
                        if bit_number_gen in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_gen].id)

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

    async def load_script_variable_raw(self, var_id, ctx: "BizHawkClientContext") -> int:
        script_vars_values = 0x2AB9EC
        script_vars = 0x9DDF4
        var_mem_offset = await bizhawk.read(ctx.bizhawk_ctx,
                                            [((script_vars + (var_id << 0x4) + 0x4), 2, self.ram_mem_domain)])
        return script_vars_values + int.from_bytes(var_mem_offset[0], "little")
