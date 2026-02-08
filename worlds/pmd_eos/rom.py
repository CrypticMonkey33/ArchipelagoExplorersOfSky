import json
from typing import TYPE_CHECKING, ClassVar

from BaseClasses import Location
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from .rom_type_definitions import RomSettings

if TYPE_CHECKING:
    from . import EOSWorld


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().pmd_eos_options.rom_file, "rb") as infile:
        return bytes(infile.read())


class EOSPathExtension(APPatchExtension):
    game = "Pokémon Mystery Dungeon: Explorers of Sky"


class EOSProcedurePatch(APProcedurePatch, APTokenMixin):
    # settings for what the end file is going to look like
    game = "Pokémon Mystery Dungeon: Explorers of Sky"
    hash = "6735749e060e002efd88e61560e45567"
    patch_file_ending = ".apeos"
    result_file_ending = ".nds"
    # different procedures to apply. Can always add more but have only needed these two so far
    procedure : ClassVar = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()


def write_tokens(
    world: "EOSWorld",
    patch: EOSProcedurePatch,
    hint_items: list[Location],
    dimensional_screams: list[Location],
    starting_se: int,
) -> None:
    ov36_mem_loc = 2724864  # find_ov36_mem_location()
    seed_offset = 0x36FA0
    player_name_offset = 0x36F80
    player_name_changed_offset = 0x36F90
    ap_settings_offset = 0x36FA8
    # mission_max_offset = 0x36F9A
    # macguffin_max_offset = 0x36F9E
    # spinda_drinks_offset = 0x37146
    hintable_items_offset = 3303424  # number from Heckas makefile code
    #custom_save_area_offset = ov36_mem_loc + 0x8F80 # unused
    # main_game_unlocked_offset = ov36_mem_loc + 0x37148  # custom_save_area_offset + 0x2A7
    dimensional_scream_who_offset = hintable_items_offset + 0x4
    dimensional_scream_what_offset = hintable_items_offset + 0x202
    dimensional_scream_where_offset = hintable_items_offset + 0x5E0
    # dimensional_scream_hints = get_dimensional_hints(world)
    dimensional_scream_hints = dimensional_screams
    # writable_screams = [k.address for k in dimensional_scream_hints]
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
        "relic_shard_fragments": world.options.required_fragments.value,
        "extra_shards": world.options.total_shards.value,
        "type_sanity": world.options.type_sanity.value,
        "starter_option": world.options.starter_option.value,
        "iq_scaling": world.options.iq_scaling.value,
        "xp_scaling": world.options.xp_scaling.value,
        "instruments_required": world.options.req_instruments.value,
        "extra_instruments": world.options.total_instruments.value,
        "hero_evolution": world.options.hero_evolution.value,
        "deathlink": world.options.deathlink.value,
        "deathlink_type": world.options.deathlink_type.value,
        "legendaries": world.options.legendaries.value,
        "sky_peak_type": world.options.sky_peak_type.value,
        "special_sanity": world.options.special_episode_sanity.value,
        "traps_allowed": world.options.allow_traps.value,
        "invisible_traps": world.options.invisible_traps.value,
        "trap_percentage": world.options.trap_percent.value,
        "long_locations": world.options.long_location.value,
        "cursed_aegis_cave": world.options.cursed_aegis_cave.value,
        "drink_events": world.options.drink_events.value,
        "spinda_drinks": world.options.spinda_drinks.value,
        "exclude_special": world.options.exclude_special.value,
        # "dimensional_screams": writable_screams,
    }
    seed = world.multiworld.seed_name.encode("UTF-8")[0:7]
    patch.write_file("options.json", json.dumps(options_dict).encode("UTF-8"))
    trans_table = {"[": "", "]": "", "~": "", "\\": ""}
    trans_table = str.maketrans(trans_table)
    # Change the player name so that PMD_EOS can read it correctly and then make it latin
    player_name = world.multiworld.player_name[world.player]
    player_name_changed = player_name.translate(trans_table)
    player_name_encoded = player_name.encode("cp1252", "xmlcharrefreplace")
    player_name_changed_encoded = player_name_changed.encode("cp1252", "xmlcharrefreplace")

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + player_name_changed_offset, player_name_changed_encoded)
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + player_name_offset, player_name_encoded)

    # Bake names of previewable items into ROM
    for i in range(len(hint_items)):
        if hint_items[i].name.__contains__("★"):
            hint_loc_name1 = hint_items[i].name.translate(trans_table)
            hint_loc_name = hint_loc_name1.replace("★", "[M:S3]")

        else:
            hint_loc_name = hint_items[i].name.translate(trans_table)
        hint_player = world.multiworld.player_name[hint_items[i].item.player].translate(trans_table)
        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_who_offset + 17 * i,
            hint_player[0:15].encode("cp1252", "xmlcharrefreplace"),
        )

        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_where_offset + 33 * i,
            hint_loc_name[0:31].encode("cp1252", "xmlcharrefreplace"),
        )

        hint_item = hint_items[i].item.name.translate(trans_table)
        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_what_offset + 33 * i,
            hint_item[0:31].encode("cp1252", "xmlcharrefreplace"),
        )

    # Bake the dimensional Scream Hints into the ROM

    for i in range(len(dimensional_scream_hints)):
        hint_player = world.multiworld.player_name[dimensional_scream_hints[i].player].translate(trans_table)
        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_who_offset + 17 * (i + 10),
            hint_player[0:15].encode("cp1252", "xmlcharrefreplace"),
        )
        if dimensional_scream_hints[i].name.__contains__("★"):
            hint_loc_name1 = dimensional_scream_hints[i].name.translate(trans_table)
            hint_loc_name = hint_loc_name1.replace("★", "[M:S3]")

        else:
            hint_loc_name = dimensional_scream_hints[i].name.translate(trans_table)
        # hint_loc_name = dimensional_scream_hints[i].name.translate(trans_table)
        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_where_offset + 33 * (i + 10),
            hint_loc_name[0:31].encode("cp1252", "xmlcharrefreplace"),
        )

        hint_item = dimensional_scream_hints[i].item.name.translate(trans_table)
        patch.write_token(
            APTokenTypes.WRITE,
            dimensional_scream_what_offset + 33 * (i + 10),
            hint_item[0:31].encode("cp1252", "xmlcharrefreplace"),
        )

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + seed_offset, seed)

    # Take the options and bake them into the rom, so they can be applied on runtime
    if world.options.special_episode_sanity.value != 1:
        starting_se = 0
    if world.options.deathlink.value:
        deathlink = 1 + world.options.deathlink_type.value
    else:
        deathlink = 0
    if world.options.goal.value == 1:
        late_missions_count = world.options.late_mission_checks.value
        late_outlaws_count = world.options.late_outlaw_checks.value
    else:
        late_missions_count = 0
        late_outlaws_count = 0

    flags = 0
    flags |= world.options.early_mission_floors.value
    flags |= world.options.move_shortcuts.value << 1
    flags |= world.options.type_sanity.value << 2
    flags |= world.options.long_location.value << 3
    flags |= world.options.guest_scaling << 4

    settings = RomSettings(world.options.xp_scaling.value, world.options.iq_scaling.value,
                                world.options.level_scale.value, world.options.goal.value,starting_se, deathlink,
                                world.options.early_mission_checks.value, world.options.early_outlaw_checks.value,
                                late_missions_count, late_outlaws_count, world.options.starter_option.value,
                                world.options.required_fragments.value, world.options.req_instruments.value,
                                world.options.spinda_drinks.value, world.options.drink_events.value, flags).serialize()

    # write the tokens that will be applied and write the token data into the bin for AP
    patch.write_token(APTokenTypes.WRITE, ov36_mem_loc + ap_settings_offset, settings)

    patch.write_file("token_data.bin", patch.get_token_binary())
    # testnum = find_ov36_mem_location()


def find_ov36_mem_location() -> int:
    # Not currently used. Was an attempt to search the entire rom for the identifier and return where it found it
    # Would simplify having to change the start value of ov 36 every time the base patch changes
    rom = get_base_rom_as_bytes()
    for byte_i in range(0x297000, 0x300000):
        # , byte in enumerate(rom)
        hex_search_value = 0xBAADF00D
        hex_searched = int.from_bytes(rom[byte_i : (byte_i + 4)])
        if hex_searched == hex_search_value:
            return byte_i
    return 0
