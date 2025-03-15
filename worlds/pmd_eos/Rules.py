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

    shop_items_rules(world, player)

    dungeon_locations_behind_items(world, player)
    instrument_and_legendary_rules(world, player)
    mission_rules(world, player)
    if world.options.goal.value == 0:
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: state.has("Dark Crater", player))
    elif world.options.goal.value == 1:
        set_rule(world.multiworld.get_location("Manaphy Leads To Marine Resort", player),
                 lambda state: state.has("Manaphy", player))
        set_rule(world.multiworld.get_location("Final Boss", player),
                 lambda state: ready_for_darkrai(state, player, world))
        set_rule(world.multiworld.get_location("Dark Crater", player),
                 lambda state: ready_for_darkrai(state, player, world))

    set_rule(world.multiworld.get_entrance("Late Game Door", player),
             lambda state: ready_for_late_game(state, player, world))
    forbid_item(world.multiworld.get_location("Hidden Land", player), "Relic Fragment Shard", player)
    forbid_item(world.multiworld.get_location("Temporal Tower", player), "Relic Fragment Shard", player)
    #set_rule(world.multiworld.get_entrance("Boss Door", player),
    #         lambda state: ready_for_final_boss(state, player))
    set_rule(world.multiworld.get_location("Hidden Land", player),
             lambda state: ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("Temporal Tower", player),
             lambda state: state.has("Temporal Tower", player) and ready_for_dialga(state, player, world))

    set_rule(world.multiworld.get_location("The Nightmare", player),
             lambda state: state.can_reach_location("Mt. Bristle", player) and state.has("The Nightmare", player)
                           and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Progressive Bag loc 2", player),
             lambda state: state.has("Mt. Bristle", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 3", player),
             lambda state: state.has("Apple Woods", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 4", player),
             lambda state: state.has("Steam Cave", player))
    set_rule(world.multiworld.get_location("Progressive Bag loc 5", player),
             lambda state: state.has("Mystifying Forest", player))

    set_rule(world.multiworld.get_location("Manaphy Egg Hatch", player),
             lambda state: state.has("Surrounded Sea", player))
    set_rule(world.multiworld.get_location("Manaphy Fed", player),
             lambda state: state.has("Surrounded Sea", player))
    set_rule(world.multiworld.get_location("Manaphy Healed", player),
             lambda state: state.has("Surrounded Sea", player) and state.has("Miracle Sea", player))
    set_rule(world.multiworld.get_location("Manaphy Join Team", player),
             lambda state: state.has("Surrounded Sea", player) and state.has("Miracle Sea", player))

    set_rule(world.multiworld.get_location("SecretRank", player),
             lambda state: state.has("Crevice Cave", player))
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
             lambda state: state.has("Mystifying Forest", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Blizzard Island", player),
             lambda state: state.has("Blizzard Island", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Crevice Cave", player),
             lambda state: state.has("Crevice Cave", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Surrounded Sea", player),
             lambda state: state.has("Surrounded Sea", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Miracle Sea", player),
             lambda state: state.has("Miracle Sea", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Mt. Travail", player),
             lambda state: state.has("Mt. Travail", player) and ready_for_late_game(state, player, world))
    #set_rule(world.multiworld.get_location("The Nightmare", player),
    #         lambda state: state.has("The Nightmare", player))
    set_rule(world.multiworld.get_location("Spacial Rift", player),
             lambda state: state.has("Spacial Rift", player) and ready_for_late_game(state, player, world))
    #set_rule(world.multiworld.get_location("Dark Crater", player),
    #         lambda state: state.has("Dark Crater", player))
    set_rule(world.multiworld.get_location("Concealed Ruins", player),
             lambda state: state.has("Concealed Ruins", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Marine Resort", player),
             lambda state: state.has("Marine Resort", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Bottomless Sea", player),
             lambda state: state.has("Bottomless Sea", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Shimmer Desert", player),
             lambda state: state.has("Shimmer Desert", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Mt. Avalanche", player),
             lambda state: state.has("Mt. Avalanche", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Giant Volcano", player),
             lambda state: state.has("Giant Volcano", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("World Abyss", player),
             lambda state: state.has("World Abyss", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Sky Stairway", player),
             lambda state: state.has("Sky Stairway", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Mystery Jungle", player),
             lambda state: state.has("Mystery Jungle", player) and ready_for_late_game(state, player, world))
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
             lambda state: state.has("Lake Afar", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Happy Outlook", player),
             lambda state: state.has("Happy Outlook", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Mt. Mistral", player),
             lambda state: state.has("Mt. Mistral", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Shimmer Hill", player),
             lambda state: state.has("Shimmer Hill", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Lost Wilderness", player),
             lambda state: state.has("Lost Wilderness", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Midnight Forest", player),
             lambda state: state.has("Midnight Forest", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Zero Isle North", player),
             lambda state: state.has("Zero Isle North", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Zero Isle East", player),
             lambda state: state.has("Zero Isle East", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Zero Isle West", player),
             lambda state: state.has("Zero Isle West", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Zero Isle South", player),
             lambda state: state.has("Zero Isle South", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Zero Isle Center", player),
             lambda state: state.has("Zero Isle Center", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Destiny Tower", player),
             lambda state: state.has("Destiny Tower", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Oblivion Forest", player),
             lambda state: state.has("Oblivion Forest", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Treacherous Waters", player),
             lambda state: state.has("Treacherous Waters", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Southeastern Islands", player),
             lambda state: state.has("Southeastern Islands", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Inferno Cave", player),
             lambda state: state.has("Inferno Cave", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("1st Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("1st Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))

    set_rule(world.multiworld.get_location("1st Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("2nd Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("3rd Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("4th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("5th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("6th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("7th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("8th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("9th Station Pass", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Sky Peak Summit", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("5th Station Clearing", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Sky Peak Summit", player),
             lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world))
    set_rule(world.multiworld.get_location("Star Cave", player),
             lambda state: state.has("Star Cave", player) and ready_for_late_game(state, player, world))

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


def mission_rules(world, player):
    for i, location in enumerate(EOS_location_table):
        if "Mission" not in location.group:
            continue
        if location.name == "Beach Cave":
            continue
        elif location.classification == "EarlyDungeonComplete":
            for j in range(world.options.early_mission_checks.value):
                set_rule(world.get_location(f"{location.name} Mission {j + 1}"),
                         lambda state, ln=location.name, p=player: state.has(ln, p))
            for j in range(world.options.early_outlaw_checks.value):
                set_rule(world.get_location(f"{location.name} Outlaw {j + 1}"),
                         lambda state, ln=location.name, p=player: state.has(ln, p))

        elif location.classification in ["LateDungeonComplete", "BossDungeonComplete"]:
            if world.options.goal.value == 1:
                if "Station" in location.group:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.get_location(f"{location.name} Mission {j + 1}"),
                                 lambda state, ln="1st Station Pass", p=player: state.has(ln, p))
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(world.get_location(f"{location.name} Outlaw {j + 1}"),
                                     lambda state, ln="1st Station Pass", p=player: state.has(ln, p))
                elif location.name == "Hidden Land":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.get_location(f"{location.name} Mission {j + 1}"),
                                 lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world))

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(world.get_location(f"{location.name} Outlaw {j + 1}"),
                                 lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world))
                else:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(world.get_location(f"{location.name} Mission {j + 1}"),
                                 lambda state, ln=location.name, p=player: state.has(ln, p))

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(world.get_location(f"{location.name} Outlaw {j + 1}"),
                                 lambda state, ln=location.name, p=player: state.has(ln, p))
