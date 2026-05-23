import typing

from typing import Dict, List
from BaseClasses import Location
from .rom_type_definitions import subX_table


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
    game: str = "Pokémon Mystery Dungeon: Explorers of Sky"


def get_location_table_by_groups() -> Dict[str, set[str]]:
    # groups: Set[str] = set()
    new_dict: Dict[str, set[str]] = {}
    for location_name in location_table:
        if location_table[location_name].group:
            for group in location_table[location_name].group:
                # groups.add(group)
                if group in new_dict:
                    new_dict[group].add(location_name)
                else:
                    test_set = set("")
                    test_set.add(location_name)
                    new_dict.update({group: test_set})

    return new_dict


def get_subx_table() -> List[LocationData]:
    new_list: List[LocationData] = []
    subX_start_id = 300
    for item in subX_table:
        if item.flag_definition == "Unused" or item.default_item == "ignore":
            continue
        new_location = LocationData(
            classification=item.classification,
            dungeon_length=0,
            name=item.flag_definition,
            id=subX_start_id + item.bitfield_bit_number,
            dungeon_start_id=0,
            group=["SubX"],
        )
        new_list.append(new_location)

    return new_list


def get_mission_location_table() -> typing.List[LocationData]:
    mission_start_id = 1000
    new_list: typing.List[LocationData] = []

    for location in EOS_location_table:
        loc_temp_name = location.name[:-8]
        if loc_temp_name == "Beach Cave" and "Mission" in location.group:

            for j in range(50):
                location_name: str = f"{loc_temp_name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))
            for j in range(50):
                location_name = f"{loc_temp_name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", 0, location_name, location_id, 0, []))

        elif location.classification == "EarlyDungeonComplete" and "Mission" in location.group:
            for j in range(31):
                location_name = f"{loc_temp_name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))

            for j in range(31):
                location_name = f"{loc_temp_name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", 0, location_name, location_id, 0, []))

        elif "Mission" in location.group and (
            location.classification == "LateDungeonComplete" or location.classification == "BossDungeonComplete"
        ):
            for j in range(31):
                location_name = f"{loc_temp_name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", 0, location_name, location_id, 0, []))

            for j in range(31):
                location_name = f"{loc_temp_name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", 0, location_name, location_id, 0, []))

    return new_list


subx_location_list = get_subx_table()
subx_location_dict = {location.name: location for location in subx_location_list}

EOS_location_table: typing.List[LocationData] = [
    # "Test Dungeon", 0,  # Should be unused
    LocationData("EarlyDungeonComplete", 2, "Beach Cave Cleared", 2, 1, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Drenched Bluff Cleared", 3, 3, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 2, "Mt. Bristle Cleared", 5, 4, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Waterfall Cave Cleared", 6, 6, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Apple Woods Cleared", 7, 7, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Craggy Coast Cleared", 8, 8, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Side Path Cleared", 9, 9, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Mt. Horn Cleared", 10, 10, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Rock Path Cleared", 11, 11, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Foggy Forest Cleared", 12, 12, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Forest Path Cleared", 13, 13, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Steam Cave Cleared", 16, 14, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 3, "Amp Plains Cleared", 19, 17, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Northern Desert Cleared", 20, 20, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Quicksand Cave Cleared", 23, 21, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Crystal Cave Cleared", 24, 24, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 2, "Crystal Crossing Cleared", 26, 25, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Chasm Cave Cleared", 27, 27, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Dark Hill Cleared", 28, 28, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Sealed Ruin Cleared", 31, 29, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", 1, "Dusk Forest Cleared", 32, 32, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Deep Dusk Forest Cleared", 33, 33, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Treeshroud Forest Cleared", 34, 34, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 3, "Brine Cave Cleared", 37, 35, ["Mission", "Early"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Hidden Land Cleared", 40, 38, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Temporal Tower Cleared", 43, 41, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", 2, "Mystifying Forest Cleared", 45, 44, ["Mission", "Late"]),  # start of extra levels
    LocationData("LateDungeonComplete", 1, "Blizzard Island Cleared", 46, 46, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Crevice Cave Cleared", 49, 47, ["Mission", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", 1, "Surrounded Sea Cleared", 50, 50, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Miracle Sea Cleared", 52, 51, ["Mission", "Late"]),  # 3 subareas
    # LocationData("DungeonComplete", 8,  "Ice Aegis Cave", 60,  54),   # 8 subareas             we hate aegis cave. also it's kinda broken rn so we're gonna remove it for now
    LocationData("LateDungeonComplete", 1, "Ice Aegis Cave Cleared", 54, 54, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Regice Chamber Cleared", 55, 55, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Rock Aegis Cave Cleared", 56, 56, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Regirock Chamber Cleared", 57, 57, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Steel Aegis Cave Cleared", 58, 58, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Registeel Chamber Cleared", 59, 59, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Aegis Cave Pit Cleared", 60, 60, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Regigigas Chamber Cleared", 61, 61, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", 1, "Mt. Travail Cleared", 62, 62, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "The Nightmare Cleared", 63, 63, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 3, "Spacial Rift Cleared", 66, 64, ["Mission", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", 3, "Dark Crater Cleared", 69, 67, ["Boss"]),  # 3 subareas
    LocationData("LateDungeonComplete", 1, "Concealed Ruins Cleared", 70, 70, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 1, "Marine Resort Cleared", 72, 72, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 2, "Bottomless Sea Cleared", 73, 73, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Shimmer Desert Cleared", 75, 75, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Mt. Avalanche Cleared", 77, 77, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Giant Volcano Cleared", 79, 79, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "World Abyss Cleared", 81, 81, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Sky Stairway Cleared", 83, 83, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", 2, "Mystery Jungle Cleared", 85, 85, ["Mission", "Late"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", 1, "Serenity River Cleared", 87, 87, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Landslide Cave Cleared", 88, 88, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Lush Prairie Cleared", 89, 89, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Tiny Meadow Cleared", 90, 90, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Labyrinth Cave Cleared", 91, 91, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", 1, "Oran Forest Cleared", 92, 92, ["Mission", "Early"]),
    LocationData("LateDungeonComplete", 1, "Lake Afar Cleared", 93, 93, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Happy Outlook Cleared", 94, 94, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Mt. Mistral Cleared", 95, 95, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Shimmer Hill Cleared", 96, 96, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Lost Wilderness Cleared", 97, 97, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", 1, "Midnight Forest Cleared", 98, 98, ["Mission", "Late"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle North Cleared", 99, 99, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle East Cleared", 100, 100, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle West Cleared", 101, 101, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle South Cleared", 102, 102, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Zero Isle Center Cleared", 103, 103, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Destiny Tower Cleared", 104, 104, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Oblivion Forest Cleared", 107, 107, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Treacherous Waters Cleared", 108, 108, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Southeastern Islands Cleared", 109, 109, ["Rule"]),
    LocationData("RuleDungeonComplete", 1, "Inferno Cave Cleared", 110, 110, ["Rule"]),
    LocationData("LateDungeonComplete", 1, "1st Station Pass Cleared", 111, 111, ["Mission", "Late", "Station"]),  # 12 subareas
    LocationData("LateDungeonComplete", 1, "2nd Station Pass Cleared", 112, 112, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "3rd Station Pass Cleared", 113, 113, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "4th Station Pass Cleared", 114, 114, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "5th Station Pass Cleared", 115, 115, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "6th Station Pass Cleared", 116, 116, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "7th Station Pass Cleared", 117, 117, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "8th Station Pass Cleared", 118, 118, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "9th Station Pass Cleared", 119, 119, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "Sky Peak Summit Pass Cleared", 120, 120, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "5th Station Clearing Cleared", 121, 121, ["Late", "Station"]),
    LocationData("LateDungeonComplete", 1, "Sky Peak Summit Cleared", 122, 122, ["Late", "Station"]),
    # Special Episode Dungeons
    LocationData("SpecialDungeonComplete", 3, "SE Deep Star Cave Cleared", 125, 123, ["Special"]),
    LocationData("SpecialDungeonComplete", 2, "SE Star Cave Pit Cleared", 127, 126, ["Special"]),
    LocationData("SpecialDungeonComplete", 1, "SE Murky Forest Cleared", 128, 128, ["Special"]),
    LocationData("SpecialDungeonComplete", 1, "SE Eastern Cave Cleared", 129, 129, ["Special"]),
    LocationData("SpecialDungeonComplete", 3, "SE Fortune Ravine Cleared", 132, 130, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 3, "SE Barren Valley Cleared", 135, 133, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 1, "SE Dark Wasteland Cleared", 136, 136, ["Special"]),
    LocationData("SpecialDungeonComplete", 2, "SE Temporal Tower Cleared", 138, 137, ["Special"]),  # 2 subareas
    LocationData("SpecialDungeonComplete", 2, "SE Dusk Forest Cleared", 140, 139, ["Special"]),  # 2 subareas
    LocationData("SpecialDungeonComplete", 1, "SE Spacial Cliffs Cleared", 141, 141, ["Special"]),
    LocationData("SpecialDungeonComplete", 3, "SE Dark Ice Mountain Cleared", 144, 142, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 1, "SE Icicle Forest Cleared", 145, 145, ["Special"]),
    LocationData("SpecialDungeonComplete", 3, "SE Vast Ice Mountain Cleared", 148, 146, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 1, "SE Southern Jungle Cleared", 149, 149, ["Special"]),
    LocationData("SpecialDungeonComplete", 3, "SE Boulder Quarry Cleared", 152, 150, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 1, "SE Right Cave Path Cleared", 153, 153, ["Special"]),
    LocationData("SpecialDungeonComplete", 1, "SE Left Cave Path Cleared", 154, 154, ["Special"]),
    LocationData("SpecialDungeonComplete", 3, "SE Limestone Cavern Cleared", 157, 155, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", 2, "SE Upper Spring Cave Cleared", 159, 158, ["Special"]),  # 7 subareas
    LocationData("SpecialDungeonComplete", 2, "SE Middle Spring Cave Cleared", 161, 160, ["Special"]),  # 7 subareas
    LocationData("SpecialDungeonComplete", 3, "SE Spring Cave Pit Cleared", 164, 162, ["Special"]),  # 7 subareas
    LocationData("EarlyDungeonComplete", 1, "Star Cave Cleared", 174, 174, ["Mission", "Early"]),
    # Dojo Dungeons
    LocationData("DojoDungeonComplete", 1, "Dojo Normal/Fly Maze Cleared", 180, 180, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Dark/Fire Maze Cleared", 181, 181, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Rock/Water Maze Cleared", 182, 182, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Grass Maze Cleared", 183, 183, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Elec/Steel Maze Cleared", 184, 184, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Ice/Ground Maze Cleared", 185, 185, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Fight/Psych Maze Cleared", 186, 186, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Poison/Bug Maze Cleared", 187, 187, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Dragon Maze Cleared", 188, 188, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", 1, "Dojo Ghost Maze Cleared", 189, 189, ["Dojo"]),  # 7 subareas
    LocationData("RuleDungeonComplete", 1, "Dojo Final Maze Cleared", 191, 191, ["Rule"]),  # 7 subareas
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 1", 900, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 2", 901, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 3", 902, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 4", 903, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 5", 904, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 6", 905, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 7", 906, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 8", 907, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 9", 908, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 10", 909, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 11", 910, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 12", 911, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 13", 912, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 14", 913, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 15", 914, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 16", 915, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 17", 916, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 18", 917, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 19", 918, 0, ["Spinda"]),
    LocationData("SpindaDrinkEvent", 0, "Spinda Drink Event 20", 919, 0, ["Spinda"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 1", 920, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 2", 921, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 3", 922, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 4", 923, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 5", 924, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 6", 925, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 7", 926, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 8", 927, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 9", 928, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 10", 929, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 11", 930, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 12", 931, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 13", 932, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 14", 933, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 15", 934, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 16", 935, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 17", 936, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 18", 937, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 19", 938, 0, ["SpindaDrink"]),
    LocationData("SpindaDrink", 0, "Spinda Drink 20", 939, 0, ["SpindaDrink"]),
    LocationData("Event", 0, "Final Boss", 999, 0),
    # generic checks, right now just bag upgrades
    # LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 1", 300, 0),
    # LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 2", 301, 0),
    # LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 3", 302, 0),
    # LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 4", 303, 0),
    # LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag loc 5", 304, 0),
    # LocationData("SEDungeonUnlock", 0, "Bidoof's Wish Location", 305, 0),
    # LocationData("SEDungeonUnlock", 0, "Igglybuff the Prodigy Location", 306, 0),
    # LocationData("SEDungeonUnlock", 0, 'Today\'s "Oh My Gosh" Location', 307, 0),
    # LocationData("SEDungeonUnlock", 0, "Here Comes Team Charm! Location", 308, 0),
    # LocationData("SEDungeonUnlock", 0, "In the Future of Darkness Location", 309, 0),
    # LocationData("ShopItem", 0, "Shop Item 1", 310, 0),
    # LocationData("ShopItem", 0, "Shop Item 2", 311, 0),
    # LocationData("ShopItem", 0, "Shop Item 3", 312, 0),
    # LocationData("ShopItem", 0, "Shop Item 4", 313, 0),
    # LocationData("ShopItem", 0, "Shop Item 5", 314, 0),
    # LocationData("ShopItem", 0, "Shop Item 6", 315, 0),
    # LocationData("ShopItem", 0, "Shop Item 7", 316, 0),
    # LocationData("ShopItem", 0, "Shop Item 8", 317, 0),
    # LocationData("ShopItem", 0, "Shop Item 9", 318, 0),
    # LocationData("ShopItem", 0, "Shop Item 10", 319, 0),
    # LocationData("SEDungeonUnlock", 0, "Team Name", 427, 0),
    # LocationData("Manaphy", 0, "Manaphy Egg Hatch", 320, 0),
    # LocationData("Manaphy", 0, "Manaphy Fed", 321, 0),
    # LocationData("Manaphy", 0, "Manaphy Healed", 322, 0),
    # LocationData("Manaphy", 0, "Manaphy Join Team", 323, 0),
    # LocationData("Manaphy", 0, "Manaphy Leads To Marine Resort", 324, 0),
    # LocationData("SecretRank", 0, "SecretRank", 347, 0),
    # LocationData("Legendary", 0, "Recruit Uxie", 325, 0),
    # LocationData("Legendary", 0, "Recruit Mesprit", 326, 0),
    # LocationData("Legendary", 0, "Recruit Azelf", 327, 0),
    # LocationData("Legendary", 0, "Recruit Dialga", 328, 0),
    # LocationData("Legendary", 0, "Recruit Phione", 329, 0),
    # LocationData("Legendary", 0, "Recruit Palkia", 330, 0),
    # LocationData("Legendary", 0, "Recruit Kyogre", 332, 0),
    # LocationData("Legendary", 0, "Recruit Groudon", 334, 0),
    # LocationData("Legendary", 0, "Recruit Articuno", 336, 0),
    # LocationData("Legendary", 0, "Recruit Heatran", 338, 0),
    # LocationData("Legendary", 0, "Recruit Giratina", 340, 0),
    # LocationData("Legendary", 0, "Recruit Rayquaza", 342, 0),
    # LocationData("Legendary", 0, "Recruit Mew", 344, 0),
    # LocationData("Legendary", 0, "Recruit Cresselia", 345, 0),
    # LocationData("Legendary", 0, "Recruit Shaymin", 346, 0),
    # LocationData("Instrument", 0, "Get Aqua-Monica", 331, 0),
    # LocationData("Instrument", 0, "Get Terra Cymbal", 333, 0),
    # LocationData("Instrument", 0, "Get Icy Flute", 335, 0),
    # LocationData("Instrument", 0, "Get Fiery Drum", 337, 0),
    # LocationData("Instrument", 0, "Get Rock Horn", 339, 0),
    # LocationData("Instrument", 0, "Get Sky Melodica", 341, 0),
    # LocationData("Instrument", 0, "Get Grass Cornet", 343, 0),
] + subx_location_list


location_Dict_by_id: typing.Dict[int, LocationData] = {location.id: location for location in EOS_location_table}
location_table: Dict[str, LocationData] = {location.name: location for location in EOS_location_table}

location_table.update(subx_location_dict)

location_table_by_groups = get_location_table_by_groups()

location_dict_by_start_id: typing.Dict[int, LocationData] = {
    location.dungeon_start_id: location for location in EOS_location_table
}

mission_location_table = get_mission_location_table()

expanded_EOS_location_table: typing.List[LocationData] = []
expanded_EOS_location_table.extend(EOS_location_table)
# expanded_EOS_location_table.extend(subx_location_list)
expanded_EOS_location_table.extend(mission_location_table)
