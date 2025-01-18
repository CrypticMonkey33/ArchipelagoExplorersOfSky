import typing

from BaseClasses import ItemClassification, Item

# BASE_OFFSET = 100000000 #Need to figure out what to set this to. The offset for Archipelago to make it unique


class ItemData(typing.NamedTuple):
    name: str
    id: int
    classification: ItemClassification
    group: list[str]
    memory_offset: int


class EOSItem(Item):
    game: str = "Pokemon Mystery Dungeon: Explorers of Sky"


EOS_item_table = [
    # "Test Dungeon"0, ItemClassification.progression, ["Unique", "Dungeons"],0x0),
    ItemData("Beach Cave", 1, ItemClassification.progression, ["Unique", "Dungeons"],0x1),
    ItemData("Drenched Bluff", 3, ItemClassification.progression, ["Unique", "Dungeons"],0x2),
    ItemData("Mt. Bristle", 4, ItemClassification.progression, ["Unique", "Dungeons"],0x3),
    ItemData("Waterfall Cave", 6, ItemClassification.progression, ["Unique", "Dungeons"],0x4),
    ItemData("Apple Woods", 7, ItemClassification.progression, ["Unique", "Dungeons"], 0x5),
    ItemData("Craggy Coast", 8, ItemClassification.progression, ["Unique", "Dungeons"],0x6),
    ItemData("Side Path", 9, ItemClassification.progression, ["Unique", "Dungeons"],0x7),
    ItemData("Mt. Horn", 10, ItemClassification.progression, ["Unique", "Dungeons"],0x8),
    ItemData("Rock Path", 11, ItemClassification.progression, ["Unique", "Dungeons"],0x9),
    ItemData("Foggy Forest", 12, ItemClassification.progression, ["Unique", "Dungeons"],0xA),
    ItemData("Forest Path", 13, ItemClassification.progression, ["Unique", "Dungeons"],0xB),
    ItemData("Steam Cave", 14, ItemClassification.progression, ["Unique", "Dungeons"],0xC),
    ItemData("Amp Plains", 17, ItemClassification.progression, ["Unique", "Dungeons"],0XD),
    ItemData("Northern Desert", 20, ItemClassification.progression, ["Unique", "Dungeons"],0xE),
    ItemData("Quicksand Cave", 21, ItemClassification.progression, ["Unique", "Dungeons"],0xF),
    ItemData("Crystal Cave", 24, ItemClassification.progression, ["Unique", "Dungeons"],0x10),
    ItemData("Crystal Crossing", 25, ItemClassification.progression, ["Unique", "Dungeons"],0x11),
    ItemData("Chasm Cave", 27, ItemClassification.progression, ["Unique", "Dungeons"],0x12),
    ItemData("Dark Hill", 28, ItemClassification.progression, ["Unique", "Dungeons"],0x13),
    ItemData("Sealed Ruin", 29, ItemClassification.progression, ["Unique", "Dungeons"],0x14),
    ItemData("Dusk Forest1", 32, ItemClassification.progression, ["Unique", "Dungeons"],0x15),
    ItemData("Deep Dusk Forest", 33, ItemClassification.progression, ["Unique", "Dungeons"],0x16),
    ItemData("Treeshroud Forest", 34, ItemClassification.progression, ["Unique", "Dungeons"],0x17),
    ItemData("Brine Cave", 35, ItemClassification.progression, ["Unique", "Dungeons"],0x18),
    ItemData("Hidden Land", 38, ItemClassification.progression, ["Unique", "Dungeons"],0x19),
    ItemData("Temporal Tower1", 41, ItemClassification.progression, ["Unique", "Dungeons"],0x1A),
    ItemData("Mystifying Forest", 44, ItemClassification.useful, ["Unique", "Dungeons"],0x1B),
    ItemData("Blizzard Island", 46, ItemClassification.useful, ["Unique", "Dungeons"],0x1C),
    ItemData("Crevice Cave", 47, ItemClassification.useful, ["Unique", "Dungeons"],0x1D),
    ItemData("Surrounded Sea", 50, ItemClassification.useful, ["Unique", "Dungeons"],0x1E),
    ItemData("Miracle Sea", 51, ItemClassification.useful, ["Unique", "Dungeons"],0x1F),
    ItemData("Ice Aegis Cave", 54, ItemClassification.useful, ["Unique", "Dungeons"],0x20),
    ItemData("Mt. Travail", 62, ItemClassification.useful, ["Unique", "Dungeons"],0x21),
    ItemData("The Nightmare", 63, ItemClassification.useful, ["Unique", "Dungeons"],0x22),
    ItemData("Spacial Rift", 64, ItemClassification.useful, ["Unique", "Dungeons"],0x23),
    ItemData("Dark Crater", 67, ItemClassification.useful, ["Unique", "Dungeons"],0x24),
    ItemData("Concealed Ruins", 70, ItemClassification.useful, ["Unique", "Dungeons"],0x25),
    ItemData("Marine Resort", 72, ItemClassification.useful, ["Unique", "Dungeons"],0x26),
    ItemData("Bottomless Sea", 73, ItemClassification.useful, ["Unique", "Dungeons"],0x27),
    ItemData("Shimmer Desert", 75, ItemClassification.useful, ["Unique", "Dungeons"],0x28),
    ItemData("Mt. Avalanche", 77, ItemClassification.useful, ["Unique", "Dungeons"],0x29),
    ItemData("Giant Volcano", 79, ItemClassification.useful, ["Unique", "Dungeons"],0x2A),
    ItemData("World Abyss", 81, ItemClassification.useful, ["Unique", "Dungeons"],0x2B),
    ItemData("Sky Stairway", 83, ItemClassification.useful, ["Unique", "Dungeons"],0x2C),
    ItemData("Mystery Jungle", 85, ItemClassification.useful, ["Unique", "Dungeons"],0x2D),
    ItemData("Serenity River", 87, ItemClassification.useful, ["Unique", "Dungeons"],0x2E),
    ItemData("Landslide Cave", 88, ItemClassification.useful, ["Unique", "Dungeons"],0x2F),
    ItemData("Lush Prairie", 89, ItemClassification.useful, ["Unique", "Dungeons"],0x30),
    ItemData("Tiny Meadow", 90, ItemClassification.useful, ["Unique", "Dungeons"],0x31),
    ItemData("Labyrinth Cave", 91, ItemClassification.useful, ["Unique", "Dungeons"],0x32),
    ItemData("Oran Forest", 92, ItemClassification.useful, ["Unique", "Dungeons"],0x33),
    ItemData("Lake Afar", 93, ItemClassification.useful, ["Unique", "Dungeons"],0x34),
    ItemData("Happy Outlook", 94, ItemClassification.useful, ["Unique", "Dungeons"],0x35),
    ItemData("Mt. Mistral", 95, ItemClassification.useful, ["Unique", "Dungeons"],0x36),
    ItemData("Shimmer Hill", 96, ItemClassification.useful, ["Unique", "Dungeons"],0x37),
    ItemData("Lost Wilderness", 97, ItemClassification.useful, ["Unique", "Dungeons"],0x38),
    ItemData("Midnight Forest", 98, ItemClassification.useful, ["Unique", "Dungeons"],0x39),
    ItemData("Zero Isle North", 99, ItemClassification.useful, ["Unique", "Dungeons"],0x3A),
    ItemData("Zero Isle East", 100, ItemClassification.useful, ["Unique", "Dungeons"],0x3B),
    ItemData("Zero Isle West", 101, ItemClassification.useful, ["Unique", "Dungeons"],0x3C),
    ItemData("Zero Isle South", 102, ItemClassification.useful, ["Unique", "Dungeons"],0x3D),
    ItemData("Zero Isle Center", 103, ItemClassification.useful, ["Unique", "Dungeons"],0x3E),
    ItemData("Destiny Tower", 104, ItemClassification.useful, ["Unique", "Dungeons"],0x3F),
    ItemData("Oblivion Forest", 107, ItemClassification.useful, ["Unique", "Dungeons"],0x42),
    ItemData("Treacherous Waters", 108, ItemClassification.useful, ["Unique", "Dungeons"],0x43),
    ItemData("Southeastern Islands", 109, ItemClassification.useful, ["Unique", "Dungeons"],0x44),
    ItemData("Inferno Cave", 110, ItemClassification.useful, ["Unique", "Dungeons"],0x45),
    ItemData("1st Station Pass", 111, ItemClassification.useful, ["Unique", "Dungeons"],0x46),
    ItemData("Murky Forest", 128, ItemClassification.useful, ["Unique", "Special Dungeons"],0x48),
    ItemData("Eastern Cave", 129, ItemClassification.useful, ["Unique", "Special Dungeons"],0x49),
    ItemData("Fortune Ravine", 130, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4A),
    ItemData("Barren Valley", 133, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4B),
    ItemData("Dark Wasteland", 136, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4C),
    ItemData("Temporal Tower2", 137, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4D),
    ItemData("Dusk Forest2", 139, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4E),
    ItemData("Spacial Cliffs", 141, ItemClassification.useful, ["Unique", "Special Dungeons"],0x4F),
    ItemData("Dark Ice Mountain", 142, ItemClassification.useful, ["Unique", "Special Dungeons"],0x50),
    ItemData("Icicle Forest", 145, ItemClassification.useful, ["Unique", "Special Dungeons"],0x51),
    ItemData("Vast Ice Mountain", 146, ItemClassification.useful, ["Unique", "Special Dungeons"],0x52),
    ItemData("Southern Jungle", 149, ItemClassification.useful, ["Unique", "Special Dungeons"],0x53),
    ItemData("Boulder Quarry", 150, ItemClassification.useful, ["Unique", "Special Dungeons"],0x54),
    ItemData("Right Cave Path", 153, ItemClassification.useful, ["Unique", "Special Dungeons"],0x55),
    ItemData("Left Cave Path", 154, ItemClassification.useful, ["Unique", "Special Dungeons"],0x56),
    ItemData("Limestone Cavern", 155, ItemClassification.useful, ["Unique", "Special Dungeons"],0x57),
    ItemData("Spring Cave", 158, ItemClassification.useful, ["Unique", "Special Dungeons"],0x58),
    ItemData("Star Cave2", 174, ItemClassification.useful, ["Unique", "Dungeons"],0x61),
    ItemData("Victory", 163, ItemClassification.progression, [], 0x00)
]

item_table: typing.Dict[str, ItemData] = {item.name: item for item in EOS_item_table}