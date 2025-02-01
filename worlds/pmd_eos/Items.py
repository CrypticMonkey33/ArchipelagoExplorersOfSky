from typing import NamedTuple, Dict, Set, List

from BaseClasses import ItemClassification, Item

# BASE_OFFSET = 100000000 #Need to figure out what to set this to. The offset for Archipelago to make it unique


class ItemData(NamedTuple):
    name: str
    id: int
    classification: ItemClassification
    start_number: int
    group: list[str]
    memory_offset: int


class EOSItem(Item):
    game: str = "Pokemon Mystery Dungeon Explorers of Sky"


def get_item_table_by_groups() -> Dict[str, set[str]]:
    #groups: Set[str] = set()
    new_dict: Dict[str, set[str]] = {}
    for item_name in item_table:
        if item_table[item_name].group:
            for group in item_table[item_name].group:
                #groups.add(group)
                if group in new_dict:
                    new_dict[group].add(item_name)
                else:
                    test_set = set("")
                    test_set.add(item_name)
                    new_dict.update({group: test_set})

    return new_dict

EOS_item_table = [
    # "Test Dungeon"0, ItemClassification.progression, ["Unique", "Dungeons"],0x0),
    #ItemData("Beach Cave", 1, ItemClassification.progression, 1, ["Unique", "EarlyDungeons"], 0x1),
    ItemData("Drenched Bluff", 3, ItemClassification.progression, 3, ["Unique", "EarlyDungeons"], 0x3),
    ItemData("Mt. Bristle", 4, ItemClassification.progression, 4, ["Unique", "EarlyDungeons"], 0x4),
    ItemData("Waterfall Cave", 6, ItemClassification.progression, 6, ["Unique", "EarlyDungeons"], 0x6),
    ItemData("Apple Woods", 7, ItemClassification.progression, 7, ["Unique", "EarlyDungeons"], 0x7),
    ItemData("Craggy Coast", 8, ItemClassification.progression, 8, ["Unique", "EarlyDungeons"], 0x8),
    ItemData("Side Path", 9, ItemClassification.progression, 9, ["Unique", "EarlyDungeons"], 0x9),
    ItemData("Mt. Horn", 10, ItemClassification.progression, 10, ["Unique", "EarlyDungeons"], 0xA),
    ItemData("Rock Path", 11, ItemClassification.progression, 11, ["Unique", "EarlyDungeons"], 0xB),
    ItemData("Foggy Forest", 12, ItemClassification.progression, 12, ["Unique", "EarlyDungeons"], 0xC),
    ItemData("Forest Path", 13, ItemClassification.progression, 13, ["Unique", "EarlyDungeons"], 0xD),
    ItemData("Steam Cave", 14, ItemClassification.progression, 14, ["Unique", "EarlyDungeons"], 0xE),
    ItemData("Amp Plains", 17, ItemClassification.progression, 17, ["Unique", "EarlyDungeons"], 0X11),
    ItemData("Northern Desert", 20, ItemClassification.progression, 20, ["Unique", "EarlyDungeons"], 0x14),
    ItemData("Quicksand Cave", 21, ItemClassification.progression, 21, ["Unique", "EarlyDungeons"], 0x15),
    ItemData("Crystal Cave", 24, ItemClassification.progression, 24, ["Unique", "EarlyDungeons"], 0x18),
    ItemData("Crystal Crossing", 25, ItemClassification.progression, 25, ["Unique", "EarlyDungeons"], 0x19),
    ItemData("Chasm Cave", 27, ItemClassification.progression, 27, ["Unique", "EarlyDungeons"], 0x1B),
    ItemData("Dark Hill", 28, ItemClassification.progression, 28, ["Unique", "EarlyDungeons"], 0x1C),
    ItemData("Sealed Ruin", 29, ItemClassification.progression, 29, ["Unique", "EarlyDungeons"], 0x1D),
    ItemData("Dusk Forest", 32, ItemClassification.progression, 32, ["Unique", "EarlyDungeons"], 0x20),
    ItemData("Deep Dusk Forest", 33, ItemClassification.progression, 33, ["Unique", "EarlyDungeons"], 0x21),
    ItemData("Treeshroud Forest", 34, ItemClassification.progression, 34, ["Unique", "EarlyDungeons"], 0x22),
    ItemData("Brine Cave", 35, ItemClassification.progression, 35, ["Unique", "EarlyDungeons"], 0x23),
    #ItemData("Hidden Land", 38, ItemClassification.progression, 38, ["Unique", "BossDungeons"], 0x26),
    ItemData("Temporal Tower", 41, ItemClassification.progression, 41, ["Unique", "BossDungeons"], 0x29),
    ItemData("Mystifying Forest", 44, ItemClassification.progression, 44, ["Unique", "LateDungeons"], 0x2C),
    ItemData("Blizzard Island", 46, ItemClassification.progression, 46, ["Unique", "LateDungeons"], 0x2E),
    ItemData("Crevice Cave", 47, ItemClassification.progression, 47, ["Unique", "LateDungeons"], 0x2F),
    ItemData("Surrounded Sea", 50, ItemClassification.progression, 50, ["Unique", "LateDungeons"], 0x32),
    ItemData("Miracle Sea", 51, ItemClassification.progression, 51, ["Unique", "LateDungeons"], 0x33),
    #ItemData("Ice Aegis Cave", 54, ItemClassification.useful, 54, ["Unique", "Dungeons"], 0x36),
    ItemData("Mt. Travail", 62, ItemClassification.progression, 62, ["Unique", "LateDungeons"], 0x3E),
    ItemData("The Nightmare", 63, ItemClassification.progression, 63, ["Unique", "LateDungeons"], 0x3F),
    ItemData("Spacial Rift", 64, ItemClassification.progression, 64, ["Unique", "LateDungeons"], 0x40),
    ItemData("Dark Crater", 67, ItemClassification.progression, 67, ["Unique", "BossDungeons"], 0x43),
    ItemData("Concealed Ruins", 70, ItemClassification.progression, 70, ["Unique", "LateDungeons"], 0x46),
    ItemData("Marine Resort", 72, ItemClassification.progression, 72, ["Unique", "LateDungeons"], 0x48),
    ItemData("Bottomless Sea", 73, ItemClassification.progression, 73, ["Unique", "LateDungeons"], 0x49),
    ItemData("Shimmer Desert", 75, ItemClassification.progression, 75, ["Unique", "LateDungeons"], 0x4B),
    ItemData("Mt. Avalanche", 77, ItemClassification.progression, 77, ["Unique", "LateDungeons"], 0x4D),
    ItemData("Giant Volcano", 79, ItemClassification.progression, 79, ["Unique", "LateDungeons"], 0x4F),
    ItemData("World Abyss", 81, ItemClassification.progression, 81, ["Unique", "LateDungeons"], 0x51),
    ItemData("Sky Stairway", 83, ItemClassification.progression, 83, ["Unique", "LateDungeons"], 0x53),
    ItemData("Mystery Jungle", 85, ItemClassification.progression, 85, ["Unique", "LateDungeons"], 0x55),
    ItemData("Serenity River", 87, ItemClassification.progression, 87, ["Unique", "LateDungeons"], 0x57),
    ItemData("Landslide Cave", 88, ItemClassification.progression, 88, ["Unique", "LateDungeons"], 0x58),
    ItemData("Lush Prairie", 89, ItemClassification.progression, 89, ["Unique", "LateDungeons"], 0x59),
    ItemData("Tiny Meadow", 90, ItemClassification.progression, 90, ["Unique", "LateDungeons"], 0x5A),
    ItemData("Labyrinth Cave", 91, ItemClassification.progression, 91, ["Unique", "LateDungeons"], 0x5B),
    ItemData("Oran Forest", 92, ItemClassification.progression, 92, ["Unique", "LateDungeons"], 0x5C),
    ItemData("Lake Afar", 93, ItemClassification.progression, 93, ["Unique", "LateDungeons"], 0x5D),
    ItemData("Happy Outlook", 94, ItemClassification.progression, 94, ["Unique", "LateDungeons"], 0x5E),
    ItemData("Mt. Mistral", 95, ItemClassification.progression, 95, ["Unique", "LateDungeons"], 0x5F),
    ItemData("Shimmer Hill", 96, ItemClassification.progression, 96, ["Unique", "LateDungeons"], 0x60),
    ItemData("Lost Wilderness", 97, ItemClassification.progression, 97, ["Unique", "LateDungeons"], 0x61),
    ItemData("Midnight Forest", 98, ItemClassification.progression, 98, ["Unique", "LateDungeons"], 0x62),
    ItemData("Zero Isle North", 99, ItemClassification.useful, 99, ["Unique", "RuleDungeons"], 0x63),
    ItemData("Zero Isle East", 100, ItemClassification.useful, 100, ["Unique", "RuleDungeons"], 0x64),
    ItemData("Zero Isle West", 101, ItemClassification.useful, 101, ["Unique", "RuleDungeons"], 0x65),
    ItemData("Zero Isle South", 102, ItemClassification.useful, 102, ["Unique", "RuleDungeons"], 0x66),
    ItemData("Zero Isle Center", 103, ItemClassification.useful, 103, ["Unique", "RuleDungeons"], 0x67),
    ItemData("Destiny Tower", 104, ItemClassification.useful, 104, ["Unique", "RuleDungeons"], 0x68),
    ItemData("Oblivion Forest", 107, ItemClassification.useful, 107, ["Unique", "RuleDungeons"], 0x6B),
    ItemData("Treacherous Waters", 108, ItemClassification.useful, 108, ["Unique", "RuleDungeons"], 0x6C),
    ItemData("Southeastern Islands", 109, ItemClassification.useful, 109, ["Unique", "RuleDungeons"], 0x6D),
    ItemData("Inferno Cave", 110, ItemClassification.useful, 110, ["Unique", "RuleDungeons"], 0x6E),
    ItemData("1st Station Pass", 111, ItemClassification.progression, 111, ["Unique", "LateDungeons"], 0x6F),
    ItemData("Bidoof SE", 123, ItemClassification.progression, 123, ["Unique", "Special Dungeons"], 0x0),
    # ItemData("Star Cave1", 123, ItemClassification.useful, 123, ["Unique", "Special Dungeons"], 0x7B),
    ItemData("IgglyBuff SE", 128, ItemClassification.progression, 128, ["Unique", "Special Dungeons"], 0x1),
    # ItemData("Murky Forest", 128, ItemClassification.useful, 128, ["Unique", "Special Dungeons"], 0x80),
    # ItemData("Eastern Cave", 129, ItemClassification.useful, 129, ["Unique", "Special Dungeons"], 0x81),
    # ItemData("Fortune Ravine", 130, ItemClassification.useful, 130, ["Unique", "Special Dungeons"], 0x82),
    ItemData("Grovyle + Dusknoir SE", 133, ItemClassification.progression, 133, ["Unique", "Special Dungeons"], 0x4),
    # ItemData("Barren Valley", 133, ItemClassification.useful, 133, ["Unique", "Special Dungeons"], 0x85),
    # ItemData("Dark Wasteland", 136, ItemClassification.useful, 136, ["Unique", "Special Dungeons"], 0x88),
    # ItemData("Temporal Tower2", 137, ItemClassification.useful, 137, ["Unique", "Special Dungeons"], 0x89),
    # ItemData("Dusk Forest2", 139, ItemClassification.useful, 139, ["Unique", "Special Dungeons"], 0x8B),
    # ItemData("Spacial Cliffs", 141, ItemClassification.useful, 141, ["Unique", "Special Dungeons"], 0x8D),
    # ItemData("Dark Ice Mountain", 142, ItemClassification.useful, 142, ["Unique", "Special Dungeons"], 0x8E),
    # ItemData("Icicle Forest", 145, ItemClassification.useful, 145, ["Unique", "Special Dungeons"], 0x91),
    # ItemData("Vast Ice Mountain", 146, ItemClassification.useful, 146, ["Unique", "Special Dungeons"], 0x92),
    ItemData("Team Charm SE", 149, ItemClassification.progression, 149, ["Unique", "Special Dungeons"], 0x3),
    # ItemData("Southern Jungle", 149, ItemClassification.useful, 149, ["Unique", "Special Dungeons"], 0x95),
    # ItemData("Boulder Quarry", 150, ItemClassification.useful, 150, ["Unique", "Special Dungeons"], 0x96),
    # ItemData("Right Cave Path", 153, ItemClassification.useful, 153, ["Unique", "Special Dungeons"], 0x99),
    # ItemData("Left Cave Path", 154, ItemClassification.useful, 154, ["Unique", "Special Dungeons"], 0x9A),
    # ItemData("Limestone Cavern", 155, ItemClassification.useful, 155, ["Unique", "Special Dungeons"], 0x9B),
    ItemData("Sunflora SE", 158, ItemClassification.progression, 158, ["Unique", "Special Dungeons"], 0x2),
    # ItemData("Spring Cave", 158, ItemClassification.useful, 158, ["Unique", "Special Dungeons"], 0x9E),
    ItemData("Star Cave2", 174, ItemClassification.progression, 174, ["Unique", "LateDungeons"], 0xAE),
    ItemData("Dojo Normal/Fly Maze", 180, ItemClassification.progression, 180, ["Unique", "Dojo Dungeons"], 0xB4),
    ItemData("Dojo Dark/Fire Maze", 181, ItemClassification.progression, 181, ["Unique", "Dojo Dungeons"], 0xB5),
    ItemData("Dojo Rock/Water Maze", 182, ItemClassification.progression, 182, ["Unique", "Dojo Dungeons"], 0xB6),
    ItemData("Dojo Grass Maze", 183, ItemClassification.progression, 183, ["Unique", "Dojo Dungeons"], 0xB7),
    ItemData("Dojo Elec/Steel Maze", 184, ItemClassification.progression, 184, ["Unique", "Dojo Dungeons"], 0xB8),
    ItemData("Dojo Ice/Ground Maze", 185, ItemClassification.progression, 185, ["Unique", "Dojo Dungeons"], 0xB9),
    ItemData("Dojo Fight/Psych Maze", 186, ItemClassification.progression, 186, ["Unique", "Dojo Dungeons"], 0xBA),
    ItemData("Dojo Poison/Bug Maze", 187, ItemClassification.progression, 187, ["Unique", "Dojo Dungeons"], 0xBB),
    ItemData("Dojo Dragon Maze", 188, ItemClassification.progression, 188, ["Unique", "Dojo Dungeons"], 0xBC),
    ItemData("Dojo Ghost Maze", 189, ItemClassification.progression, 189, ["Unique", "Dojo Dungeons"], 0xBD),
    # ItemData("Dojo Final Maze", 191, ItemClassification.useful, 191, ["Unique", "Dojo Dungeons"], 0xBF),  # 7 subareas
    ItemData("Relic Fragment Shard", 200, ItemClassification.progression, 200, ["Macguffin"], 0x00),
    ItemData("Cresselia Feather", 201, ItemClassification.progression, 201, ["Macguffin"], 0x00),

    ItemData("Victory", 300, ItemClassification.progression, 0, [], 0x00),
    ItemData("Bag Upgrade", 500, ItemClassification.useful, 0, ["ProgressiveBag", "Generic"], 0x00),
    #ItemData("FillerItem", 600, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem2", 601, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem3", 602, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem4", 603, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem5", 604, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem6", 605, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem7", 606, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem8", 607, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem9", 608, ItemClassification.filler, 0, ["Filler"], 0x00),
    #ItemData("FillerItem10", 609, ItemClassification.filler, 0, ["Filler"], 0x00),
    ItemData("Golden Seed", 393, ItemClassification.filler, 0, ["Item"], 0x5D),
    ItemData("Gold Ribbon", 394, ItemClassification.filler, 0, ["Item"], 0x20),
    ItemData("Team Name Trap", 700, ItemClassification.trap, 0, ["Trap"], 0x0),
    ItemData("Confusion Trap", 701, ItemClassification.trap, 0, ["Trap"], 0x0),
    ItemData("Nap Time!", 702, ItemClassification.trap, 0, ["Trap"], 0x0),

]

item_frequencies: Dict[str, int] = {
    "Bag Upgrade": 5
}

item_table: Dict[str, ItemData] = {item.name: item for item in EOS_item_table}
item_table_by_id: Dict[int, ItemData] = {item.id: item for item in EOS_item_table}

item_table_by_groups = get_item_table_by_groups()
