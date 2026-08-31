from typing import ClassVar

from BaseClasses import Location

from .rom_type_definitions import subx_table


class LocationData:
    name: str = ""
    classification: str = ""
    dungeon_length: int = 1
    id: int = -1
    dungeon_start_id: int = -1
    group: ClassVar[list[str]] = [""]

    def __init__(self, classification, name, id, group=None):
        if group is None:
            group = [""]
        self.name = name
        self.classification = classification
        self.id = id
        self.group = group


class EOSLocation(Location):
    game: str = "Pokémon Mystery Dungeon: Explorers of Sky"


def get_location_table_by_groups() -> dict[str, set[str]]:
    # groups: Set[str] = set()
    new_dict: dict[str, set[str]] = {}
    for location_name, location_data in location_table.items():
        if location_data.group:
            for group in location_data.group:
                # groups.add(group)
                if group in new_dict:
                    new_dict[group].add(location_name)
                else:
                    test_set = set("")
                    test_set.add(location_name)
                    new_dict.update({group: test_set})

    return new_dict


def get_subx_table() -> list[LocationData]:
    new_list: list[LocationData] = []
    subx_start_id = 300
    for item in subx_table:
        if item.flag_definition == "Unused" or item.default_item == "ignore":
            continue
        new_location = LocationData(
            classification=item.classification,
            name=item.flag_definition,
            id=subx_start_id + item.bitfield_bit_number,
            group=["SubX"],
        )
        new_list.append(new_location)

    return new_list


def get_mission_location_table() -> list[LocationData]:
    mission_start_id = 1000
    new_list: list[LocationData] = []

    for location in eos_location_table:
        if location.name == "Beach Cave" and "Mission" in location.group:
            for j in range(50):
                location_name: str = f"{location.name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", location_name, location_id, []))
            for j in range(50):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", location_name, location_id, []))

        elif location.classification == "EarlyDungeonComplete" and "Mission" in location.group:
            for j in range(31):
                location_name = f"{location.name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", location_name, location_id, []))

            for j in range(31):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", location_name, location_id, []))

        elif "Mission" in location.group and (
            location.classification == "LateDungeonComplete" or location.classification == "BossDungeonComplete"
        ):
            for j in range(31):
                location_name = f"{location.name} Mission {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j
                new_list.append(LocationData("Mission", location_name, location_id, []))

            for j in range(31):
                location_name = f"{location.name} Outlaw {j + 1}"
                location_id = location.id + mission_start_id + (100 * location.id) + j + 50
                new_list.append(LocationData("Outlaw", location_name, location_id, []))

    return new_list


def get_location_table_by_start_id() -> dict[int, set[str]]:
    # groups: Set[str] = set()
    new_dict: dict[int, set[str]] = {}
    for location_name, location_data in location_table.items():
        if location_data.group:
            for group in location_data.group:
                # groups.add(group)
                if group in new_dict:
                    new_dict[group].add(location_name)
                else:
                    test_set = set("")
                    test_set.add(location_name)
                    new_dict.update({group: test_set})

    return new_dict


subx_location_list = get_subx_table()
subx_location_dict = {location.name: location for location in subx_location_list}

eos_location_table: list[LocationData] = [
    LocationData("EarlyDungeonComplete", "Beach Cave Cleared", 2, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Drenched Bluff Cleared", 3, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Mt. Bristle Cleared", 5, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", "Waterfall Cave Cleared", 6, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Apple Woods Cleared", 7, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Craggy Coast Cleared", 8, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Side Path Cleared", 9, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Mt. Horn Cleared", 10, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Rock Path Cleared", 11, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Foggy Forest Cleared", 12, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Forest Path Cleared", 13, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Steam Cave Cleared", 16, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", "Amp Plains Cleared", 19, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", "Northern Desert Cleared", 20, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Quicksand Cave Cleared", 23, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", "Crystal Cave Cleared", 24, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Crystal Crossing Cleared", 26, ["Mission", "Early"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", "Chasm Cave Cleared", 27, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Dark Hill Cleared", 28, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Sealed Ruin Cleared", 31, ["Mission", "Early"]),  # 3 subareas
    LocationData("EarlyDungeonComplete", "Dusk Forest Cleared", 32, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Deep Dusk Forest Cleared", 33, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Treeshroud Forest Cleared", 34, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Brine Cave Cleared", 37, ["Mission", "Early"]),  # 3 subareas
    LocationData("BossDungeonComplete", "Hidden Land Cleared", 40, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", "Temporal Tower Cleared", 43, ["Mission", "Boss", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", "Mystifying Forest Cleared", 45, ["Mission", "Late"]),  # start of extra levels
    LocationData("LateDungeonComplete", "Blizzard Island Cleared", 46, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Crevice Cave Cleared", 49, ["Mission", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", "Surrounded Sea Cleared", 50, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Miracle Sea Cleared", 52, ["Mission", "Late"]),  # 3 subareas
    LocationData("LateDungeonComplete", "Ice Aegis Cave Cleared", 54, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Regice Chamber Cleared", 55, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Rock Aegis Cave Cleared", 56, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Regirock Chamber Cleared", 57, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Steel Aegis Cave Cleared", 58, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Registeel Chamber Cleared", 59, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Aegis Cave Pit Cleared", 60, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Regigigas Chamber Cleared", 61, ["Late", "Aegis", "Optional"]),
    LocationData("LateDungeonComplete", "Mt. Travail Cleared", 62, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "The Nightmare Cleared", 63,["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Spacial Rift Cleared", 66,["Mission", "Late"]),  # 3 subareas
    LocationData("BossDungeonComplete", "Dark Crater Cleared", 69,["Boss"]),  # 3 subareas
    LocationData("LateDungeonComplete", "Concealed Ruins Cleared", 70, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Marine Resort Cleared", 72, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Bottomless Sea Cleared", 73, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Shimmer Desert Cleared", 75, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Mt. Avalanche Cleared", 77, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Giant Volcano Cleared", 79, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "World Abyss Cleared", 81, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Sky Stairway Cleared", 83, ["Mission", "Late"]),  # 2 subareas
    LocationData("LateDungeonComplete", "Mystery Jungle Cleared", 85, ["Mission", "Late"]),  # 2 subareas
    LocationData("EarlyDungeonComplete", "Serenity River Cleared", 87, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Landslide Cave Cleared", 88, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Lush Prairie Cleared", 89, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Tiny Meadow Cleared", 90, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Labyrinth Cave Cleared", 91, ["Mission", "Early"]),
    LocationData("EarlyDungeonComplete", "Oran Forest Cleared", 92, ["Mission", "Early"]),
    LocationData("LateDungeonComplete", "Lake Afar Cleared", 93, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Happy Outlook Cleared", 94, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Mt. Mistral Cleared", 95, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Shimmer Hill Cleared", 96, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Lost Wilderness Cleared", 97, ["Mission", "Late"]),
    LocationData("LateDungeonComplete", "Midnight Forest Cleared", 98, ["Mission", "Late"]),
    LocationData("RuleDungeonComplete", "Zero Isle North Cleared", 99, ["Rule"]),
    LocationData("RuleDungeonComplete", "Zero Isle East Cleared", 100, ["Rule"]),
    LocationData("RuleDungeonComplete", "Zero Isle West Cleared", 101, ["Rule"]),
    LocationData("RuleDungeonComplete", "Zero Isle South Cleared", 102, ["Rule"]),
    LocationData("RuleDungeonComplete", "Zero Isle Center Cleared", 103, ["Rule"]),
    LocationData("RuleDungeonComplete", "Destiny Tower Cleared", 104, ["Rule"]),
    LocationData("RuleDungeonComplete", "Oblivion Forest Cleared", 107, ["Rule"]),
    LocationData("RuleDungeonComplete", "Treacherous Waters Cleared", 108, ["Rule"]),
    LocationData("RuleDungeonComplete", "Southeastern Islands Cleared", 109, ["Rule"]),
    LocationData("RuleDungeonComplete", "Inferno Cave Cleared", 110, ["Rule"]),
    LocationData("LateDungeonComplete", "1st Station Pass Cleared", 111, ["Mission", "Late", "Station"]),  # 12 subareas
    LocationData("LateDungeonComplete", "2nd Station Pass Cleared", 112, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "3rd Station Pass Cleared", 113, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "4th Station Pass Cleared", 114, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "5th Station Pass Cleared", 115, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "6th Station Pass Cleared", 116, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "7th Station Pass Cleared", 117, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "8th Station Pass Cleared", 118, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "9th Station Pass Cleared", 119, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "Sky Peak Summit Pass Cleared", 120, ["Mission", "Late", "Station"]),
    LocationData("LateDungeonComplete", "5th Station Clearing Cleared", 121, ["Late", "Station"]),
    LocationData("LateDungeonComplete", "Sky Peak Summit Cleared", 122, ["Late", "Station"]),
    # Special Episode Dungeons
    LocationData("SpecialDungeonComplete", "SE Deep Star Cave Cleared", 125, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Star Cave Pit Cleared", 127, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Murky Forest Cleared", 128, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Eastern Cave Cleared", 129, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Fortune Ravine Cleared", 132, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Barren Valley Cleared", 135, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Dark Wasteland Cleared", 136, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Temporal Tower Cleared", 138, ["Special"]),  # 2 subareas
    LocationData("SpecialDungeonComplete", "SE Dusk Forest Cleared", 140, ["Special"]),  # 2 subareas
    LocationData("SpecialDungeonComplete", "SE Spacial Cliffs Cleared", 141, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Dark Ice Mountain Cleared", 144, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Icicle Forest Cleared", 145, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Vast Ice Mountain Cleared", 148, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Southern Jungle Cleared", 149, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Boulder Quarry Cleared", 152, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Right Cave Path Cleared", 153, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Left Cave Path Cleared", 154, ["Special"]),
    LocationData("SpecialDungeonComplete", "SE Limestone Cavern Cleared", 157, ["Special"]),  # 3 subareas
    LocationData("SpecialDungeonComplete", "SE Upper Spring Cave Cleared", 159, ["Special"]),  # 7 subareas
    LocationData("SpecialDungeonComplete", "SE Middle Spring Cave Cleared", 161, ["Special"]),  # 7 subareas
    LocationData("SpecialDungeonComplete", "SE Spring Cave Pit Cleared", 164, ["Special"]),  # 7 subareas
    LocationData("EarlyDungeonComplete", "Star Cave Cleared", 174, ["Mission", "Early"]),
    # Dojo Dungeons
    LocationData("DojoDungeonComplete", "Dojo Normal/Fly Maze Cleared", 180, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Dark/Fire Maze Cleared", 181, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Rock/Water Maze Cleared", 182, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Grass Maze Cleared", 183, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Elec/Steel Maze Cleared", 184, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Ice/Ground Maze Cleared", 185, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Fight/Psych Maze Cleared", 186, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Poison/Bug Maze Cleared", 187, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Dragon Maze Cleared", 188, ["Dojo"]),  # 7 subareas
    LocationData("DojoDungeonComplete", "Dojo Ghost Maze Cleared", 189, ["Dojo"]),  # 7 subareas
    LocationData("RuleDungeonComplete", "Dojo Final Maze Cleared", 191, ["Rule"]),  # 7 subareas
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 1", 900, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 2", 901, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 3", 902, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 4", 903, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 5", 904, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 6", 905, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 7", 906, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 8", 907, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 9", 908, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 10", 909, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 11", 910, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 12", 911, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 13", 912, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 14", 913, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 15", 914, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 16", 915, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 17", 916, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 18", 917, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 19", 918, ["Spinda"]),
    LocationData("SpindaDrinkEvent", "Spinda Drink Event 20", 919, ["Spinda"]),
    LocationData("SpindaDrink", "Spinda Drink 1", 920, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 2", 921, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 3", 922, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 4", 923, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 5", 924, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 6", 925, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 7", 926, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 8", 927, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 9", 928, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 10", 929, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 11", 930, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 12", 931, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 13", 932, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 14", 933, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 15", 934, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 16", 935, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 17", 936, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 18", 937, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 19", 938, ["SpindaDrink"]),
    LocationData("SpindaDrink", "Spinda Drink 20", 939, ["SpindaDrink"]),
    LocationData("Event", "Final Boss", 999,),
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
    *subx_location_list
]


location_dict_by_id: dict[int, LocationData] = {location.id: location for location in eos_location_table}
location_table: dict[str, LocationData] = {location.name: location for location in eos_location_table}

location_table.update(subx_location_dict)

location_table_by_groups = get_location_table_by_groups()

location_dict_by_start_id: dict[int, LocationData] = {
    location.dungeon_start_id: location for location in eos_location_table
}

mission_location_table = get_mission_location_table()

expanded_eos_location_table: list[LocationData] = []
expanded_eos_location_table.extend(eos_location_table)
# expanded_eos_location_table.extend(subx_location_list)
expanded_eos_location_table.extend(mission_location_table)
