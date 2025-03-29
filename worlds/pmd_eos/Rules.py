from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_rule, forbid_item
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id
from .Items import item_table_by_id, EOS_item_table
from .Options import EOSOptions
from .RomTypeDefinitions import subX_table

if TYPE_CHECKING:
    from . import EOSWorld


def set_rules(world: "EOSWorld", excluded):
    player = world.player
    options = world.options

    special_episodes_rules(world, player)

    #shop_items_rules(world, player)
    subx_rules(world, player)
    dungeon_locations_behind_items(world, player)
    #instrument_and_legendary_rules(world, player)
    mission_rules(world, player)
    if world.options.goal.value == 0:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: state.has("Dark Crater", player))
    elif world.options.goal.value == 1:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: ready_for_darkrai(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: ready_for_darkrai(state, player, world))

    set_rule(world.multiworld.get_entrance("Late Game Door", player),
             lambda state: ready_for_late_game(state, player, world))
    forbid_item(world.multiworld.get_location("Hidden Land", player), "Relic Fragment Shard", player)
    forbid_item(world.multiworld.get_location("Temporal Tower", player), "Relic Fragment Shard", player)

    set_rule(world.multiworld.get_location("Hidden Land", player),
             lambda state: ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("Temporal Tower", player),
             lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("The Nightmare", player),
             lambda state: state.can_reach_location("Mt. Bristle", player) and state.has("The Nightmare", player)
                           and ready_for_late_game(state, player, world))



def ready_for_dialga(state, player, world):
    return state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)


def ready_for_late_game(state, player, world):
    return (state.has_group("EarlyDungeons", player, 10)
            and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
            and state.has("Temporal Tower", player))


def instrument_and_legendary_rules(world, player):
    set_rule(world.multiworld.get_location("Get Aqua-Monica", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Bottomless Sea", player))
    set_rule(world.multiworld.get_location("Get Terra Cymbal", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Shimmer Desert", player))
    set_rule(world.multiworld.get_location("Get Icy Flute", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Mt. Avalanche", player))
    set_rule(world.multiworld.get_location("Get Fiery Drum", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Giant Volcano", player))
    set_rule(world.multiworld.get_location("Get Rock Horn", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("World Abyss", player))
    set_rule(world.multiworld.get_location("Get Sky Melodica", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Sky Stairway", player))
    set_rule(world.multiworld.get_location("Get Grass Cornet", player),
             lambda state: state.has("Secret Rank", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Mystery Jungle", player))

    #Legendary Recruitment
    set_rule(world.multiworld.get_location("Recruit Uxie", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Steam Cave", player))
    set_rule(world.multiworld.get_location("Recruit Mespirit", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Quicksand Cave", player))
    set_rule(world.multiworld.get_location("Recruit Azelf", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Crystal Crossing", player)
             )
    set_rule(world.multiworld.get_location("Recruit Dialga", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
             )
    set_rule(world.multiworld.get_location("Recruit Phione", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Miracle Sea", player)
                           and state.has("Surrounded Sea", player)
             )
    set_rule(world.multiworld.get_location("Recruit Palkia", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Spacial Rift", player)
             )
    set_rule(world.multiworld.get_location("Recruit Kyogre", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Bottomless Sea", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Groudon", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Shimmer Desert", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Articuno", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Mt. Avalanche", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Heatran", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Giant Volcano", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Giratina", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("World Abyss", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Rayquaza", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Sky Stairway", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Mew", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
                           and state.has("Mystery Jungle", player)
                           and state.has("Secret Rank", player)
             )
    set_rule(world.multiworld.get_location("Recruit Cresselia", player),
             lambda state: state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
             )
    set_rule(world.multiworld.get_location("Recruit Shaymin", player),
             lambda state: state.has("1st Station Pass", player)
                           and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
                           and state.has("Temporal Tower", player)
             )


def shop_items_rules(world, player):
    set_rule(world.multiworld.get_location("Shop Item 1", player),
             lambda state: state.has_group("ProgressiveBag", player, 3))  # 5k cost
    set_rule(world.multiworld.get_location("Shop Item 2", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 1k cost
    set_rule(world.multiworld.get_location("Shop Item 3", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 1k cost
    set_rule(world.multiworld.get_location("Shop Item 4", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 1k cost
    set_rule(world.multiworld.get_location("Shop Item 5", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 1k cost
    set_rule(world.multiworld.get_location("Shop Item 6", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 1k cost
    set_rule(world.multiworld.get_location("Shop Item 7", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 500 cost
    set_rule(world.multiworld.get_location("Shop Item 8", player),
             lambda state: state.has_group("ProgressiveBag", player, 2))  # 500 cost
    set_rule(world.multiworld.get_location("Shop Item 9", player),
             lambda state: state.has_group("ProgressiveBag", player, 3))  # 5k cost
    #set_rule(world.multiworld.get_location("Shop Item 10", player),
    #         lambda state: state.has_group("Bag Upgrade", player, 3))  # 100 cost


def special_episodes_rules(world, player):
    # Bidoof Special Episode Checks
    set_rule(world.multiworld.get_location("SE Star Cave", player),
             lambda state: state.has("Bidoof\'s Wish", player))

    # Igglybuff Special Episode checks
    set_rule(world.multiworld.get_location("SE Murky Forest", player),
             lambda state: state.has("Igglybuff the Prodigy", player))
    set_rule(world.multiworld.get_location("SE Eastern Cave", player),
             lambda state: state.has("Igglybuff the Prodigy", player))
    set_rule(world.multiworld.get_location("SE Fortune Ravine", player),
             lambda state: state.has("Igglybuff the Prodigy", player))

    # Grovyle and Dusknoir Special Episode Checks
    set_rule(world.multiworld.get_location("In the Future of Darkness Location", player),
             lambda state: ready_for_dialga(state, player, world))
    set_rule(world.multiworld.get_location("SE Barren Valley", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Dark Wasteland", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Temporal Tower", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Dusk Forest", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Spacial Cliffs", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Dark Ice Mountain", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Icicle Forest", player),
             lambda state: state.has("In the Future of Darkness", player))
    set_rule(world.multiworld.get_location("SE Vast Ice Mountain", player),
             lambda state: state.has("In the Future of Darkness", player))

    # Team Charm Special Episode Checks
    set_rule(world.multiworld.get_location("SE Southern Jungle", player),
             lambda state: state.has("Here Comes Team Charm!", player))
    set_rule(world.multiworld.get_location("SE Boulder Quarry", player),
             lambda state: state.has("Here Comes Team Charm!", player))
    set_rule(world.multiworld.get_location("SE Right Cave Path", player),
             lambda state: state.has("Here Comes Team Charm!", player))
    set_rule(world.multiworld.get_location("SE Left Cave Path", player),
             lambda state: state.has("Here Comes Team Charm!", player))
    set_rule(world.multiworld.get_location("SE Limestone Cavern", player),
             lambda state: state.has("Here Comes Team Charm!", player))

    # Sunflora Special Episode Checks
    set_rule(world.multiworld.get_location("SE Upper Spring Cave", player),
             lambda state: state.has('Today\'s "Oh My Gosh"', player))
    set_rule(world.multiworld.get_location("SE Middle Spring Cave", player),
             lambda state: state.has('Today\'s "Oh My Gosh"', player))
    set_rule(world.multiworld.get_location("SE Spring Cave Pit", player),
             lambda state: state.has('Today\'s "Oh My Gosh"', player))


def ready_for_darkrai(state, player, world):
    return (state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
            and state.has("Temporal Tower", player)
            and state.has_group("Instrument", player, world.options.req_instruments.value)
            and state.has_group("LateDungeons", player, 10))


def dungeon_locations_behind_items(world, player):
    for location in EOS_location_table:
        if location.name == "Beach Cave":
            continue
        elif "Early" in location.group or "Dojo" in location.group:
            set_rule(world.multiworld.get_location(location.name, player),
                     lambda state, ln=location.name: state.has(ln, player))
        elif "Station" in location.group:
            set_rule(world.multiworld.get_location(location.name, player),
                     lambda state, ln=location.name: state.has("1st Station Pass", player)
                                                     and ready_for_late_game(state, player, world))
        elif "Late" in location.group:
            set_rule(world.multiworld.get_location(location.name, player),
                     lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world))
        elif "Rule" in location.group:
            set_rule(world.multiworld.get_location(location.name, player),
                     lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world))
        elif "Special" in location.group:
            continue


def mission_rules(world, player):
    for i, location in enumerate(EOS_location_table):
        if "Mission" not in location.group:
            continue
        if location.name == "Beach Cave":
            continue
        elif location.classification == "EarlyDungeonComplete":
            for j in range(world.options.early_mission_checks.value):
                set_rule(world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                         lambda state, ln=location.name, p=player: state.has(ln, p))
            for j in range(world.options.early_outlaw_checks.value):
                set_rule(world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                         lambda state, ln=location.name, p=player: state.has(ln, p))

        elif location.classification in ["LateDungeonComplete", "BossDungeonComplete"]:
            if world.options.goal.value == 1:
                if "Station" in location.group:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                 lambda state, ln="1st Station Pass", p=player: state.has(ln, p))
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                     lambda state, ln="1st Station Pass", p=player: state.has(ln, p))
                elif location.name == "Hidden Land":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                 lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world))

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                 lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world))
                else:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                 lambda state, ln=location.name, p=player: state.has(ln, p))

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                 lambda state, ln=location.name, p=player: state.has(ln, p))


def subx_rules(world, player):

    for item in subX_table:
        if item.flag_definition == "Unused":
            continue
        if (item.flag_definition == "Manaphy's Discovery") and world.options.goal.value == 0:
            continue
        for requirement in item.prerequisites:
            if requirement == "Defeat Dialga":
                add_rule(world.multiworld.get_location(item.flag_definition, player),
                         lambda state, req="Relic Fragment Shard", p=player,
                                num=world.options.shard_fragments.value, req2="Temporal Tower":
                                state.has(req, p, num) and state.has(req2, p))

            elif requirement in ["ProgressiveBag1", "ProgressiveBag2", "ProgressiveBag3"]:
                bag_num_str = requirement[-1]
                bag_num = int(bag_num_str)
                add_rule(world.multiworld.get_location(item.flag_definition, player),
                     lambda state, req="Bag Upgrade", p=player, num=bag_num: state.has(req, p, num))

            elif requirement == "Hidden Land":
                add_rule(world.multiworld.get_location(item.flag_definition, player),
                         lambda state, req="Relic Fragment Shard", p=player,
                                num=world.options.shard_fragments.value: state.has(req, p, num))

            elif requirement == "All Mazes":
                add_rule(world.multiworld.get_location(item.flag_definition, player),
                         lambda state, req="Dojo Dungeons", p=player: state.has_group(req, p, 10))

            else:
                add_rule(world.multiworld.get_location(item.flag_definition, player),
                     lambda state, req=requirement, p=player: state.has(req, p))

