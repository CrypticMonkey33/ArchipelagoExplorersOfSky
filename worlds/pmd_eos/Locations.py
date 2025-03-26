import typing

import typing_extensions
from typing import Dict
from BaseClasses import Location


class LocationData:
    name: str = ""
    classification: str = ""
    dungeon_length: int = 1
    id: int = -1
    dungeon_start_id: int = -1
    group: list[str] = [""]

    def __init__(self, classification, dungeon_length, name, id, dungeon_start_id, group=None):
        if group is None:
            group = [""]
        self.name = name
        self.classification = classification
        self.dungeon_length = dungeon_length
        self.id = id
        self.dungeon_start_id = dungeon_start_id
        self.group = group


class EOSLocation(Location):
    game: str = "Pokemon Mystery Dungeon Explorers of Sky"


def get_location_table_by_groups() -> Dict[str, set[str]]:
    #groups: Set[str] = set()
    new_dict: Dict[str, set[str]] = {}
    for location_name in location_table:
        if location_table[location_name].group:
            for group in location_table[location_name].group:
                #groups.add(group)
                if group in new_dict:
                    new_dict[group].add(location_name)
                else:
                    test_set = set("")
                    test_set.add(location_name)
                    new_dict.update({group: test_set})

    return new_dict


def get_mission_location_table() -> typing.List[LocationData]:

    new_list: typing.List[LocationData] = []

    for location in EOS_location_table:
        if location.name == "Beach Cave" and "Mission" in location.group:
            for j in range(50):
                location_name: str = f"{location.name} Mission {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))
            for j in range(50):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", 0, location_name, location_id, 0, []))

        elif location.classification == "EarlyDungeonComplete" and "Mission" in location.group:
            for j in range(50):
                location_name = f"{location.name} Mission {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))

            for j in range(50):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", 0, location_name, location_id, 0, []))

        elif "Mission" in location.group and (location.classification == "LateDungeonComplete"
                                              or location.classification == "BossDungeonComplete"):
            for j in range(50):
                location_name = f"{location.name} Mission {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))

            for j in range(50):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + 500 + (100 * location.id) + j + 50
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))

    return new_list


def get_location_table_by_start_id() -> Dict[int, set[str]]:
    #groups: Set[str] = set()
    new_dict: Dict[int, set[str]] = {}
    for location_name in location_table:
        if location_table[location_name].group:
            for group in location_table[location_name].group:
                #groups.add(group)
                if group in new_dict:
                    new_dict[group].add(location_name)
                else:
                    test_set = set("")
                    test_set.add(location_name)
                    new_dict.update({group: test_set})

    return new_dict


EOS_location_table: typing.List[LocationData] = [
    # "Test Dungeon", 0,  # Should be unused
    LocationData("EarlyDungeonComplete", 2,  "Beach Cave", 2,  1, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Drenched Bluff", 3, 3, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 2, "Mt. Bristle", 5, 4, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Waterfall Cave", 6, 6, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Apple Woods", 7, 7, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Craggy Coast", 8, 8, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Side Path", 9, 9, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Mt. Horn", 10, 10, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Rock Path", 11, 11, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Foggy Forest", 12, 12, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Forest Path", 13, 13, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Steam Cave", 16, 14, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 3, "Amp Plains", 19, 17, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Northern Desert", 20, 20, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Quicksand Cave", 23, 21, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Crystal Cave", 24, 24, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 2, "Crystal Crossing", 26, 25, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Chasm Cave", 27, 27, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Dark Hill", 28, 28, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Sealed Ruin", 31, 29, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Dusk Forest", 32, 32, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Deep Dusk Forest", 33, 33, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Treeshroud Forest", 34, 34, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Brine Cave", 37, 35, ["Mission", "Early"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Hidden Land", 40, 38, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Temporal Tower", 43, 41, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", 2, "Mystifying Forest", 45, 44, ["Mission", "Late"]),  # start of extra levels
    LocationData("LateDungeonComplete", 1, "Blizzard Island", 46, 46, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Crevice Cave", 49, 47, ["Mission", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", 1, "Surrounded Sea", 50, 50, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Miracle Sea", 53, 51, ["Mission", "Late"]),  # 3 subareas
    # LocationData("DungeonComplete", 8,  "Ice Aegis Cave", 60,  54),   # 8 subareas             we hate aegis cave. also it's kinda broken rn so we're gonna remove it for now
    LocationData("LateDungeonComplete", 1, "Mt. Travail", 62, 62, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "The Nightmare", 63, 63, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Spacial Rift", 66, 64, ["Mission", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Dark Crater", 69, 67, ["Boss"]),  # 3 subareas
    LocationData("LateDungeonComplete", 1, "Concealed Ruins", 70, 70, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 1, "Marine Resort", 72, 72, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 2, "Bottomless Sea", 73, 73, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Shimmer Desert", 75, 75, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Mt. Avalanche", 77, 77, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Giant Volcano", 79, 79, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "World Abyss", 81, 81, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Sky Stairway", 83, 83, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Mystery Jungle", 85, 85, ["Mission", "Late"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Serenity River", 87, 87, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Landslide Cave", 88, 88, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Lush Prairie", 89, 89, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Tiny Meadow", 90, 90, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Labyrinth Cave", 91, 91, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Oran Forest", 92, 92, ["Mission", "Early"]),
    LocationData("LateDungeonComplete", 1, "Lake Afar", 93, 93, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Happy Outlook", 94, 94, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Mt. Mistral", 95, 95, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Shimmer Hill", 96, 96, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Lost Wilderness", 97, 97, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Midnight Forest", 98, 98, ["Mission", "Late"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle North", 99, 99, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle East", 100, 100, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle West", 101, 101, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle South", 102, 102, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle Center", 103, 103, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Destiny Tower", 104, 104, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Oblivion Forest", 107, 107, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Treacherous Waters", 108, 108, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Southeastern Islands", 109, 109, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Inferno Cave", 110, 110, ["Rule"]),
    LocationData("LateDungeonComplete", 1, "1st Station Pass", 111, 111, ["Mission", "Late"]),  # 12 subareas
    LocationData("LateDungeonComplete", 1, "2nd Station Pass", 112, 112, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "3rd Station Pass", 113, 113, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "4th Station Pass", 114, 114, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "5th Station Pass", 115, 115, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "6th Station Pass", 116, 116, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "7th Station Pass", 117, 117, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "8th Station Pass", 118, 118, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "9th Station Pass", 119, 119, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "Sky Peak Summit Pass", 120, 120, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "5th Station Clearing", 121, 121, ["Late"]),
    LocationData("LateDungeonComplete", 1, "Sky Peak Summit", 122, 122, ["Late"]),
    # Special Episode Dungeons
    LocationData("SpecialDungeonComplete", 5, "SE Star Cave", 127, 123),
    LocationData("SpecialDungeonComplete", 1,  "SE Murky Forest", 128,  128),
    LocationData("SpecialDungeonComplete", 1,  "SE Eastern Cave", 129,  129),
    LocationData("SpecialDungeonComplete", 3,  "SE Fortune Ravine", 132,  130),   # 3 subareas
    LocationData("SpecialDungeonComplete", 3,  "SE Barren Valley", 135,  133),   # 3 subareas
    LocationData("SpecialDungeonComplete", 1,  "SE Dark Wasteland", 136,  136),
    LocationData("SpecialDungeonComplete", 2,  "SE Temporal Tower", 138,  137),   # 2 subareas
    LocationData("SpecialDungeonComplete", 2,  "SE Dusk Forest", 140,  139),   # 2 subareas
    LocationData("SpecialDungeonComplete", 1,  "SE Spacial Cliffs", 141,  141),
    LocationData("SpecialDungeonComplete", 3,  "SE Dark Ice Mountain", 144,  142),   # 3 subareas
    LocationData("SpecialDungeonComplete", 1,  "SE Icicle Forest", 145,  145),
    LocationData("SpecialDungeonComplete", 3,  "SE Vast Ice Mountain", 148,  146),   # 3 subareas
    LocationData("SpecialDungeonComplete", 1,  "SE Southern Jungle", 149,  149),
    LocationData("SpecialDungeonComplete", 3,  "SE Boulder Quarry", 152,  150),   # 3 subareas
    LocationData("SpecialDungeonComplete", 1,  "SE Right Cave Path", 153,  153),
    LocationData("SpecialDungeonComplete", 1,  "SE Left Cave Path", 154,  154),
    LocationData("SpecialDungeonComplete", 3,  "SE Limestone Cavern", 157,  155),   # 3 subareas
    LocationData("SpecialDungeonComplete", 2,  "SE Upper Spring Cave", 159,  158),   # 7 subareas
    LocationData("SpecialDungeonComplete", 2, "SE Middle Spring Cave", 161, 160),  # 7 subareas
    LocationData("SpecialDungeonComplete", 3, "SE Spring Cave Pit", 164, 162),  # 7 subareas

    LocationData("LateDungeonComplete", 1, "Star Cave", 174,  174, ["Mission", "Late"]),
    # Dojo Dungeons
    LocationData("DojoDungeonComplete", 1, "Dojo Normal/Fly Maze", 180, 180),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Dark/Fire Maze", 181, 181),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Rock/Water Maze", 182, 182),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Grass Maze", 183, 183),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Elec/Steel Maze", 184, 184),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Ice/Ground Maze", 185, 185),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Fight/Psych Maze", 186, 186),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Poison/Bug Maze", 187, 187),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Dragon Maze", 188, 188),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Ghost Maze", 189, 189),  # 7 subareas
    #LocationData("RuleDungeonComplete", 1, "Dojo Final Maze", 191, 191),  # 7 subareas

    LocationData("Event", 0,  "Final Boss", 400, 0),
    # generic checks, right now just bag upgrades
    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 1", 300, 0),
    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 2", 301, 0),
    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 3", 302, 0),
    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 4", 303, 0),
    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 5", 304, 0),

    LocationData("SEDungeonUnlock", 0, "Bidoof's Wish Location", 305, 0),
    LocationData("SEDungeonUnlock", 0, "Igglybuff the Prodigy Location", 306, 0),
    LocationData("SEDungeonUnlock", 0, 'Today\'s "Oh My Gosh" Location', 307, 0),
    LocationData("SEDungeonUnlock", 0, "Here Comes Team Charm! Location", 308, 0),
    LocationData("SEDungeonUnlock", 0, "In the Future of Darkness Location", 309, 0),

    LocationData("ShopItem", 0, "Shop Item 1", 310, 0),
    LocationData("ShopItem", 0, "Shop Item 2", 311, 0),
    LocationData("ShopItem", 0, "Shop Item 3", 312, 0),
    LocationData("ShopItem", 0, "Shop Item 4", 313, 0),
    LocationData("ShopItem", 0, "Shop Item 5", 314, 0),
    LocationData("ShopItem", 0, "Shop Item 6", 315, 0),
    LocationData("ShopItem", 0, "Shop Item 7", 316, 0),
    LocationData("ShopItem", 0, "Shop Item 8", 317, 0),
    LocationData("ShopItem", 0, "Shop Item 9", 318, 0),
    LocationData("ShopItem", 0, "Shop Item 10", 319, 0),
    LocationData("SEDungeonUnlock", 0, "Team Name", 427, 0),
    LocationData("Manaphy", 0, "Manaphy Egg Hatch", 320, 0),
    LocationData("Manaphy", 0, "Manaphy Fed", 321, 0),
    LocationData("Manaphy", 0, "Manaphy Healed", 322, 0),
    LocationData("Manaphy", 0, "Manaphy Join Team", 323, 0),
    LocationData("Manaphy", 0, "Manaphy Leads To Marine Resort", 324, 0),
    LocationData("SecretRank", 0, "SecretRank", 347, 0),

    LocationData("Legendary", 0, "Recruit Uxie", 325, 0),
    LocationData("Legendary", 0, "Recruit Mespirit", 326, 0),
    LocationData("Legendary", 0, "Recruit Azelf", 327, 0),
    LocationData("Legendary", 0, "Recruit Dialga", 328, 0),
    LocationData("Legendary", 0, "Recruit Phione", 329, 0),
    LocationData("Legendary", 0, "Recruit Palkia", 330, 0),
    LocationData("Legendary", 0, "Recruit Kyogre", 332, 0),
    LocationData("Legendary", 0, "Recruit Groudon", 334, 0),
    LocationData("Legendary", 0, "Recruit Articuno", 336, 0),
    LocationData("Legendary", 0, "Recruit Heatran", 338, 0),
    LocationData("Legendary", 0, "Recruit Giratina", 340, 0),
    LocationData("Legendary", 0, "Recruit Rayquaza", 342, 0),
    LocationData("Legendary", 0, "Recruit Mew", 344, 0),
    LocationData("Legendary", 0, "Recruit Cresselia", 345, 0),
    LocationData("Legendary", 0, "Recruit Shaymin", 346, 0),

    LocationData("Instrument", 0, "Get Aqua-Monica", 331, 0),
    LocationData("Instrument", 0, "Get Terra Cymbal", 333, 0),
    LocationData("Instrument", 0, "Get Icy Flute", 335, 0),
    LocationData("Instrument", 0, "Get Fiery Drum", 337, 0),
    LocationData("Instrument", 0, "Get Rock Horn", 339, 0),
    LocationData("Instrument", 0, "Get Sky Melodica", 341, 0),
    LocationData("Instrument", 0, "Get Grass Cornet", 343, 0),

]

location_Dict_by_id: typing.Dict[int, LocationData] = {location.id: location for location in EOS_location_table}
location_table: Dict[str, LocationData] = {location.name: location for location in EOS_location_table}

location_table_by_groups = get_location_table_by_groups()

location_dict_by_start_id: typing.Dict[int, LocationData] = {location.dungeon_start_id: location for location in EOS_location_table}

mission_location_table = get_mission_location_table()

expanded_EOS_location_table: typing.List[LocationData] = []
expanded_EOS_location_table.extend(EOS_location_table)
expanded_EOS_location_table.extend(mission_location_table)
