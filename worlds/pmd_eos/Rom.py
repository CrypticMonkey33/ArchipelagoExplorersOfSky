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
    ov36_mem_loc = 0x0028DC00
    options_dict = {
        "seed": world.multiworld.seed,
        "player": world.player,
    }
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+0x36F80, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc+0x37020, world.multiworld.seed_name.encode("UTF-8"))

    patch.write_file("token_data.bin", patch.get_token_binary())
