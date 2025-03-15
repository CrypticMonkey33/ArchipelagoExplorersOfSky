from typing import TYPE_CHECKING, Optional, Set, List, Dict
import array
import time
import re
import binascii

from Utils import async_start
from NetUtils import ClientStatus
from .Locations import EOSLocation, EOS_location_table, location_Dict_by_id, location_dict_by_start_id, \
    location_table_by_groups
from .Items import ItemData, item_table_by_id, lootbox_table, item_table_by_groups
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
    instruments_collected = 0
    required_instruments = 0
    dialga_complete = False
    #item_boxes_collected: List[ItemData] = []
    random: Random = Random()
    outside_deathlink = 0
    deathlink_sender = ""
    deathlink_message:str = ""
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

    async def update_received_items(self, ctx: "BizHawkClientContext", received_items_offset, received_index,
                                    i) -> None:
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
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            self.outside_deathlink += 1
            self.deathlink_sender = args["data"]["source"]
            self.deathlink_message = args["data"]["cause"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger

        try:
            if ctx.seed_name is None:
                return
            if not self.seed_verify:
                # Need to figure out where we are putting the seed and then update this
                seed = await bizhawk.read(ctx.bizhawk_ctx, [(0x3DE010, 8, self.ram_mem_domain)])
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
            #if 310 not in ctx.locations_info:
            #    await ctx.send_msgs(
            #        [{
            #            "cmd": "LocationScouts",
            #            "locations": [310, 311, 312, 313, 314, 315, 316, 317, 318, 319]
            #        }]
            #    )
            await (ctx.send_msgs(
                [
                    {"cmd": "Set",
                     "key": self.player_name + "Dungeon Missions",
                     "default": {location: 0 for location in location_table_by_groups["Mission"]},
                     "want_reply": True,
                     "operations": [{"operation": "update", "value": {}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Dungeon Outlaws",
                     "default": {location: 0 for location in location_table_by_groups["Mission"]},
                     "want_reply": True,
                     "operations": [{"operation": "update", "value": {}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Item Boxes Collected",
                     "default": {0: []},
                     "want_reply": True,
                     "operations": [{"operation": "default", "value": {0: []}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Legendaries Recruited",
                     "default": {0: []},
                     "want_reply": True,
                     "operations": [{"operation": "default", "value": {0: []}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "GenericStorage",
                     "default": {"goal_complete": False, "bag_given": False, "macguffins_collected": 0,
                                 "macguffin_unlock_amount": 0, "instruments_collected": 0, "required_instruments": 0,
                                 "dialga_complete": False},
                     "want_reply": True,
                     "operations": [{"operation": "default", "value":
                         {"goal_complete": False, "bag_given": False,
                          "macguffins_collected": 0, "macguffin_unlock_amount": 0,
                          "instruments_collected": 0, "required_instruments": 0,
                          "dialga_complete": False}}]
                     }
                ]))
            await asyncio.sleep(0.1)

            item_boxes_collected: List[Dict] = []
            legendaries_recruited: List[Dict] = []
            open_list_total_offset: int = await (self.load_script_variable_raw(0x4F, ctx))
            conquest_list_total_offset: int = await (self.load_script_variable_raw(0x52, ctx))
            scenario_balance_offset = await (self.load_script_variable_raw(0x13, ctx))
            performance_progress_offset = await (self.load_script_variable_raw(0x4E, ctx))
            scenario_subx_offset = await (self.load_script_variable_raw(0x5, ctx))
            received_items_offset = await (self.load_script_variable_raw(0x16, ctx))
            scenario_main_offset = await (self.load_script_variable_raw(0x3, ctx))
            scenario_main_bitfield_offset = await (self.load_script_variable_raw(0x11, ctx))
            special_episode_offset = await (self.load_script_variable_raw(0x4B, ctx))
            item_backup_offset = await (self.load_script_variable_raw(0x64, ctx))
            dungeon_enter_index_offset = await (self.load_script_variable_raw(0x29, ctx))
            scenario_talk_bitfield_offset = await (self.load_script_variable_raw(0x12, ctx))
            event_local_offset = await (self.load_script_variable_raw(0x5C, ctx))
            bank_gold_offset = 0x2A5504  # await (self.load_script_variable_raw(0x3D, ctx))
            player_gold_offset = 0x2A54F8
            custom_save_area_offset = 0x3B0000
            mission_status_offset = custom_save_area_offset + 0x4
            relic_shards_offset = custom_save_area_offset + 0x184
            instruments_offset = custom_save_area_offset + 0x185
            death_link_offset = custom_save_area_offset + 0x186
            death_link_receiver_offset = death_link_offset # reciever bool
            death_link_sender_offset = death_link_offset + 0x1 # sender bool
            death_link_sky_death_message_offset = death_link_offset + 0x2  # sky death message
            death_link_ally_death_message_offset = death_link_offset + 0x2 + 128 # ally death message
            death_link_ally_name_offset = death_link_offset + 0x2 + 256  # ally death name
            hintable_items_offset = custom_save_area_offset + 0x29A

            if (self.player_name + "Dungeon Missions") in ctx.stored_data:
                dungeon_missions_dict = ctx.stored_data[self.player_name + "Dungeon Missions"]
            else:
                dungeon_missions_dict = {}
                return
            if (self.player_name + "Dungeon Outlaws") in ctx.stored_data:
                dungeon_outlaws_dict = ctx.stored_data[self.player_name + "Dungeon Outlaws"]
            else:
                dungeon_outlaws_dict = {}
                return
            if (self.player_name + "Item Boxes Collected") in ctx.stored_data:
                item_boxes_collected = ctx.stored_data[self.player_name + "Item Boxes Collected"]["0"]
            else:
                item_boxes_collected = []
                return
            if (self.player_name + "Legendaries Recruited") in ctx.stored_data:
                legendaries_recruited = ctx.stored_data[self.player_name + "Legendaries Recruited"]["0"]
            else:
                legendaries_recruited = []
                return
            if (self.player_name + "GenericStorage") in ctx.stored_data:
                stored = ctx.stored_data[self.player_name + "GenericStorage"]
                self.goal_complete = stored["goal_complete"]
                self.bag_given = stored["bag_given"]
                self.macguffins_collected = stored["macguffins_collected"]
                self.macguffin_unlock_amount = stored["macguffin_unlock_amount"]
                self.required_instruments = stored["required_instruments"]
                self.instruments_collected = stored["instruments_collected"]
                self.dialga_complete = stored["dialga_complete"]

            else:

                return

            if ctx.slot_data:
                if ("Deathlink" in ctx.slot_data):
                    if ("DeathLink" not in ctx.tags) and ctx.slot_data["Deathlink"]:
                        await ctx.update_death_link(True)
                    elif ("DeathLink" in ctx.tags) and not ctx.slot_data["Deathlink"]:
                        await ctx.update_death_link(False)
                else:
                    return

            if self.required_instruments == 0:
                self.required_instruments = ctx.slot_data["RequiredInstruments"]

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
                    (scenario_talk_bitfield_offset + 0x1F, 1, self.ram_mem_domain),
                    (dungeon_enter_index_offset, 2, self.ram_mem_domain),
                    (event_local_offset, 1, self.ram_mem_domain),
                    (death_link_receiver_offset, 1, self.ram_mem_domain),  # reciever bool
                    (death_link_sender_offset, 1, self.ram_mem_domain),  # sender bool
                    (death_link_sky_death_message_offset, 128, self.ram_mem_domain),  # sky death message
                    (death_link_ally_death_message_offset, 128, self.ram_mem_domain),  # ally death message
                    (death_link_ally_name_offset, 18, self.ram_mem_domain),  # ally death name
                    (hintable_items_offset, 0xA, self.ram_mem_domain),
                    (bank_gold_offset, 4, self.ram_mem_domain),
                    (player_gold_offset, 4, self.ram_mem_domain),
                    (relic_shards_offset, 1, self.ram_mem_domain),
                    (instruments_offset, 1, self.ram_mem_domain),
                ]
            )
            # make sure we are actually on the start screen before checking items and such
            scenario_main_list = read_state[6]
            if int.from_bytes(scenario_main_list) == 0:
                return
            #is_running = await self.is_game_running(ctx)
            LOADED_OVERLAY_GROUP_1 = 0xAFAD4
            overlay_groups = await bizhawk.read(ctx.bizhawk_ctx, [(LOADED_OVERLAY_GROUP_1, 8, self.ram_mem_domain)])
            group1 = int.from_bytes(overlay_groups[0][0:4], "little")
            group2 = int.from_bytes(overlay_groups[0][4:8], "little")
            if group2 == 0x2:
                is_running = (group1 == 13 or group1 == 14)
            else:
                is_running = False
            if not is_running:
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
            scenario_talk_bitfield_248_list = int.from_bytes(read_state[10])
            event_local_num = int.from_bytes(read_state[12])
            dungeon_enter_index = int.from_bytes(read_state[11], "little")
            deathlink_receiver_bit = int.from_bytes(read_state[13])
            deathlink_sender_bit = int.from_bytes(read_state[14])
            deathlink_message_from_sky = ""
            #deathlink_ally_death_message = read_state[16].decode("latin1")
            #deathlink_ally_name = read_state[17].decode("latin1")
            hintable_items = array.array('i', [item for item in read_state[18]])
            bank_gold_amount = int.from_bytes(read_state[19], "little")
            player_gold_amount = int.from_bytes(read_state[20], "little")
            locs_to_send = set()
            relic_shards_amount = int.from_bytes(read_state[21])
            instruments_amount = int.from_bytes(read_state[22])

            #if (310 in ctx.locations_info) and hintable_items[0] == 0:
            #    for i in range(10):
            #        network_item = ctx.locations_info[310+i]


            # Loop for receiving items.
            for i in range(len(ctx.items_received) - received_index):
                # get the item data from our item table
                item_data = item_table_by_id[ctx.items_received[received_index + i].item]
                if (("EarlyDungeons" in item_data.group) or ("LateDungeons" in item_data.group)
                        or ("Dojo Dungeons" in item_data.group) or ("BossDungeons" in item_data.group)
                        or ("ExtraDungeons" in item_data.group) or ("RuleDungeons" in item_data.group)):
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
                            write_byte = performance_progress_bitfield[0] | (0x1 << 2)
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

                    elif item_data.name == "Secret of the Waterfall":
                        if ((performance_progress_bitfield[3] >> 3) & 1) == 0:
                            write_byte = performance_progress_bitfield[3] | (0x1 << 3)
                            performance_progress_bitfield[3] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x3, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )

                    elif item_data.name == "Chatot Repllent":
                        if ((performance_progress_bitfield[3] >> 1) & 1) == 0:
                            write_byte = performance_progress_bitfield[3] | (0x1 << 1)
                            performance_progress_bitfield[3] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x3, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )

                    elif item_data.name == "Sky Jukebox":
                        if ((performance_progress_bitfield[3] >> 2) & 1) == 0:
                            write_byte = performance_progress_bitfield[3] | (0x1 << 2)
                            performance_progress_bitfield[3] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x3, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )

                    elif item_data.name == "Recruitment Sensor":
                        if ((performance_progress_bitfield[3] >> 5) & 1) == 0:
                            write_byte = performance_progress_bitfield[3] | (0x1 << 5)
                            performance_progress_bitfield[3] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x3, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )

                    elif item_data.name == "Hero Evolution":
                        write_byte = performance_progress_bitfield[1] | (0x1 << 2)
                        performance_progress_bitfield[1] = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (performance_progress_offset + 0x1, int.to_bytes(write_byte),
                                 self.ram_mem_domain),
                            ]
                        )
                    elif item_data.name == "Recruit Evolution":
                        write_byte = performance_progress_bitfield[0] | (0x1 << 6)
                        performance_progress_bitfield[0] = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (performance_progress_offset, int.to_bytes(write_byte),
                                 self.ram_mem_domain),
                            ]
                        )
                    elif item_data.name == "Recruitment":
                        write_byte = performance_progress_bitfield[0] | (0x1 << 5)
                        performance_progress_bitfield[0] = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (performance_progress_offset, int.to_bytes(write_byte),
                                 self.ram_mem_domain),
                            ]
                        )

                    elif item_data.name == "Formation Control":
                        write_byte = performance_progress_bitfield[0] | (0x1 << 7)
                        performance_progress_bitfield[0] = write_byte
                        write_byte2 = performance_progress_bitfield[2] | (0x1 << 4)
                        performance_progress_bitfield[2] = write_byte
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (performance_progress_offset, int.to_bytes(write_byte),
                                 self.ram_mem_domain),
                                (performance_progress_offset + 0x2, int.to_bytes(write_byte2),
                                 self.ram_mem_domain),
                            ]
                        )
                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Money" in item_data.group:
                    player_gold_amount += item_data.memory_offset
                    #bank_gold_amount += item_data.memory_offset
                    if player_gold_amount > 99999:
                        extra_money = player_gold_amount - 99999
                        player_gold_amount = 99999
                        bank_gold_amount += extra_money
                    if bank_gold_amount > 9999999:
                        bank_gold_amount = 9999999
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (bank_gold_offset, int.to_bytes(bank_gold_amount,4, "little"),
                             self.ram_mem_domain),
                            (player_gold_offset, int.to_bytes(player_gold_amount, 4, "little"),
                             self.ram_mem_domain)
                        ],
                    )
                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Rank" in item_data.group:
                    if item_data.name == "Secret Rank":
                        write_byte = performance_progress_bitfield[2] | (0x1 << 6)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (performance_progress_offset + 0x2, int.to_bytes(write_byte),
                                 self.ram_mem_domain)],
                        )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Macguffin" in item_data.group:
                    if item_data.name == "Relic Fragment Shard":
                        if relic_shards_amount == self.macguffins_collected:
                            self.macguffins_collected += 1
                            relic_shards_amount += 1
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (relic_shards_offset, int.to_bytes(relic_shards_amount),
                                     self.ram_mem_domain)],
                            )
                            await asyncio.sleep(0.1)
                        elif relic_shards_amount > self.macguffins_collected:
                            # uhhhh I don't know how this could happen? Also what do I do????
                            self.macguffins_collected = relic_shards_amount
                        else:
                            relic_shards_amount += 1
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (relic_shards_offset, int.to_bytes(relic_shards_amount),
                                     self.ram_mem_domain)],
                            )
                            await asyncio.sleep(0.1)

                        if self.macguffins_collected >= self.macguffin_unlock_amount:
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

                    #elif item_data.name == "Cresselia Feather":
                    #    self.cresselia_feather_acquired = True

                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Item" in item_data.group:
                    item_boxes_collected += [
                        {"name": item_data.name, "id": item_data.id, "memory_offset": item_data.memory_offset}]
                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Legendary" in item_data.group:
                    legendaries_recruited += [
                        {"name": item_data.name, "id": item_data.id, "memory_offset": item_data.memory_offset}]
                    await self.update_received_items(ctx, received_items_offset, received_index, i)
                elif "Trap" in item_data.group:
                    if item_data.name == "Inspiration Strikes!":
                        if ((performance_progress_bitfield[4] >> 0) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] | 0x1
                            performance_progress_bitfield[4] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                    elif item_data.name == "Get Unowned!":
                        if ((performance_progress_bitfield[4] >> 1) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 1)
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
                            write_byte = scenario_main_bitfield_list[0] | (0x1 << 3)
                            scenario_main_bitfield_list[0] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (scenario_main_bitfield_offset, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                    elif item_data.name == "Sentry Duty!":  # 34
                        if ((performance_progress_bitfield[4] >> 2) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 2)
                            performance_progress_bitfield[4] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)
                    elif item_data.name == "Touch Grass":  # 36
                        if ((performance_progress_bitfield[4] >> 4) & 1) == 0:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 4)
                            performance_progress_bitfield[4] = write_byte
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte),
                                     self.ram_mem_domain),
                                ]
                            )
                        await self.update_received_items(ctx, received_items_offset, received_index, i)

            # Check for set location flags in dungeon list
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
                            locs_to_send.add(400)
                        elif (ctx.slot_data["Goal"] == 1) and (bit_number_dung == 69):
                            self.goal_complete = True
                            locs_to_send.add(400)
                        elif (ctx.slot_data["Goal"] == 1) and (bit_number_dung == 43):
                            self.dialga_complete = True
                        if bit_number_dung in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_dung].id)

            # Check for set location flags in general bitfield
            for byte_m, byte in enumerate(scenario_subx_bitfield):
                for k in range(8):
                    if k in self.checked_general_flags[byte_m]:
                        continue
                    if ((byte >> k) & 1) == 1:
                        self.checked_general_flags[byte_m] += [k]
                        bit_number_gen = (byte_m * 8) + k + 300
                        if bit_number_gen in location_Dict_by_id:
                            locs_to_send.add(location_Dict_by_id[bit_number_gen].id)

            # 3 = 251 send check for mission, 4 = 252 outlaw, 5 = 253 normal missions
            if ((scenario_talk_bitfield_248_list >> 5) & 1) == 1:  # if normal mission
                # read dungeon enter index
                mission_status_read = await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(mission_status_offset, 384, self.ram_mem_domain)])
                mission_status = array.array('i', [item for item in mission_status_read[0]])
                for i in range(192):
                    if i not in location_dict_by_start_id:
                        continue
                    else:
                        if "Mission" in location_dict_by_start_id[i].group:
                            location_name = location_dict_by_start_id[i].name
                            location_id = location_dict_by_start_id[i].id
                            dungeons_complete = dungeon_missions_dict[location_name]
                            current_missions_completed = mission_status[2*i]
                            if current_missions_completed > dungeons_complete:
                                if "Early" in location_dict_by_start_id[i].group:
                                    for k in range(current_missions_completed - dungeons_complete):
                                        if dungeons_complete < ctx.slot_data["EarlyMissionsAmount"]:
                                            locs_to_send.add(location_id + 500 + (100 * location_id) + dungeons_complete + k)
                                            dungeon_missions_dict[location_name] += 1
                                            # location.id + 500 + (100 * i) + j`

                                elif "Late" in location_dict_by_start_id[i].group:
                                    for k in range(current_missions_completed - dungeons_complete):
                                        if dungeons_complete < ctx.slot_data["LateMissionsAmount"]:
                                            locs_to_send.add(location_id + 500 + (100 * location_id) + dungeons_complete + k)
                                            dungeon_missions_dict[location_name] += 1
                                            # location.id + 500 + (100 * i) + j

                scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xDF
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                         self.ram_mem_domain),
                    ]
                )
                await asyncio.sleep(0.1)
            elif ((scenario_talk_bitfield_248_list >> 4) & 1) == 1:  # if outlaw mission
                # read dungeon enter index
                mission_status_read = await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(mission_status_offset, 384, self.ram_mem_domain)])
                mission_status = array.array('i', [item for item in mission_status_read[0]])
                for i in range(192):
                    if i not in location_dict_by_start_id:
                        continue
                    else:
                        if "Mission" in location_dict_by_start_id[i].group:
                            location_name = location_dict_by_start_id[i].name
                            location_id = location_dict_by_start_id[i].id
                            dungeons_complete = dungeon_outlaws_dict[location_name]
                            current_missions_completed = mission_status[2*i + 1]
                            if current_missions_completed > dungeons_complete:
                                if "Early" in location_dict_by_start_id[i].group:
                                    for k in range(current_missions_completed - dungeons_complete):
                                        if dungeons_complete < ctx.slot_data["EarlyOutlawsAmount"]:
                                            locs_to_send.add(location_id + 500 + 50 + (100 * location_id) + dungeons_complete + k)
                                            dungeon_outlaws_dict[location_name] += 1
                                            # location.id + 500 + (100 * i) + j`

                                elif "Late" in location_dict_by_start_id[i].group:
                                    for k in range(current_missions_completed - dungeons_complete):
                                        if dungeons_complete < ctx.slot_data["LateOutlawsAmount"]:
                                            locs_to_send.add(location_id + 500 + 50 + (100 * location_id) + dungeons_complete + k)
                                            dungeon_outlaws_dict[location_name] += 1
                                            # location.id + 500 + (100 * i) + j

                scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xEF
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                         self.ram_mem_domain),
                    ]
                )
                await asyncio.sleep(0.1)
            hints_to_send = []
            for i in range(10):
                if hintable_items[i] == 1:
                    hints_to_send += [i + 310]
            await (ctx.send_msgs(
                [
                    {"cmd": "LocationScouts",
                     "locations": hints_to_send,
                     "create_as_hint": 2
                     }]))


            # Send locations if there are any to send.
            if locs_to_send != self.local_checked_locations:
                self.local_checked_locations = locs_to_send

                if locs_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])

            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if (self.outside_deathlink == 0) and ((deathlink_sender_bit & 1) == 1):
                    deathlink_message_from_sky = read_state[15].decode("latin1").split(chr(0))[0]
                    deathlink_message_from_sky = re.sub(r"\[.*?]", "", deathlink_message_from_sky)
                    lappyint = self.random.randint(1, 100)
                    #deathlink_message_from_sky = deathlink_message_from_sky.replace("byan", "by an")
                    if lappyint == 1:
                        await ctx.send_death(f"{ctx.player_names[ctx.slot]} was defeated by Lappy's silliness")
                    else:
                        await ctx.send_death(f"{ctx.player_names[ctx.slot]}{deathlink_message_from_sky}")
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (death_link_sender_offset, int.to_bytes(0), self.ram_mem_domain)
                    ]
                )
                await asyncio.sleep(0.1)
            if self.outside_deathlink != 0:
                trans = str.maketrans("[]~\\", "    ")
                trans.update({0: 32})
                write_message = self.deathlink_message.translate(trans).split(chr(0))[0].encode("latin1")[0:128]
                write_message2 = f"[CS:N]{self.deathlink_sender.translate(trans).split(chr(0))[0][0:18]}[CR]".encode("latin1")
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (death_link_ally_death_message_offset, write_message,self.ram_mem_domain),
                        (death_link_ally_name_offset, write_message2, self.ram_mem_domain),
                        (death_link_receiver_offset, int.to_bytes(1), self.ram_mem_domain)
                    ]
                )
                self.outside_deathlink -= 1

            # Check for opening Dark Crater
            if (self.instruments_collected >= self.required_instruments) and self.dialga_complete:
                item_memory_offset = 0x43  # the location in memory of Dark Crater
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

            # Sending item boxes on Event Divide
            if ((performance_progress_bitfield[4] >> 3) & 1) == 0:  # if we are not currently dealing with items
                if item_boxes_collected != []:
                    # I have an item in my list, add it to the queue and set the performance progress list to true
                    item_data = item_boxes_collected.pop(0)
                    if item_data["name"] in item_table_by_groups["Single"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte
                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, int.to_bytes(0, byteorder="little",length=2), self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                 self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Multi"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte
                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, int.to_bytes(5, byteorder="little",length=2), self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (
                                scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Instrument"]:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                            performance_progress_bitfield[4] = write_byte
                            write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                            scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                            if instruments_amount == self.instruments_collected:
                                self.instruments_collected += 1
                                instruments_amount += 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [
                                        (instruments_offset, int.to_bytes(instruments_amount),
                                         self.ram_mem_domain)],
                                )
                                await asyncio.sleep(0.1)
                            elif instruments_amount > self.instruments_collected:
                                # uhhhh I don't know how this could happen? Also what do I do????
                                self.instruments_collected = instruments_amount
                            else:
                                instruments_amount += 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [
                                        (instruments_offset, int.to_bytes(instruments_amount),
                                         self.ram_mem_domain)],
                                )
                                await asyncio.sleep(0.1)

                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (item_backup_offset, write_byte2, self.ram_mem_domain),
                                    (item_backup_offset + 0x2, int.to_bytes(0, byteorder="little",length=2), self.ram_mem_domain),
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                    (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                    self.ram_mem_domain)

                                ]
                            )
                            await asyncio.sleep(0.1)

                    elif item_data["name"] in item_table_by_groups["Exclusive"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte

                        write_byte3 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]

                        write_byte2 = [0x16c % 256, 0x16c // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, write_byte3, self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (
                                scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)
                         
                    elif item_data["name"] in item_table_by_groups["Box"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte

                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]

                        loot_table = lootbox_table[item_data["name"]]

                        items_in_box = [item for item in loot_table]
                        loot_chosen = loot_table[self.random.choice(seq=items_in_box)]
                        write_byte3 = [loot_chosen % 256, loot_chosen // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, write_byte3, self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                 self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)

            else:  # if we are dealing with items
                if (item_boxes_collected != []) and (((scenario_talk_bitfield_248_list >> 2) & 1) == 1):
                    # I have an item in my list and lappy is already done with the item in the queue,
                    # so add another item to queue and set performance progress to true
                    item_data = item_boxes_collected.pop(0)
                    if item_data["name"] in item_table_by_groups["Single"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte
                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, int.to_bytes(0, byteorder="little",length=2), self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                 self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Multi"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte
                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, int.to_bytes(5, byteorder="little",length=2), self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (
                                scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Instrument"]:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                            performance_progress_bitfield[4] = write_byte
                            write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]
                            scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                            if instruments_amount == self.instruments_collected:
                                self.instruments_collected += 1
                                instruments_amount += 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [
                                        (instruments_offset, int.to_bytes(instruments_amount),
                                         self.ram_mem_domain)],
                                )
                                await asyncio.sleep(0.1)
                            elif instruments_amount > self.instruments_collected:
                                # uhhhh I don't know how this could happen? Also what do I do????
                                self.instruments_collected = instruments_amount
                            else:
                                instruments_amount += 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [
                                        (instruments_offset, int.to_bytes(instruments_amount),
                                         self.ram_mem_domain)],
                                )
                                await asyncio.sleep(0.1)

                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (item_backup_offset, write_byte2, self.ram_mem_domain),
                                    (item_backup_offset + 0x2, int.to_bytes(0, byteorder="little",length=2), self.ram_mem_domain),
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                    (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                    self.ram_mem_domain)
                                ]
                            )
                            await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Exclusive"]:
                            write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                            performance_progress_bitfield[4] = write_byte

                            write_byte3 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]

                            write_byte2 = [0x16c % 256, 0x16c // 256]
                            scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (item_backup_offset, write_byte2, self.ram_mem_domain),
                                    (item_backup_offset + 0x2, write_byte3, self.ram_mem_domain),
                                    (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                    (
                                    scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                    self.ram_mem_domain)
                                ]
                            )
                            await asyncio.sleep(0.1)
                    elif item_data["name"] in item_table_by_groups["Box"]:
                        write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                        performance_progress_bitfield[4] = write_byte

                        write_byte2 = [item_data["memory_offset"] % 256, item_data["memory_offset"] // 256]

                        loot_table = lootbox_table[item_data["name"]]

                        items_in_box = [item for item in loot_table]
                        loot_chosen = loot_table[self.random.choice(seq=items_in_box)]
                        write_byte3 = [loot_chosen % 256, loot_chosen // 256]
                        scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFB
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (item_backup_offset, write_byte2, self.ram_mem_domain),
                                (item_backup_offset + 0x2, write_byte3, self.ram_mem_domain),
                                (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                                (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                                 self.ram_mem_domain)
                            ]
                        )
                        await asyncio.sleep(0.1)

                elif item_boxes_collected != []:
                    # I have items in my list still, but lappy has not processed the item yet, just move on for now
                    pass

                elif ((scenario_talk_bitfield_248_list >> 2) & 1) == 1:
                    # I don't have items in my list and lappy is done with the item,
                    # add a null to the queue and set performance progress to true
                    write_byte = performance_progress_bitfield[4] | (0x1 << 3)
                    scenario_talk_bitfield_248_list = (scenario_talk_bitfield_248_list & 0xFB)
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (item_backup_offset, [0, 0], self.ram_mem_domain),
                            (item_backup_offset + 0x2, [0, 0], self.ram_mem_domain),
                            (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                            (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                             self.ram_mem_domain)
                        ]
                    )
                    await asyncio.sleep(0.1)

            # if performance progress 37 is off, and we have a legendary to recruit, turn 37 on
            if (((performance_progress_bitfield[4] >> 5) & 1) == 0) and event_local_num != 22 and legendaries_recruited:
                write_byte = performance_progress_bitfield[4] | (0x1 << 5)
                performance_progress_bitfield[4] = write_byte
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (performance_progress_offset + 0x4, int.to_bytes(write_byte), self.ram_mem_domain),
                    ]
                )
                await asyncio.sleep(0.1)

            # if Scenario Talk 249 is on, edit event local with the index of the next legendary and then turn off
            # performance progress 37
            if (((scenario_talk_bitfield_248_list >> 1) & 1) == 1) and event_local_num == 22 and legendaries_recruited:
                item_data = legendaries_recruited.pop(0)
                write_byte2 = item_data["memory_offset"]
                scenario_talk_bitfield_248_list = scenario_talk_bitfield_248_list & 0xFD
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [

                        (event_local_offset, int.to_bytes(write_byte2), self.ram_mem_domain),
                        (scenario_talk_bitfield_offset + 0x1F, int.to_bytes(scenario_talk_bitfield_248_list),
                         self.ram_mem_domain),
                    ]
                )
                await asyncio.sleep(0.1)

            # Update data storage
            await (ctx.send_msgs(
                [
                    {"cmd": "Set",
                     "key": self.player_name + "Dungeon Missions",
                     "default": {},
                     "want_reply": True,
                     "operations": [{"operation": "update", "value": dungeon_missions_dict}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Dungeon Outlaws",
                     "default": {},
                     "want_reply": True,
                     "operations": [{"operation": "update", "value": dungeon_outlaws_dict}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Item Boxes Collected",
                     "default": {},
                     "want_reply": True,
                     "operations": [{"operation": "replace", "value": {0: item_boxes_collected}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "Legendaries Recruited",
                     "default": {},
                     "want_reply": True,
                     "operations": [{"operation": "replace", "value": {0: legendaries_recruited}}]
                     },
                    {"cmd": "Set",
                     "key": self.player_name + "GenericStorage",
                     "default": {"goal_complete": False, "bag_given": False, "macguffins_collected": 0,
                                 "macguffin_unlock_amount": 0, "cresselia_feather_acquired": False,
                                 "dialga_complete": False},
                     "want_reply": True,
                     "operations": [{"operation": "update", "value":
                         {"goal_complete": self.goal_complete, "bag_given": self.bag_given,
                          "macguffins_collected": self.macguffins_collected, "macguffin_unlock_amount": self.macguffin_unlock_amount,
                          "required_instruments": self.required_instruments, "instruments_collected": self.instruments_collected,
                          "dialga_complete": self.dialga_complete}}]
                     }
                ]))
            await asyncio.sleep(0.1)

            # Check for finishing the game and send the goal to the server
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

    def unused(self, ctx):
        (ctx.send_msgs(
            [
                {"cmd": "Set",
                 "key": "Dungeon Missions",
                 "default": {},
                 "want_reply": True,
                 "operations": [{"operation": "update", "value": {}}]
                 }
            ]
        ))

    async def is_game_running(self, ctx: "BizHawkClientContext") -> bool:
        LOADED_OVERLAY_GROUP_1 = 0xAF234
        overlay_groups = await bizhawk.read(ctx.bizhawk_ctx, [(LOADED_OVERLAY_GROUP_1, 8, self.ram_mem_domain)])
        group1 = int.from_bytes(overlay_groups[0][0:4], "little")
        group2 = int.from_bytes(overlay_groups[0][4:8], "little")
        if (group2 == 0x2):
            return group1 == 13 or group1 == 14
        return False
