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
    subx_rules(world, player)
    dungeon_locations_behind_items(world, player)
    mission_rules(world, player)

    if world.options.goal.value == 0:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: state.has("Dark Crater", player) and ready_for_late_game(state, player, world))

    elif world.options.goal.value == 1:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: ready_for_darkrai(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: ready_for_darkrai(state, player, world))

    set_rule(world.multiworld.get_entrance("Late Game Door", player),
             lambda state: ready_for_late_game(state, player, world))

    set_rule(world.multiworld.get_location("Hidden Land", player),
             lambda state: has_relic_shards(state, player, world))

    set_rule(world.multiworld.get_location("Temporal Tower", player),
             lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world))

    set_rule(world.multiworld.get_location("The Nightmare", player),
             lambda state: state.can_reach_location("Mt. Bristle", player) and state.has("The Nightmare", player)
                           and ready_for_late_game(state, player, world))

    forbid_item(world.multiworld.get_location("Hidden Land", player), "Relic Fragment Shard", player)
    forbid_item(world.multiworld.get_location("Temporal Tower", player), "Relic Fragment Shard", player)


def has_relic_shards(state, player, world):
    return state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)


def ready_for_late_game(state, player, world):
    return (state.has_group("EarlyDungeons", player, 10)
            and state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
            and state.has("Temporal Tower", player))


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
             lambda state: has_relic_shards(state, player, world))
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
                     lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player,
                                                                                                   world))
        elif "Rule" in location.group:
            set_rule(world.multiworld.get_location(location.name, player),
                     lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player,
                                                                                                   world))
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
                         lambda state: ready_for_late_game(state, player, world))

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
