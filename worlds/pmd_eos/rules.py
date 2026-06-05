from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_rule, forbid_item
from .locations import EOS_location_table, EOSLocation, location_Dict_by_id
from .rom_type_definitions import subX_table
from .pokemon import pokemon_info

if TYPE_CHECKING:
    from . import EOSWorld



def set_rules(world: "EOSWorld", excluded):
    player = world.player
    options = world.options

    special_episodes_rules(world, player)
    subx_rules(world, player)
    dungeon_locations_behind_items(world, player)
    mission_rules(world, player)
    forbid_items_behind_locations(world, player)
    spinda_drink_events(world, player)

    if world.options.goal.value == 0:
        set_rule(
            world.multiworld.get_location("Final Boss", player),
            lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Final Boss", player), lambda state: state.has("Main Game Unlock", player)
            )

        # set_rule(world.multiworld.get_location("Dark Crater", player),
        # lambda state: state.has("Dark Crater", player) and ready_for_late_game(state, player, world))

    elif world.options.goal.value == 1:
        set_rule(
            world.multiworld.get_location("Final Boss", player), lambda state: ready_for_darkrai(state, player, world)
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Final Boss", player), lambda state: state.has("Main Game Unlock", player)
            )
        set_rule(
            world.multiworld.get_location("Dark Crater", player), lambda state: ready_for_darkrai(state, player, world)
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Dark Crater", player),
                lambda state: state.has("Main Game Unlock", player),
            )
        set_rule(
            world.multiworld.get_location("The Nightmare", player),
            lambda state: state.can_reach_location("Mt. Bristle", player)
            and state.has("The Nightmare", player)
            and ready_for_late_game(state, player, world),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("The Nightmare", player),
                lambda state: state.has("Main Game Unlock", player),
            )

    set_rule(
        world.multiworld.get_entrance("Late Game Door", player), lambda state: ready_for_late_game(state, player, world)
    )
    
    set_rule(
        world.multiworld.get_entrance("Pokemon Recruit", player), lambda state: has_start_recruit(state, player, world)
    )

    set_rule(world.multiworld.get_location("Hidden Land", player), lambda state: has_relic_shards(state, player, world))
    if special_episode_sanity_no_exclusion(world, player):
        add_rule(
            world.multiworld.get_location("Hidden Land", player), lambda state: state.has("Main Game Unlock", player)
        )

    set_rule(
        world.multiworld.get_location("Temporal Tower", player),
        lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world),
    )
    if special_episode_sanity_no_exclusion(world, player):
        add_rule(
            world.multiworld.get_location("Temporal Tower", player), lambda state: state.has("Main Game Unlock", player)
        )


def has_relic_shards(state, player, world):
    return state.has("Relic Fragment Shard", player, world.options.required_fragments.value)


def ready_for_late_game(state, player, world):
    return (
        state.has_group("EarlyDungeons", player, 10)
        and state.has("Relic Fragment Shard", player, world.options.required_fragments.value)
        and state.has("Temporal Tower", player)
    )

def has_start_recruit(state, player, world):
    if special_episode_sanity_no_exclusion(world, player): 
        return (
            state.has("Recruitment", player) 
            and state.has("Main Game Unlock", player)
            or state.has("Progressive Recruitment", player, 1) 
            and state.has("Main Game Unlock", player)
        )
    else:
        return (
            state.has("Recruitment", player)
            or state.has("Progressive Recruitment", player, 1)
        )


def spinda_drink_events(world, player):
    de_amount = world.options.drink_events.value
    sdrinks_amount = world.options.spinda_drinks.value
    for i in range(de_amount):
        set_rule(
            world.multiworld.get_location("Spinda Drink Event " + str(i + 1), player),
            lambda state: state.has("Bag Upgrade", player, 3),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Spinda Drink Event " + str(i + 1), player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )
    for i in range(sdrinks_amount):
        set_rule(
            world.multiworld.get_location("Spinda Drink " + str(i + 1), player),
            lambda state: state.has("Bag Upgrade", player),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Spinda Drink " + str(i + 1), player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )


def forbid_items_behind_locations(world, player):
    forbid_item(world.multiworld.get_location("Hidden Land", player), "Relic Fragment Shard", player)
    forbid_item(world.multiworld.get_location("Temporal Tower", player), "Relic Fragment Shard", player)
    if world.options.goal.value == 1 and world.options.sky_peak_type == 1:
        forbid_item(world.multiworld.get_location("1st Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("2nd Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("3rd Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("4th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("5th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("6th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("7th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("8th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("9th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("Sky Peak Summit Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("5th Station Clearing", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("Sky Peak Summit", player), "Progressive Sky Peak", player)
        # if world.options.goal.value == 1:
        for i in range(111, 120):
            location = location_Dict_by_id[i]
            for j in range(world.options.late_mission_checks.value):
                forbid_item(
                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                    "Progressive Sky Peak",
                    player,
                )
            for j in range(world.options.late_outlaw_checks.value):
                forbid_item(
                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                    "Progressive Sky Peak",
                    player,
                )

def special_episodes_rules(world, player):
    if not world.options.exclude_special.value:
        # Bidoof Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Deep Star Cave", player), lambda state: state.has("Bidoof's Wish", player)
        )
        set_rule(
            world.multiworld.get_location("SE Star Cave Pit", player), lambda state: state.has("Bidoof's Wish", player)
        )

        # Igglybuff Special Episode checks
        set_rule(
            world.multiworld.get_location("SE Murky Forest", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )
        set_rule(
            world.multiworld.get_location("SE Eastern Cave", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )
        set_rule(
            world.multiworld.get_location("SE Fortune Ravine", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )

        # Grovyle and Dusknoir Special Episode Checks
        set_rule(
            world.multiworld.get_location("In the Future of Darkness Location", player),
            lambda state: has_relic_shards(state, player, world),
        )
        set_rule(
            world.multiworld.get_location("SE Barren Valley", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dark Wasteland", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Temporal Tower", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dusk Forest", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Spacial Cliffs", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dark Ice Mountain", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Icicle Forest", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Vast Ice Mountain", player),
            lambda state: state.has("In the Future of Darkness", player),
        )

        # Team Charm Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Southern Jungle", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Boulder Quarry", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Right Cave Path", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Left Cave Path", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Limestone Cavern", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )

        # Sunflora Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Upper Spring Cave", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )
        set_rule(
            world.multiworld.get_location("SE Middle Spring Cave", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )
        set_rule(
            world.multiworld.get_location("SE Spring Cave Pit", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )


def ready_for_darkrai(state, player, world):
    return (
        state.has("Relic Fragment Shard", player, world.options.required_fragments.value)
        and state.has("Temporal Tower", player)
        and state.has_group("Instrument", player, world.options.req_instruments.value)
        and state.has_group("LateDungeons", player, 10)
    )

def pokemon_rule(rule, world, player, location_name, location_id, has_rule_list):
    if has_rule_list[location_id - 15000]:
        add_rule(
            world.multiworld.get_location(location_name, player),
            rule,
            combine = "or"
        )
    else:
        has_rule_list[location_id - 15000] = 1
        set_rule(
            world.multiworld.get_location(location_name, player),
            rule
        )

def early_pokemon_evolution_rule(location_id, location_found, location_name, level, pokemeon_has_rule, player, world, recruit_chance, difficulty):
    for j in range(len(pokemon_info[location_id - 15000][3])):                               
        if(pokemon_info[location_id - 15000][3][j][1] <= level):
            if (pokemon_info[location_id - 15000][3][j][2] and world.options.goal == 0):
                pass
            else:
                rule = early_evolution_pokemon(location_found, pokemon_info[location_id - 15000][3][j], player, world, recruit_chance, difficulty)
                pokemon_rule(rule, world, player, pokemon_info[location_id - 15000][3][j][0], pokemon_info[location_id - 15000][3][j][3] + 15000, pokemeon_has_rule)

                for h in range(len(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3])):
                    if(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][1] <= level):
                        if (pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][2] and world.options.goal == 0 or pokemon_info[location_id - 15000][3][j][2] and world.options.goal == 0):
                            pass
                        else:
                            rule = early_evolution_pokemon(location_found, pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h], player, world, recruit_chance, difficulty)
                            pokemon_rule(rule, world, player, pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][0], pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][3] + 15000, pokemeon_has_rule)

def late_pokemon_evolution_rule(location_id, location_found, location_name, level, pokemeon_has_rule, player, world, recruit_chance, difficulty):
    for j in range(len(pokemon_info[location_id - 15000][3])):                               
        if(pokemon_info[location_id - 15000][3][j][1] <= level):
            rule = late_evolution_pokemon(location_found, player, world, recruit_chance, difficulty)
            pokemon_rule(rule, world, player, pokemon_info[location_id - 15000][3][j][0], pokemon_info[location_id - 15000][3][j][3] + 15000, pokemeon_has_rule)

            for h in range(len(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3])):
                if(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][1] <= level):
                    rule = late_evolution_pokemon(location_found, player, world, recruit_chance, difficulty)
                    pokemon_rule(rule, world, player, pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][0], pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][3] + 15000, pokemeon_has_rule)

def aegis_pokemon_evolution_rule(location_id, location_found, location_name, level, amount, pokemeon_has_rule, player, world, recruit_chance, difficulty):
    for j in range(len(pokemon_info[location_id - 15000][3])):                               
        if(pokemon_info[location_id - 15000][3][j][1] <= level):
            rule = aegis_evolution_pokemon(location_found, amount, player, world, recruit_chance, difficulty)
            pokemon_rule(rule, world, player, pokemon_info[location_id - 15000][3][j][0], pokemon_info[location_id - 15000][3][j][3] + 15000, pokemeon_has_rule)

            for h in range(len(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3])):
                if(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][1] <= level):
                    rule = aegis_evolution_pokemon(location_found, amount, player, world, recruit_chance, difficulty)
                    pokemon_rule(rule, world, player, pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][0], pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][3] + 15000, pokemeon_has_rule)

def boss_pokemon_evolution_rule(location_id, location_found, location_name, level, pokemeon_has_rule, player, world, recruit_chance, difficulty):
    for j in range(len(pokemon_info[location_id - 15000][3])):                               
        if(pokemon_info[location_id - 15000][3][j][1] <= level):
            rule = boss_evolution_pokemon(player, world, recruit_chance, difficulty)
            pokemon_rule(rule, world, player, pokemon_info[location_id - 15000][3][j][0], pokemon_info[location_id - 15000][3][j][3] + 15000, pokemeon_has_rule)

            for h in range(len(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3])):
                if(pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][1] <= level):
                    rule = boss_evolution_pokemon(player, world, recruit_chance, difficulty)
                    pokemon_rule(rule, world, player, pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][0], pokemon_info[pokemon_info[location_id - 15000][3][j][3]][3][h][3] + 15000, pokemeon_has_rule)

def early_evolution_pokemon(location_name, location_data, player, world, recruit_chance, difficulty):
    if (location_data[2] or location_data[1] > 20):
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                )
    else:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and state.has_group("EarlyDungeons", player, 10)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and state.has_group("EarlyDungeons", player, 10)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has_group("EarlyDungeons", player, 10)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and state.has_group("EarlyDungeons", player, 10)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                )

def late_evolution_pokemon(location_name, player, world, recruit_chance, difficulty):
    if recruit_chance >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.100 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Friend Bow", player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Progressive Recruitment", player, 2)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.225 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 3)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.326 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 4)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Luminous Spring", player)
            )
    else:
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 5)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Secret Slab", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Mystery Part", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            )

def aegis_evolution_pokemon(location_name, amount, player, world, recruit_chance, difficulty):
    if amount == 1:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 1)
                )
    elif amount == 2:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 2)
                )
    elif amount == 3:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                and state.has("Luminous Spring", player)
                and state.has("Progressive Seal", player, 3)
                )

def boss_evolution_pokemon(player, world, recruit_chance, difficulty):
    if recruit_chance >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.100 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Friend Bow", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Amber Tear", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 2)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.225 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 3)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Amber Tear", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Luminous Spring", player)
            )
    elif recruit_chance + 0.326 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 4)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Luminous Spring", player)
            )
    else:
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 5)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Secret Slab", player)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Mystery Part", player)
            and state.has("Secret Rank", player)
            and state.has("Luminous Spring", player)
            )

def early_pokemon(location_name, player, world, recruit_chance, difficulty):
    if recruit_chance >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            )
    elif recruit_chance + 0.100 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Friend Bow", player)
            and state.has_group("EarlyDungeons", player, 10)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and state.has_group("EarlyDungeons", player, 10)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has_group("EarlyDungeons", player, 10)
            or state.has(ln, player)
            and state.has("Progressive Recruitment", player, 2)
            and state.has_group("EarlyDungeons", player, 10)
            )
    elif recruit_chance + 0.225 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 3)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            )
    elif recruit_chance + 0.326 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 4)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            )
    else:
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 5)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Secret Slab", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Mystery Part", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            )

def late_pokemon(location_name, player, world, recruit_chance, difficulty):
    if recruit_chance >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and ready_for_late_game(state, player, world)
            )
    elif recruit_chance + 0.100 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Friend Bow", player)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Progressive Recruitment", player, 2)
            and ready_for_late_game(state, player, world)
            )
    elif recruit_chance + 0.225 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 3)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Amber Tear", player)
            and ready_for_late_game(state, player, world)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            )
    elif recruit_chance + 0.326 >= difficulty: 
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 4)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            )
    else:
        return (
            lambda state, ln=location_name: state.has(ln, player)
            and state.has("Progressive Recruitment", player, 5)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Secret Slab", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            or state.has(ln, player)
            and state.has("Golden Mask", player)
            and state.has("Mystery Part", player)
            and ready_for_late_game(state, player, world)
            and state.has_group("LateDungeons", player, 10)
            and state.has("Secret Rank", player)
            )

def aegis_pokemon(location_name, amount, player, world, recruit_chance, difficulty):
    if amount == 1:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                and state.has_group("LateDungeons", player, 10)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                and state.has_group("LateDungeons", player, 10)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                )
    elif amount == 2:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 1)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                and state.has_group("LateDungeons", player, 10)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                and state.has_group("LateDungeons", player, 10)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 2)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                )
    elif amount == 3:
        if recruit_chance >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.100 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Friend Bow", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Progressive Recruitment", player, 2)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.225 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 3)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Amber Tear", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                )
        elif recruit_chance + 0.326 >= difficulty: 
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 4)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                and state.has_group("LateDungeons", player, 10)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                and state.has_group("LateDungeons", player, 10)
                )
        else:
            return (
                lambda state, ln=location_name: state.has(ln, player)
                and state.has("Progressive Recruitment", player, 5)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Secret Slab", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                or state.has(ln, player)
                and state.has("Golden Mask", player)
                and state.has("Mystery Part", player)
                and ready_for_late_game(state, player, world)
                and state.has("Progressive Seal", player, 3)
                and state.has_group("LateDungeons", player, 10)
                and state.has("Secret Rank", player)
                )
    return

def boss_pokemon(player, world, recruit_chance, difficulty):
    if recruit_chance >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            )
    elif recruit_chance + 0.100 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Friend Bow", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Amber Tear", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 2)
            )
    elif recruit_chance + 0.225 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 3)
            or ready_for_darkrai(state, player, world)
            and state.has("Amber Tear", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            )
    elif recruit_chance + 0.326 >= difficulty: 
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 4)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            )
    else:
        return (
            lambda state: ready_for_darkrai(state, player, world)
            and state.has("Progressive Recruitment", player, 5)
            and state.has("Secret Rank", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Secret Slab", player)
            and state.has("Secret Rank", player)
            or ready_for_darkrai(state, player, world)
            and state.has("Golden Mask", player)
            and state.has("Mystery Part", player)
            and state.has("Secret Rank", player)
            )

def dungeon_locations_behind_items(world, player):
    pokemeon_has_rule = [0] * 492
    for location in EOS_location_table:
        if location.name == "Beach Cave":
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
            continue
        elif "Early" in location.group:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Dojo" in location.group:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player)
                    or state.has("Bidoof's Wish", player)
                    or state.has('Today\'s "Oh My Gosh"', player),
                )
        elif "Pokemon" == location.classification:
            if world.options.recruit_sanity.value == 0:
                continue
            match world.options.recruit_sanity_difficulty.value:
                    case 0:
                        difficulty = 0.175 + 0.495
                    case 1:
                        difficulty = 0.125 + 0.495
                    case 2:
                        difficulty = 0.05 + 0.495
                    case 3:
                        difficulty = 0.001 + 0.495
                    case _:
                        difficulty = 0.5
            if (world.options.goal == 0):
                level = 20
            else:
                if (world.options.long_location.value == 1 and world.options.recruit_sanity_long_location.value == 1):
                    level = 100
                else:
                    level = 45
            if ((pokemon_info[location.id - 15000][1] + 0.496) < difficulty and world.options.goal == 1):
                continue
            elif ((pokemon_info[location.id - 15000][1] + 0.100) < difficulty and world.options.goal == 0):
                continue

            for i in range(len(location.group)):
                if(pokemon_info[location.id - 15000][5][i] == "Early"):
                    rule = early_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                    pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                    if world.options.recruit_sanity_evolution.value == 1:
                        early_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                        
                elif(pokemon_info[location.id - 15000][5][i] == "Late"):
                    if(world.options.goal == 0):
                        continue
                    rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                    pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                    if world.options.recruit_sanity_evolution.value == 1:
                        late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)

                elif(pokemon_info[location.id - 15000][5][i] == "Ice"):
                    if(world.options.goal == 0):
                        continue
                    rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                    pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                    if world.options.recruit_sanity_evolution.value == 1:
                        late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)

                elif(pokemon_info[location.id - 15000][5][i] == "Rock"):
                    if(world.options.goal == 0):
                        continue
                    if (world.options.cursed_aegis_cave.value == 1):
                        rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                    else:
                        rule = aegis_pokemon(location.group[i], 1, player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            aegis_pokemon_evolution_rule(location.id, location.group[i], location.name, level, 1, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                elif(pokemon_info[location.id - 15000][5][i] == "Steel"):
                    if(world.options.goal == 0):
                        continue
                    if (world.options.cursed_aegis_cave.value == 1):
                        rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                    else:
                        rule = aegis_pokemon(location.group[i], 2, player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            aegis_pokemon_evolution_rule(location.id, location.group[i], location.name, level, 2, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)

                elif(pokemon_info[location.id - 15000][5][i] == "Pit"):
                    if(world.options.goal == 0):
                        continue
                    if (world.options.cursed_aegis_cave.value == 1):
                        rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                    else:
                        rule = aegis_pokemon(location.group[i], 3, player, world, pokemon_info[location.id - 15000][1], difficulty)
                        pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                        if world.options.recruit_sanity_evolution.value == 1:
                            aegis_pokemon_evolution_rule(location.id, location.group[i], location.name, level, 3, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
                
                elif(pokemon_info[location.id - 15000][5][i] == "Boss"):
                    if(world.options.goal == 0):
                        continue
                    rule = boss_pokemon(player, world, pokemon_info[location.id - 15000][1], difficulty)
                    pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                    if world.options.recruit_sanity_evolution.value == 1:
                        boss_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)

                elif(pokemon_info[location.id - 15000][5][i] == "Long"):
                    if(world.options.long_location.value == 0 or world.options.recruit_sanity_long_location.value == 0 or world.options.goal == 0):
                        continue
                    rule = late_pokemon(location.group[i], player, world, pokemon_info[location.id - 15000][1], difficulty)
                    pokemon_rule(rule, world, player, location.name, location.id, pokemeon_has_rule)
                    if world.options.recruit_sanity_evolution.value == 1:
                        late_pokemon_evolution_rule(location.id, location.group[i], location.name, level, pokemeon_has_rule, player, world, pokemon_info[location.id - 15000][1], difficulty)
        
        elif "Station" in location.group and world.options.goal.value == 1:
            if world.options.sky_peak_type.value == 1:  # progressive
                if location.name == "Sky Peak Summit":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Progressive Sky Peak", player, 10)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.name == "5th Station Clearing":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Progressive Sky Peak", player, 5)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                else:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state, req_num=(location.id - 110): state.has("Progressive Sky Peak", player, req_num)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            elif world.options.sky_peak_type.value == 2:  # all random
                if location.name == "Sky Peak Summit":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Sky Peak Summit Pass", player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.name == "5th Station Clearing":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("5th Station Pass", player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                else:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state, ln=location.name: state.has(ln, player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            elif world.options.sky_peak_type.value == 3:  # all open from 1st station pass
                set_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
        elif "Aegis" in location.group and world.options.goal.value == 1:
            if world.options.cursed_aegis_cave.value == 0:
                if location.id in [54]:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player) and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [55, 56]:  # Regice Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 1),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [57, 58]:  # Regirock Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 2),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [59, 60, 61]:  # Registeel Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 3),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            else:
                set_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Ice Aegis Cave", player) and ready_for_late_game(state, player, world),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Main Game Unlock", player),
                    )

        elif "Late" in location.group and world.options.goal.value == 1:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Rule" in location.group and world.options.goal.value == 1:
            if world.options.long_location == 0:
                continue
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Special" in location.group:
            continue


def mission_rules(world, player):
    for i, location in enumerate(EOS_location_table):
        if "Mission" not in location.group:
            continue

        if location.name == "Beach Cave":
            if special_episode_sanity_no_exclusion(world, player):
                for j in range(world.options.early_mission_checks.value):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
                for j in range(world.options.early_outlaw_checks.value):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
            continue

        elif location.classification == "EarlyDungeonComplete":
            for j in range(world.options.early_mission_checks.value):
                set_rule(
                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                    lambda state, ln=location.name, p=player: state.has(ln, p),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
            for j in range(world.options.early_outlaw_checks.value):
                set_rule(
                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                    lambda state, ln=location.name, p=player: state.has(ln, p),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )

        elif location.classification in ["LateDungeonComplete", "BossDungeonComplete"]:
            if world.options.goal.value == 1:
                if "Station" in location.group:
                    if world.options.sky_peak_type == 1:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln="Progressive Sky Peak", num=(location.id - 110), p=player: state.has(
                                    ln, p, num
                                )
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln="Progressive Sky Peak", num=(location.id - 110), p=player: state.has(
                                    ln, p, num
                                )
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                    elif world.options.sky_peak_type == 2:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln=location.name, p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln=location.name, p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                    elif world.options.sky_peak_type == 3:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln="1st Station Pass", p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln="1st Station Pass", p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                elif location.name == "Hidden Land":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                elif location.name == "The Nightmare":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world)
                            and state.can_reach_location("Mt. Bristle", p)
                            and state.has(ln, p),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world)
                            and state.can_reach_location("Mt. Bristle", p)
                            and state.has(ln, p),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                else:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: state.has(ln, p)
                            and ready_for_late_game(state, player, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: state.has(ln, p)
                            and ready_for_late_game(state, player, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )


def subx_rules(world, player):
    for item in subX_table:
        if item.flag_definition == "Unused" or item.default_item == "ignore":
            continue
        if world.options.goal.value == 0 and item.classification in [
            "Manaphy",
            "LateSubX",
            "Legendary",
            "Instrument",
            "SecretRank",
        ]:
            continue
        if world.options.goal.value == 0 and item.flag_definition in [
            "Recycle Shop Dungeon #4",
            "Recycle Shop Dungeon #5",
        ]:
            continue
        if world.options.goal.value == 0 and item.flag_definition == "Bag Upgrade 5":
            continue
        # if world.options.long_location.value == 0 and item.classification in ["OptionalSubX"]:
        #   continue
        if item.classification == "Rank":
            rank_toid_dict = {
                "Bronze Rank": 1,
                "Silver Rank": 2,
                "Gold Rank": 3,
                "Diamond Rank": 4,
                "Super Rank": 5,
                "Ultra Rank": 6,
                "Hyper Rank": 7,
                "Master Rank": 8,
                "Master ★ Rank": 9,
                "Master ★★ Rank": 10,
                "Master ★★★ Rank": 11,
                "Guildmaster Rank": 12,
            }
            if rank_toid_dict[item.flag_definition] > world.options.max_rank:
                continue
            # if dialga is the goal, we can't add master star rank+
            if world.options.goal.value == 0 and rank_toid_dict[item.flag_definition] > 8:
                continue
        if (
            (special_episode_sanity_no_exclusion(world, player))
            and item.classification in ["Free", "ShopItem"]
            and "Main Game" not in item.prerequisites
        ):
            add_rule(
                world.multiworld.get_location(item.flag_definition, player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )
        elif special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location(item.flag_definition, player),
                lambda state: state.has("Main Game Unlock", player),
            )
        # if (item.flag_definition == "Manaphy's Discovery") and world.options.goal.value == 0:
        # continue
        for requirement in item.prerequisites:
            if requirement == "Defeat Dialga":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state: ready_for_late_game(state, player, world),
                )
            elif requirement == "Sky Peak Summit Pass":
                if world.options.sky_peak_type == 1:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Progressive Sky Peak": ready_for_late_game(state, player, world)
                        and state.has(req, player, 10),
                    )
                elif world.options.sky_peak_type == 2:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Sky Peak Summit Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
                elif world.options.sky_peak_type == 3:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="1st Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
            elif requirement == "7th Station Pass":
                if world.options.sky_peak_type == 1:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Progressive Sky Peak": ready_for_late_game(state, player, world)
                        and state.has(req, player, 7),
                    )
                elif world.options.sky_peak_type == 2:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="7th Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
                elif world.options.sky_peak_type == 3:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="1st Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
            elif requirement in ["ProgressiveBag1", "ProgressiveBag2", "ProgressiveBag3"]:
                bag_num_str = requirement[-1]
                bag_num = int(bag_num_str)
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Bag Upgrade", p=player, num=bag_num: state.has(req, p, num),
                )

            elif requirement in ["3 Early", "5 Early", "10 Early"]:
                dungeon_num_str = requirement[0:2]
                dungeon_num = int(dungeon_num_str)
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="EarlyDungeons", p=player, num=dungeon_num: state.has_group(req, p, num),
                )

            elif requirement == "Hidden Land":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state,
                    req="Relic Fragment Shard",
                    p=player,
                    num=world.options.required_fragments.value: state.has(req, p, num),
                )
            elif requirement == "Ice Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=1: state.has(req, p, num),
                )

            elif requirement == "Rock Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=2: state.has(req, p, num),
                )

            elif requirement == "Steel Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=3: state.has(req, p, num),
                )

            elif requirement == "All Mazes":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Dojo Dungeons", p=player: state.has_group(req, p, 10),
                )
            elif requirement == "Bidoof's Wish":
                if world.options.exclude_special.value:
                    continue
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req=requirement, p=player: state.has(req, p),
                )
            elif requirement == "Main Game":
                continue
            else:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req=requirement, p=player: state.has(req, p),
                )


def special_episode_sanity_no_exclusion(world, player) -> bool:
    if world.options.special_episode_sanity.value == 1 and not world.options.exclude_special.value:
        return True
    else:
        return False
