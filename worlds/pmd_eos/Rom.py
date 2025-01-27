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
    ov36_mem_loc = 0x295400
    seed_offset = 0x37020
    player_name_offset = 0x36F80
    recruitment_offset = 0x3702C
    recruitment_evo_offset = 0x37030
    team_formation_offset = 0x37034
    level_scaling_offset = 0x37038
    options_dict = {
        "seed": world.multiworld.seed,
        "player": world.player,
        "bag_start": world.options.bag_on_start.value,
        "level_scaling": world.options.level_scale.value,
        "recruiting": world.options.recruit.value,
        "recruits_evolution": world.options.recruit_evo.value,
        "team_formation": world.options.team_form.value,
        "dojo_dungeons_rando": world.options.dojo_dungeons.value,
        "relic_shard_fragments": world.options.shard_fragments.value,
    }
    seed = world.multiworld.seed_name.encode("UTF-8")[0:7]
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+player_name_offset, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+seed_offset, seed)

    if world.options.recruit:
        patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + recruitment_offset, int.to_bytes(0x1))

    if world.options.recruit_evo:
        patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + recruitment_evo_offset, int.to_bytes(0x1))

    if world.options.team_form:
        patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + team_formation_offset, int.to_bytes(0x1))

    if world.options.level_scale:
        patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + level_scaling_offset, int.to_bytes(0x1))

    patch.write_file("token_data.bin", patch.get_token_binary())

