import typing

from BaseClasses import ItemClassification, Item

# BASE_OFFSET = 100000000 #Need to figure out what to set this to. The offset for Archipelago to make it unique


class ItemData(typing.NamedTuple):
    name: str
    id: int
    classification: ItemClassification
    start_number: int
    group: list[str]
    memory_offset: int


class EOSItem(Item):
    game: str = "Pokemon Mystery Dungeon Explorers of Sky"


EOS_item_table = [
    # "Test Dungeon"0, ItemClassification.progression, ["Unique", "Dungeons"],0x0),
    ItemData("Beach Cave", 1, ItemClassification.progression, 1, ["Unique", "Dungeons"], 0x1),
    ItemData("Drenched Bluff", 3, ItemClassification.progression, 3, ["Unique", "Dungeons"], 0x3),
    ItemData("Mt. Bristle", 4, ItemClassification.progression, 4, ["Unique", "Dungeons"], 0x4),
    ItemData("Waterfall Cave", 6, ItemClassification.progression, 6, ["Unique", "Dungeons"], 0x6),
    ItemData("Apple Woods", 7, ItemClassification.progression, 7, ["Unique", "Dungeons"], 0x7),
    ItemData("Craggy Coast", 8, ItemClassification.progression, 8, ["Unique", "Dungeons"], 0x8),
    ItemData("Side Path", 9, ItemClassification.progression, 9, ["Unique", "Dungeons"], 0x9),
    ItemData("Mt. Horn", 10, ItemClassification.progression, 10, ["Unique", "Dungeons"], 0xA),
    ItemData("Rock Path", 11, ItemClassification.progression, 11, ["Unique", "Dungeons"], 0xB),
    ItemData("Foggy Forest", 12, ItemClassification.progression, 12, ["Unique", "Dungeons"], 0xC),
    ItemData("Forest Path", 13, ItemClassification.progression, 13, ["Unique", "Dungeons"], 0xD),
    ItemData("Steam Cave", 14, ItemClassification.progression, 14, ["Unique", "Dungeons"], 0xE),
    ItemData("Amp Plains", 17, ItemClassification.progression, 17, ["Unique", "Dungeons"], 0X11),
    ItemData("Northern Desert", 20, ItemClassification.progression, 20, ["Unique", "Dungeons"], 0x14),
    ItemData("Quicksand Cave", 21, ItemClassification.progression, 21, ["Unique", "Dungeons"], 0x16),
    ItemData("Crystal Cave", 24, ItemClassification.progression, 24, ["Unique", "Dungeons"], 0x18),
    ItemData("Crystal Crossing", 25, ItemClassification.progression, 25, ["Unique", "Dungeons"], 0x19),
    ItemData("Chasm Cave", 27, ItemClassification.progression, 27, ["Unique", "Dungeons"], 0x1B),
    ItemData("Dark Hill", 28, ItemClassification.progression, 28, ["Unique", "Dungeons"], 0x1C),
    ItemData("Sealed Ruin", 29, ItemClassification.progression, 29, ["Unique", "Dungeons"], 0x1D),
    ItemData("Dusk Forest1", 32, ItemClassification.progression, 32, ["Unique", "Dungeons"], 0x20),
    ItemData("Deep Dusk Forest", 33, ItemClassification.progression, 33, ["Unique", "Dungeons"], 0x21),
    ItemData("Treeshroud Forest", 34, ItemClassification.progression, 34, ["Unique", "Dungeons"], 0x22),
    ItemData("Brine Cave", 35, ItemClassification.progression, 35, ["Unique", "Dungeons"], 0x23),
    ItemData("Hidden Land", 38, ItemClassification.progression, 38, ["Unique", "Dungeons"], 0x26),
    ItemData("Temporal Tower1", 41, ItemClassification.progression, 41, ["Unique", "Dungeons"], 0x29),
    ItemData("Mystifying Forest", 44, ItemClassification.useful, 44, ["Unique", "Dungeons"], 0x2C),
    ItemData("Blizzard Island", 46, ItemClassification.useful, 46, ["Unique", "Dungeons"], 0x2E),
    ItemData("Crevice Cave", 47, ItemClassification.useful, 47, ["Unique", "Dungeons"], 0x2F),
    ItemData("Surrounded Sea", 50, ItemClassification.useful, 50, ["Unique", "Dungeons"], 0x32),
    ItemData("Miracle Sea", 51, ItemClassification.useful, 51, ["Unique", "Dungeons"], 0x33),
    ItemData("Ice Aegis Cave", 54, ItemClassification.useful, 54, ["Unique", "Dungeons"], 0x36),
    ItemData("Mt. Travail", 62, ItemClassification.useful, 62, ["Unique", "Dungeons"], 0x3E),
    ItemData("The Nightmare", 63, ItemClassification.useful, 63, ["Unique", "Dungeons"], 0x3F),
    ItemData("Spacial Rift", 64, ItemClassification.useful, 64, ["Unique", "Dungeons"], 0x40),
    ItemData("Dark Crater", 67, ItemClassification.useful, 67, ["Unique", "Dungeons"], 0x43),
    ItemData("Concealed Ruins", 70, ItemClassification.useful, 70, ["Unique", "Dungeons"], 0x46),
    ItemData("Marine Resort", 72, ItemClassification.useful, 72, ["Unique", "Dungeons"], 0x48),
    ItemData("Bottomless Sea", 73, ItemClassification.useful, 73, ["Unique", "Dungeons"], 0x49),
    ItemData("Shimmer Desert", 75, ItemClassification.useful, 75, ["Unique", "Dungeons"], 0x4B),
    ItemData("Mt. Avalanche", 77, ItemClassification.useful, 77, ["Unique", "Dungeons"], 0x4D),
    ItemData("Giant Volcano", 79, ItemClassification.useful, 79, ["Unique", "Dungeons"], 0x4F),
    ItemData("World Abyss", 81, ItemClassification.useful, 81, ["Unique", "Dungeons"], 0x51),
    ItemData("Sky Stairway", 83, ItemClassification.useful, 83, ["Unique", "Dungeons"], 0x53),
    ItemData("Mystery Jungle", 85, ItemClassification.useful, 85, ["Unique", "Dungeons"], 0x55),
    ItemData("Serenity River", 87, ItemClassification.useful, 87, ["Unique", "Dungeons"], 0x57),
    ItemData("Landslide Cave", 88, ItemClassification.useful, 88, ["Unique", "Dungeons"], 0x58),
    ItemData("Lush Prairie", 89, ItemClassification.useful, 89, ["Unique", "Dungeons"], 0x59),
    ItemData("Tiny Meadow", 90, ItemClassification.useful, 90, ["Unique", "Dungeons"], 0x5A),
    ItemData("Labyrinth Cave", 91, ItemClassification.useful, 91, ["Unique", "Dungeons"], 0x5B),
    ItemData("Oran Forest", 92, ItemClassification.useful, 92, ["Unique", "Dungeons"], 0x5C),
    ItemData("Lake Afar", 93, ItemClassification.useful, 93, ["Unique", "Dungeons"], 0x5D),
    ItemData("Happy Outlook", 94, ItemClassification.useful, 94, ["Unique", "Dungeons"], 0x5E),
    ItemData("Mt. Mistral", 95, ItemClassification.useful, 95, ["Unique", "Dungeons"], 0x5F),
    ItemData("Shimmer Hill", 96, ItemClassification.useful, 96, ["Unique", "Dungeons"], 0x60),
    ItemData("Lost Wilderness", 97, ItemClassification.useful, 97, ["Unique", "Dungeons"], 0x61),
    ItemData("Midnight Forest", 98, ItemClassification.useful, 98, ["Unique", "Dungeons"], 0x62),
    ItemData("Zero Isle North", 99, ItemClassification.useful, 99, ["Unique", "Dungeons"], 0x63),
    ItemData("Zero Isle East", 100, ItemClassification.useful, 100, ["Unique", "Dungeons"], 0x64),
    ItemData("Zero Isle West", 101, ItemClassification.useful, 101, ["Unique", "Dungeons"], 0x65),
    ItemData("Zero Isle South", 102, ItemClassification.useful, 102, ["Unique", "Dungeons"], 0x66),
    ItemData("Zero Isle Center", 103, ItemClassification.useful, 103, ["Unique", "Dungeons"], 0x67),
    ItemData("Destiny Tower", 104, ItemClassification.useful, 104, ["Unique", "Dungeons"], 0x68),
    ItemData("Oblivion Forest", 107, ItemClassification.useful, 107, ["Unique", "Dungeons"], 0x6B),
    ItemData("Treacherous Waters", 108, ItemClassification.useful, 108, ["Unique", "Dungeons"], 0x6C),
    ItemData("Southeastern Islands", 109, ItemClassification.useful, 109, ["Unique", "Dungeons"], 0x6D),
    ItemData("Inferno Cave", 110, ItemClassification.useful, 110, ["Unique", "Dungeons"], 0x6E),
    ItemData("1st Station Pass", 111, ItemClassification.useful, 111, ["Unique", "Dungeons"], 0x6F),
    # ItemData("Star Cave1", 123, ItemClassification.useful, 123, ["Unique", "Special Dungeons"], 0x7B),
    # ItemData("Murky Forest", 128, ItemClassification.useful, 128, ["Unique", "Special Dungeons"], 0x80),
    # ItemData("Eastern Cave", 129, ItemClassification.useful, 129, ["Unique", "Special Dungeons"], 0x81),
    # ItemData("Fortune Ravine", 130, ItemClassification.useful, 130, ["Unique", "Special Dungeons"], 0x82),
    # ItemData("Barren Valley", 133, ItemClassification.useful, 133, ["Unique", "Special Dungeons"], 0x85),
    # ItemData("Dark Wasteland", 136, ItemClassification.useful, 136, ["Unique", "Special Dungeons"], 0x88),
    # ItemData("Temporal Tower2", 137, ItemClassification.useful, 137, ["Unique", "Special Dungeons"], 0x89),
    # ItemData("Dusk Forest2", 139, ItemClassification.useful, 139, ["Unique", "Special Dungeons"], 0x8B),
    # ItemData("Spacial Cliffs", 141, ItemClassification.useful, 141, ["Unique", "Special Dungeons"], 0x8D),
    # ItemData("Dark Ice Mountain", 142, ItemClassification.useful, 142, ["Unique", "Special Dungeons"], 0x8E),
    # ItemData("Icicle Forest", 145, ItemClassification.useful, 145, ["Unique", "Special Dungeons"], 0x91),
    # ItemData("Vast Ice Mountain", 146, ItemClassification.useful, 146, ["Unique", "Special Dungeons"], 0x92),
    # ItemData("Southern Jungle", 149, ItemClassification.useful, 149, ["Unique", "Special Dungeons"], 0x95),
    # ItemData("Boulder Quarry", 150, ItemClassification.useful, 150, ["Unique", "Special Dungeons"], 0x96),
    # ItemData("Right Cave Path", 153, ItemClassification.useful, 153, ["Unique", "Special Dungeons"], 0x99),
    # ItemData("Left Cave Path", 154, ItemClassification.useful, 154, ["Unique", "Special Dungeons"], 0x9A),
    # ItemData("Limestone Cavern", 155, ItemClassification.useful, 155, ["Unique", "Special Dungeons"], 0x9B),
    # ItemData("Spring Cave", 158, ItemClassification.useful, 158, ["Unique", "Special Dungeons"], 0x9E),
    ItemData("Star Cave2", 174, ItemClassification.useful, 174, ["Unique", "Dungeons"], 0xAE),
    ItemData("Victory", 300, ItemClassification.progression, 0, [], 0x00)
]

item_table: typing.Dict[str, ItemData] = {item.name: item for item in EOS_item_table}
item_table_by_id: typing.Dict[int, ItemData] = {item.id: item for item in EOS_item_table}