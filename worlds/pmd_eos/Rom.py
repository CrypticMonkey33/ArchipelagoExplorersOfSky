import io
import json
import random

from . import data
from typing import TYPE_CHECKING, Optional
from BaseClasses import Item, Location
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .Items import item_table
from .Locations import EOS_location_table

if TYPE_CHECKING:
    from . import EOSWorld


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pmd_eos_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes


class EOSPathExtension(APPatchExtension):
    game = "Pokemon Mystery Dungeon Explorers of Sky"


class EOSProcedurePatch(APProcedurePatch, APTokenMixin):
    # settings for what the end file is going to look like
    game = "Pokemon Mystery Dungeon Explorers of Sky"
    hash = "6735749e060e002efd88e61560e45567"
    patch_file_ending = ".apeos"
    result_file_ending = ".nds"
    # different procedures to apply. Can always add more but have only needed these two so far
    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_tokens(world: "EOSWorld", patch: EOSProcedurePatch) -> None:
    ov36_mem_loc = 0x296200  # find_ov36_mem_location()
    seed_offset = 0x36F90
    player_name_offset = 0x36F80
    ap_settings_offset = 0x36F98
    mission_max_offset = 0x36F9A
    macguffin_max_offset = 0x36F9E
    # recruitment_offset = 0x3702C
    # recruitment_evo_offset = 0x37030
    # team_formation_offset = 0x37034
    # level_scaling_offset = 0x37038
    options_dict = {
        "seed": world.multiworld.seed,
        "player": world.player,
        "goal": world.options.goal.value,
        "bag_start": world.options.bag_on_start.value,
        "level_scaling": world.options.level_scale.value,
        "recruiting": world.options.recruit.value,
        "recruits_evolution": world.options.recruit_evo.value,
        "team_formation": world.options.team_form.value,
        "dojo_dungeons_rando": world.options.dojo_dungeons.value,
        "relic_shard_fragments": world.options.shard_fragments.value,
        "extra_shards": world.options.extra_shards.value,
        "type_sanity": world.options.type_sanity.value,
        "starter_option": world.options.starter_option.value,
        "iq_scaling": world.options.iq_scaling.value,
        "xp_scaling": world.options.xp_scaling.value,
        "instruments_required": world.options.req_instruments.value,
        "extra_instruments": world.options.extra_instruments.value,
        "hero_evolution": world.options.hero_evolution.value,
        "deathlink": world.options.deathlink.value,
        "legendaries": world.options.legendaries.value,
        "allowed_legendaries": world.options.allowed_legendaries.value,
    }
    seed = world.multiworld.seed_name.encode("UTF-8")[0:7]
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    # Change the player name so that PMD_EOS can read it correctly and then make it ascii
    player_name_changed = (world.multiworld.player_name[world.player]).translate("[]~\\")

    player_name_changed = player_name_changed.encode("ascii", "xmlcharrefreplace")

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+player_name_offset,
                      player_name_changed)

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+seed_offset, seed)
    instrument_count = world.options.req_instruments.value + world.options.extra_instruments.value
    macguffin_count = world.options.shard_fragments.value + world.options.extra_shards.value
    # Take the options and bake them into the rom, so they can be applied on runtime
    write_byte = 0
    write_byte = write_byte | world.options.iq_scaling.value
    if world.options.recruit.value:
        write_byte = write_byte | (0x1 << 4)

    if world.options.recruit_evo.value:
        write_byte = write_byte | (0x1 << 5)

    if world.options.team_form.value:
        write_byte = write_byte | (0x1 << 6)

    if world.options.level_scale.value:
        write_byte = write_byte | (0x1 << 7)

    if world.options.type_sanity.value:
        write_byte = write_byte | (0x1 << 8)

    if world.options.starter_option.value == 1:
        write_byte = write_byte | (0x1 << 9)

    elif world.options.starter_option.value == 2:
        write_byte = write_byte | (0x1 << 10)

    elif world.options.starter_option.value == 3:
        write_byte = write_byte | ((0x1 << 9) + (0x1 << 10))
    # write the tokens that will be applied and write the token data into the bin for AP
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + ap_settings_offset, int.to_bytes(write_byte, length=2, byteorder="little"))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + macguffin_max_offset + 0x1, int.to_bytes(instrument_count))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + macguffin_max_offset, int.to_bytes(macguffin_count))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + mission_max_offset, int.to_bytes(world.options.early_mission_checks.value))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + mission_max_offset + 0x1, int.to_bytes(world.options.early_outlaw_checks.value))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + mission_max_offset + 0x2, int.to_bytes(world.options.late_mission_checks.value))
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + mission_max_offset + 0x3, int.to_bytes(world.options.late_outlaw_checks.value))
    patch.write_file("token_data.bin", patch.get_token_binary())


def find_ov36_mem_location() -> int:
    # Not currently used. Was an attempt to search the entire rom for the identifier and return where it found it
    # Would simplify having to change the start value of ov 36 every time the base patch changes
    rom = get_base_rom_as_bytes()
    for byte_i, byte in enumerate(rom):

        hex_search_value = 0x0DF0ADBA
        hex_searched = int.from_bytes(rom[byte_i:(byte_i+3)])
        if hex_searched == hex_search_value:
            return byte_i


