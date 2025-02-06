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
    game = "Pokemon Mystery Dungeon Explorers of Sky"
    hash = "6735749e060e002efd88e61560e45567"
    patch_file_ending = ".apeos"
    result_file_ending = ".nds"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_tokens(world: "EOSWorld", patch: EOSProcedurePatch) -> None:
    ov36_mem_loc = 0x296000 #find_ov36_mem_location()
    seed_offset = 0x36F90
    player_name_offset = 0x36F80
    ap_settings_offset = 0x36F98
    recruitment_offset = 0x3702C
    recruitment_evo_offset = 0x37030
    team_formation_offset = 0x37034
    level_scaling_offset = 0x37038
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
    }
    seed = world.multiworld.seed_name.encode("UTF-8")[0:7]
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    player_name_changed = (world.multiworld.player_name[world.player]).translate("[]~\\")

    player_name_changed = player_name_changed.encode("ascii", "xmlcharrefreplace")

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+player_name_offset,
                      player_name_changed)

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+seed_offset, seed)
    write_byte = 0
    if world.options.recruit:
        write_byte = write_byte | (0x1 << 0)

    if world.options.recruit_evo:
        write_byte = write_byte | (0x1 << 1)

    if world.options.team_form:
        write_byte = write_byte | (0x1 << 2)

    if world.options.level_scale:
        write_byte = write_byte | (0x1 << 3)

    if world.options.type_sanity:
        write_byte = write_byte | (0x1 << 4)

    if world.options.starter_option == 1:
        write_byte = write_byte | (0x1 << 5)

    elif world.options.starter_option == 2:
        write_byte = write_byte | (0x1 << 6)

    elif world.options.starter_option == 3:
        write_byte = write_byte | ((0x1 << 5) + (0x1 << 6))

    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + ap_settings_offset, int.to_bytes(write_byte))
    patch.write_file("token_data.bin", patch.get_token_binary())


def find_ov36_mem_location() -> int:
    rom = get_base_rom_as_bytes()
    for byte_i, byte in enumerate(rom):

        hex_search_value = 0x0DF0ADBA
        hex_searched = int.from_bytes(rom[byte_i:(byte_i+3)])
        if hex_searched == hex_search_value:
            return byte_i


