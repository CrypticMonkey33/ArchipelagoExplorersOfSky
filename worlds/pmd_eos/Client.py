from typing import TYPE_CHECKING, Optional, Set, List, Dict
import array
import binascii

from NetUtils import ClientStatus
from .Locations import EOSLocation, EOS_location_table, location_Dict_by_id
from .Items import EOS_item_table, ItemData, item_table_by_id, lootbox_table
from random import Random
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
    goal_complete = False
    bag_given = False
    macguffins_collected = 0
    macguffin_unlock_amount = 0
    cresselia_feather_acquired = False
    dialga_complete = False
    item_boxes_collected: List[ItemData] = []
    random: Random = Random()

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


    async def update_received_items(self, ctx: "BizHawkClientContext", received_items_offset, received_index, i) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [
                (received_items_offset, [(received_index + i + 1) // 0x100, (received_index + i + 1) % 0x100],
                 self.ram_mem_domain),
            ]
        )

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:

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
        await (ctx.send_msgs([{"cmd": "Set", "key": "Dungeon Missions", "default": {}, "want_reply": True}]))
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.rom_slot_name = rom_name
        self.seed_verify = False
        name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE000, 16, self.ram_mem_domain)]))[0]
        name = bytes([byte for byte in name_bytes if byte != 0]).decode("UTF-8")
        self.player_name = name
        #self.macguffin_unlock_amount = ctx.slot_data["ShardFragmentAmount"]

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
            ctx.stored_data
            open_list_total_offset: int = await (self.load_script_variable_raw(0x4F, ctx))
            conquest_list_total_offset: int = await (self.load_script_variable_raw(0x52, ctx))
            scenario_balance_offset = await (self.load_script_variable_raw(0x13, ctx))
            performance_progress_offset = await (self.load_script_variable_raw(0x4E, ctx))
            scenario_subx_offset = await (self.load_script_variable_raw(0x5, ctx))
            received_items_offset = await (self.load_script_variable_raw(0x16, ctx))
            scenario_main_offset = await (self.load_script_variable_raw(0x3, ctx))
            scenario_main_bitfield_offset = await (self.load_script_variable_raw(0x11, ctx))
            special_episode_offset = await (self.load_script_variable_raw(0x4B,  ctx))
            item_backup_offset = await (self.load_script_variable_raw(0x64, ctx))
            # read the open and conquest lists with the offsets we found
            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (conquest_list_total_offset, 24, self.ram_mem_domain),  # conquest list in Script_Vars_Values
                    (open_list_total_offset, 24, self.ram_mem_domain),  # open list in Script_Vars_Values
                    (scenario_balance_offset, 1, self.ram_mem_domain),
                    (performance_progress_offset, 5, self.ram_mem_domain),
                    (scenario_subx_offset, 16, self.ram_mem_domain),
                    (received_items_offset, 2, self.ram_mem_domain),
                    (scenario_main_offset, 1, self.ram_mem_domain),
                    (special_episode_offset, 1, self.ram_mem_domain),
                    (scenario_main_bitfield_offset, 1, self.ram_mem_domain),
                    (item_backup_offset, 4, self.ram_mem_domain),
                ]
            )
            # make sure we are actually on the start screen before checking items and such
            scenario_main_list = read_state[6]
            if int.from_bytes(scenario_main_list) == 0:
                return

            if self.macguffin_unlock_amount == 0:
                self.macguffin_unlock_amount = ctx.slot_data["ShardFragmentAmount"]

            # read the state of the dungeon lists
            open_list: array.array[int] = array.array('i', [item for item in read_state[1]])
            conquest_list: array.array[int] = array.array('i', [item for item in read_state[0]])
            scenario_balance_byte = array.array('i', [item for item in read_state[2]])
            performance_progress_bitfield: array.array[int] = array.array('i', [item for item in read_state[3]])
            scenario_subx_bitfield: array.array[int] = array.array('i', [item for item in read_state[4]])
            received_index = int.from_bytes(read_state[5])
            special_episode_bitfield = int.from_bytes(read_state[7])
            scenario_main_bitfield_list: array.array[int] = array.array('i', [item for item in read_state[8]])
            item_backup_bytes: array.array[int] = array.array('i', [item for item in read_state[9]])
            locs_to_send = set()


            # Loop for receiving items.
            for i in range(len(ctx.items_received) - received_index):
                # get the item data from our item table
                item_data = item_table_by_id[ctx.items_received[received_index + i].item]
                if (("EarlyDungeons" in item_data.group) or ("LateDungeons" in item_data.group)
                        or ("Dojo Dungeons" in item_data.group) or ("BossDungeons" in item_data.group)):
                    item_memory_offset = item_data.memory_offset
                    # Since our open list is a byte array and our memory offset is bit based
                    # We have to grab our significant byte digits
                    sig_digit = item_memory_offset // 8
                    non_sig_digit = item_memory_offset % 8
                    if ((open_list[sig_digit] >> non_sig_digit) & 1) == 0:
                        # Since we are writing bytes, we need to add the bit to the specific byte
                        write_byte = open_list[sig_digit] | (1 << non_sig_digit)
                        open_list[sig_digit] = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (open_list_total_offset + sig_digit, int.to_bytes(write_byte),
                                 self.ram_mem_domain)],
                        )

                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                    await asyncio.sleep(0.1)
                elif "Special Dungeons" in item_data.group:
                    item_memory_offset = item_data.memory_offset
                    if (special_episode_bitfield >> item_memory_offset & 1) == 0:
                        # Since we are writing bytes, we need to add the bit to the specific byte
                        write_byte = special_episode_bitfield | (1 << item_memory_offset)
                        special_episode_bitfield = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (special_episode_offset, int.to_bytes(write_byte),
                                 self.ram_mem_domain)],
                        )
                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Generic" in item_data.group:
                    if item_data.name == "Bag Upgrade":

                        if ((performance_progress_bitfield[0] >> 2) & 1) == 0:
                            write_byte = performance_progress_bitfield[0] + (0x1 << 2)
                            performance_progress_bitfield[0] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        else:

                            write_byte = scenario_balance_byte[0] + 0x1
                            scenario_balance_byte[0] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (scenario_balance_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Macguffin" in item_data.group:
                    if item_data.name == "Relic Fragment Shard":
                        self.macguffins_collected += 1
                        if self.macguffins_collected == self.macguffin_unlock_amount:
                            item_memory_offset = 0x26  # the location in memory of Hidden Land
                            sig_digit = item_memory_offset // 8
                            non_sig_digit = item_memory_offset % 8
                            if ((open_list[sig_digit] >> non_sig_digit) & 1) == 0:
                                # Since we are writing bytes, we need to add the bit to the specific byte
                                write_byte = open_list[sig_digit] | (1 << non_sig_digit)
                                open_list[sig_digit] = write_byte
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [
                                        (open_list_total_offset + sig_digit, int.to_bytes(write_byte),
                                         self.ram_mem_domain)],
                                )

                            await asyncio.sleep(0.1)
                    elif item_data.name == "Cresselia Feather":
                        self.cresselia_feather_acquired = True

                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Item" in item_data.group:
                    self.item_boxes_collected += [item_data]
                    await self.update_received_items(ctx, received_items_offset, received_index, i)

                elif "Trap" in item_data.group:
                    if item_data.name == "Team Name Trap":
                        if ((performance_progress_bitfield[4] >> 0) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] + 0x1
                            performance_progress_bitfield[4] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                    elif item_data.name == "Confusion Trap":
                        if ((performance_progress_bitfield[4] >> 1) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] + (0x1 << 1)
                            performance_progress_bitfield[4] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                    elif item_data.name == "Nap Time!":
                        if ((scenario_main_bitfield_list[0] >> 3) & 1) == 0:
                            write_byte = scenario_main_bitfield_list[0] + (0x1 << 3)
                            scenario_main_bitfield_list[0] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (scenario_main_bitfield_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)

            # Check for set location flags.
            for byte_i, byte in enumerate(conquest_list):
                for j in range(8):
                    if j in self.checked_dungeon_flags[byte_i]:
                        continue  # if the number already exists in the dictionary, it's already been checked. Move on
                    if ((byte >> j) & 1) == 1:  # check if the bit j in each byte is on, meaning dungeon cleared
                        self.checked_dungeon_flags[byte_i] += [j]
                        # Note to self, change the Location table to be a Dictionary, so I don't have to loop
                        bit_number_dung = (byte_i * 8) + j
                        if (ctx.slot_data["Goal"] == 0) and (bit_number_dung == 43):
                            self.goal_complete = True
                            locs_to_send.add(700)
                        elif (ctx.slot_data["Goal"] == 1) and (bit_number_dung == 67):
                            self.goal_complete = True
                            locs_to_send.add(700)
                        elif (ctx.slot_data["Goal"] == 1) and (bit_number_dung == 43):
                            self.dialga_complete = True
                        if bit_number_dung in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_dung].id)

            for byte_m, byte in enumerate(scenario_subx_bitfield):
                for k in range(8):
                    if k in self.checked_general_flags[byte_m]:
                        continue
                    if ((byte >> k) & 1) == 1:
                        self.checked_general_flags[byte_m] += [k]
                        bit_number_gen = (byte_m * 8) + k + 300
                        if bit_number_gen in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_gen].id)

            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            if self.cresselia_feather_acquired and self.dialga_complete:
                item_memory_offset = 0x67  # the location in memory of Dark Crater
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

            if self.item_boxes_collected:
                if ((performance_progress_bitfield[4] >> 3) & 1) == 0:
                    item_data = self.item_boxes_collected.pop(0)
                    if item_data.name in ["Golden Seed", "Gold Ribbon", "Link Box", "Sky Gift"]:
                        write_byte = performance_progress_bitfield[4] + (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte
                        write_byte2 = item_data.memory_offset

                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, [write_byte2, 0], self.ram_mem_domain),
                                (item_backup_offset + 0x2, int.to_bytes(0), self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain)
                            ]
                        )
                    else:
                        write_byte = performance_progress_bitfield[4] + (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte

                        write_byte2 = [item_data.memory_offset % 256, item_data.memory_offset // 256]

                        loot_table = lootbox_table[item_data.name]

                        items_in_box = [item for item in loot_table]
                        loot_chosen = loot_table[self.random.choice(seq=items_in_box)]
                        write_byte3 = [loot_chosen % 256, loot_chosen // 256]
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, write_byte3, self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain)
                            ]
                        )

            if not ctx.finished_game and self.goal_complete:
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

