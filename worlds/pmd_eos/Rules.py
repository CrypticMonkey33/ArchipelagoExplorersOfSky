from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_rule, forbid_item
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id
from .Items import item_table_by_id
from .Options import EOSOptions

if TYPE_CHECKING:
    from . import EOSWorld


def set_rules(world: "EOSWorld", excluded):
    player = world.player
    options = world.options

    special_episodes_rules(world, player)

    dungeon_locations_behind_items(world, player)
    if world.options.goal.value == 0:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: state.has("Dark Crater", player))
    elif world.options.goal.value == 1:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: state.has("Temporal Tower", player) and ready_for_darkrai(state, player, world)
                               and state.has("Dark Crater", player))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: state.has("Dark Crater", player) and state.has("Temporal Tower", player)
                               and ready_for_darkrai(state, player, world))

    set_rule(world.multiworld.get_entrance("Late Game Door", player),
             lambda state: ready_for_late_game(state, player))
    #set_rule(world.multiworld.get_entrance("Boss Door", player),
    #         lambda state: ready_for_final_boss(state, player))
    set_rule(world.multiworld.get_location("Hidden Land", player),
             lambda state: ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("Temporal Tower", player),
             lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("The Nightmare", player),
             lambda state: state.can_reach_location("Mt. Bristle", player) and state.has("The Nightmare", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 2", player),
             lambda state: state.has("Drenched Bluff", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 3", player),
             lambda state: state.has("Mt. Bristle", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 4", player),
             lambda state: state.has("Waterfall Cave", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 5", player),
             lambda state: state.has("Apple Woods", player))
    #set_rule(world.multiworld.get_entrance("Early Game Door", player),
    #         lambda state: state.has("Beach Cave", player))
    #for location_num in location_Dict_by_id:
    #    location_start = location_Dict_by_id[location_num].dungeon_start_id
    #    if location_start in item_table_by_id:
    #        if location_start == 0:
    #            continue
    #        item_name = item_table_by_id[location_start].name
    #        if (item_name == "Beach Cave") or (location_start > 43):
    #            continue
    #        #forbid_item(world.multiworld.get_location(location_Dict_by_id[location_num].name, player),
    #        #            item_name,
    #        #            player)
    #        set_rule(world.multiworld.get_location(location_Dict_by_id[location_num].name, player),
    #                 lambda state: state.has(item_name, player))


def ready_for_dialga(state, player, world):
    return state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)


def ready_for_late_game(state, player):
    return state.has_group("EarlyDungeons", player, 5)


def special_episodes_rules(world, player):
    # Bidoof Special Episode Checks
    set_rule(world.multiworld.get_location("SE Star Cave", player),
             lambda state: state.has("Bidoof SE", player))

    # Igglybuff Special Episode checks
    set_rule(world.multiworld.get_location("SE Murky Forest", player),
             lambda state: state.has("IgglyBuff SE", player))
    set_rule(world.multiworld.get_location("SE Eastern Cave", player),
             lambda state: state.has("IgglyBuff SE", player))
    set_rule(world.multiworld.get_location("SE Fortune Ravine", player),
             lambda state: state.has("IgglyBuff SE", player))

    # Grovyle and Dusknoir Special Episode Checks
    set_rule(world.multiworld.get_location("SE Barren Valley", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Dark Wasteland", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Temporal Tower", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Dusk Forest", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Spacial Cliffs", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Dark Ice Mountain", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Icicle Forest", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))
    set_rule(world.multiworld.get_location("SE Vast Ice Mountain", player),
             lambda state: state.has("Grovyle + Dusknoir SE", player))

    # Team Charm Special Episode Checks
    set_rule(world.multiworld.get_location("SE Southern Jungle", player),
             lambda state: state.has("Team Charm SE", player))
    set_rule(world.multiworld.get_location("SE Boulder Quarry", player),
             lambda state: state.has("Team Charm SE", player))
    set_rule(world.multiworld.get_location("SE Right Cave Path", player),
             lambda state: state.has("Team Charm SE", player))
    set_rule(world.multiworld.get_location("SE Left Cave Path", player),
             lambda state: state.has("Team Charm SE", player))
    set_rule(world.multiworld.get_location("SE Limestone Cavern", player),
             lambda state: state.has("Team Charm SE", player))

    # Sunflora Special Episode Checks
    set_rule(world.multiworld.get_location("SE Spring Cave", player),
             lambda state: state.has("Sunflora SE", player))


def ready_for_darkrai(state, player, world):
    return (state.has("Relic Fragment Shard", player, world.options.shard_fragments.value)
            and state.has("Cresselia Feather", player))


def dungeon_locations_behind_items(world, player):
    set_rule(world.multiworld.get_location("Drenched Bluff", player),
             lambda state: state.has("Drenched Bluff", player))
    set_rule(world.multiworld.get_location("Mt. Bristle", player),
             lambda state: state.has("Mt. Bristle", player))
    set_rule(world.multiworld.get_location("Waterfall Cave", player),
             lambda state: state.has("Waterfall Cave", player))
    set_rule(world.multiworld.get_location("Apple Woods", player),
             lambda state: state.has("Apple Woods", player))
    set_rule(world.multiworld.get_location("Craggy Coast", player),
             lambda state: state.has("Craggy Coast", player))
    set_rule(world.multiworld.get_location("Side Path", player),
             lambda state: state.has("Side Path", player))
    set_rule(world.multiworld.get_location("Mt. Horn", player),
             lambda state: state.has("Mt. Horn", player))
    set_rule(world.multiworld.get_location("Rock Path", player),
             lambda state: state.has("Rock Path", player))
    set_rule(world.multiworld.get_location("Foggy Forest", player),
             lambda state: state.has("Foggy Forest", player))
    set_rule(world.multiworld.get_location("Forest Path", player),
             lambda state: state.has("Forest Path", player))
    set_rule(world.multiworld.get_location("Steam Cave", player),
             lambda state: state.has("Steam Cave", player))
    set_rule(world.multiworld.get_location("Amp Plains", player),
             lambda state: state.has("Amp Plains", player))
    set_rule(world.multiworld.get_location("Northern Desert", player),
             lambda state: state.has("Northern Desert", player))
    set_rule(world.multiworld.get_location("Quicksand Cave", player),
             lambda state: state.has("Quicksand Cave", player))
    set_rule(world.multiworld.get_location("Crystal Cave", player),
             lambda state: state.has("Crystal Cave", player))
    set_rule(world.multiworld.get_location("Crystal Crossing", player),
             lambda state: state.has("Crystal Crossing", player))
    set_rule(world.multiworld.get_location("Chasm Cave", player),
             lambda state: state.has("Chasm Cave", player))
    set_rule(world.multiworld.get_location("Dark Hill", player),
             lambda state: state.has("Dark Hill", player))
    set_rule(world.multiworld.get_location("Sealed Ruin", player),
             lambda state: state.has("Sealed Ruin", player))
    set_rule(world.multiworld.get_location("Dusk Forest", player),
             lambda state: state.has("Dusk Forest", player))
    set_rule(world.multiworld.get_location("Deep Dusk Forest", player),
             lambda state: state.has("Deep Dusk Forest", player))
    set_rule(world.multiworld.get_location("Treeshroud Forest", player),
             lambda state: state.has("Treeshroud Forest", player))
    set_rule(world.multiworld.get_location("Brine Cave", player),
             lambda state: state.has("Brine Cave", player))
    #set_rule(world.multiworld.get_location("Hidden Land", player),
    #         lambda state: state.has("Hidden Land", player))
    #set_rule(world.multiworld.get_location("Temporal Tower", player),
    #         lambda state: state.has("Temporal Tower", player))
    set_rule(world.multiworld.get_location("Mystifying Forest", player),
             lambda state: state.has("Mystifying Forest", player))
    set_rule(world.multiworld.get_location("Blizzard Island", player),
             lambda state: state.has("Blizzard Island", player))
    set_rule(world.multiworld.get_location("Crevice Cave", player),
             lambda state: state.has("Crevice Cave", player))
    set_rule(world.multiworld.get_location("Surrounded Sea", player),
             lambda state: state.has("Surrounded Sea", player))
    set_rule(world.multiworld.get_location("Miracle Sea", player),
             lambda state: state.has("Miracle Sea", player))
    set_rule(world.multiworld.get_location("Mt. Travail", player),
             lambda state: state.has("Mt. Travail", player))
    #set_rule(world.multiworld.get_location("The Nightmare", player),
    #         lambda state: state.has("The Nightmare", player))
    set_rule(world.multiworld.get_location("Spacial Rift", player),
             lambda state: state.has("Spacial Rift", player))
    #set_rule(world.multiworld.get_location("Dark Crater", player),
    #         lambda state: state.has("Dark Crater", player))
    set_rule(world.multiworld.get_location("Concealed Ruins", player),
             lambda state: state.has("Concealed Ruins", player))
    set_rule(world.multiworld.get_location("Marine Resort", player),
             lambda state: state.has("Marine Resort", player))
    set_rule(world.multiworld.get_location("Bottomless Sea", player),
             lambda state: state.has("Bottomless Sea", player))
    set_rule(world.multiworld.get_location("Shimmer Desert", player),
             lambda state: state.has("Shimmer Desert", player))
    set_rule(world.multiworld.get_location("Mt. Avalanche", player),
             lambda state: state.has("Mt. Avalanche", player))
    set_rule(world.multiworld.get_location("Giant Volcano", player),
             lambda state: state.has("Giant Volcano", player))
    set_rule(world.multiworld.get_location("World Abyss", player),
             lambda state: state.has("World Abyss", player))
    set_rule(world.multiworld.get_location("Sky Stairway", player),
             lambda state: state.has("Sky Stairway", player))
    set_rule(world.multiworld.get_location("Mystery Jungle", player),
             lambda state: state.has("Mystery Jungle", player))
    set_rule(world.multiworld.get_location("Serenity River", player),
             lambda state: state.has("Serenity River", player))
    set_rule(world.multiworld.get_location("Landslide Cave", player),
             lambda state: state.has("Landslide Cave", player))
    set_rule(world.multiworld.get_location("Lush Prairie", player),
             lambda state: state.has("Lush Prairie", player))
    set_rule(world.multiworld.get_location("Tiny Meadow", player),
             lambda state: state.has("Tiny Meadow", player))
    set_rule(world.multiworld.get_location("Labyrinth Cave", player),
             lambda state: state.has("Labyrinth Cave", player))
    set_rule(world.multiworld.get_location("Oran Forest", player),
             lambda state: state.has("Oran Forest", player))
    set_rule(world.multiworld.get_location("Lake Afar", player),
             lambda state: state.has("Lake Afar", player))
    set_rule(world.multiworld.get_location("Happy Outlook", player),
             lambda state: state.has("Happy Outlook", player))
    set_rule(world.multiworld.get_location("Mt. Mistral", player),
             lambda state: state.has("Mt. Mistral", player))
    set_rule(world.multiworld.get_location("Shimmer Hill", player),
             lambda state: state.has("Shimmer Hill", player))
    set_rule(world.multiworld.get_location("Lost Wilderness", player),
             lambda state: state.has("Lost Wilderness", player))
    set_rule(world.multiworld.get_location("Midnight Forest", player),
             lambda state: state.has("Midnight Forest", player))
    set_rule(world.multiworld.get_location("Zero Isle North", player),
             lambda state: state.has("Zero Isle North", player))
    set_rule(world.multiworld.get_location("Zero Isle East", player),
             lambda state: state.has("Zero Isle East", player))
    set_rule(world.multiworld.get_location("Zero Isle West", player),
             lambda state: state.has("Zero Isle West", player))
    set_rule(world.multiworld.get_location("Zero Isle South", player),
             lambda state: state.has("Zero Isle South", player))
    set_rule(world.multiworld.get_location("Zero Isle Center", player),
             lambda state: state.has("Zero Isle Center", player))
    set_rule(world.multiworld.get_location("Destiny Tower", player),
             lambda state: state.has("Destiny Tower", player))
    set_rule(world.multiworld.get_location("Oblivion Forest", player),
             lambda state: state.has("Oblivion Forest", player))
    set_rule(world.multiworld.get_location("Treacherous Waters", player),
             lambda state: state.has("Treacherous Waters", player))
    set_rule(world.multiworld.get_location("Southeastern Islands", player),
             lambda state: state.has("Southeastern Islands", player))
    set_rule(world.multiworld.get_location("Inferno Cave", player),
             lambda state: state.has("Inferno Cave", player))
    set_rule(world.multiworld.get_location("1st Station Pass", player),
             lambda state: state.has("1st Station Pass", player))
    set_rule(world.multiworld.get_location("Dojo Normal/Fly Maze", player),
             lambda state: state.has("Dojo Normal/Fly Maze", player))
    set_rule(world.multiworld.get_location("Dojo Dark/Fire Maze", player),
             lambda state: state.has("Dojo Dark/Fire Maze", player))
    set_rule(world.multiworld.get_location("Dojo Rock/Water Maze", player),
             lambda state: state.has("Dojo Rock/Water Maze", player))
    set_rule(world.multiworld.get_location("Dojo Grass Maze", player),
             lambda state: state.has("Dojo Grass Maze", player))
    set_rule(world.multiworld.get_location("Dojo Elec/Steel Maze", player),
             lambda state: state.has("Dojo Elec/Steel Maze", player))
    set_rule(world.multiworld.get_location("Dojo Ice/Ground Maze", player),
             lambda state: state.has("Dojo Ice/Ground Maze", player))
    set_rule(world.multiworld.get_location("Dojo Fight/Psych Maze", player),
             lambda state: state.has("Dojo Fight/Psych Maze", player))
    set_rule(world.multiworld.get_location("Dojo Poison/Bug Maze", player),
             lambda state: state.has("Dojo Poison/Bug Maze", player))
    set_rule(world.multiworld.get_location("Dojo Dragon Maze", player),
             lambda state: state.has("Dojo Dragon Maze", player))
    set_rule(world.multiworld.get_location("Dojo Ghost Maze", player),
             lambda state: state.has("Dojo Ghost Maze", player))
