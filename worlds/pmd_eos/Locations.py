import typing

from BaseClasses import Location


class LocationData:
    name: str = ""
    classification: str = ""
    dungeon_length: int = 1
    id: int = -1

    def __init__(self,  classification, dungeon_length, name, id):
        self.name = name
        self.classification = classification
        self.dungeon_length = dungeon_length
        self.id = id


class EOSLocation(Location):
    game: str = "Pokemon Mystery Dungeon: Explorers of Sky"


EOS_location_table: typing.List[LocationData] = [
    # "Test Dungeon", 0,  # Should be unused
    LocationData("DungeonUnlock", 1, "Beach Cave", 1),
    LocationData("DungeonUnlock", 1, "Drenched Bluff", 3),
    LocationData("DungeonUnlock", 2, "Mt. Bristle", 4),  # 2 subareas
    LocationData("DungeonUnlock", 1, "Waterfall Cave", 6),
    LocationData("DungeonUnlock", 1, "Apple Woods", 7),
    LocationData("DungeonUnlock", 1, "Craggy Coast", 8),
    LocationData("DungeonUnlock", 1, "Side Path", 9),
    LocationData("DungeonUnlock", 1, "Mt. Horn", 10),
    LocationData("DungeonUnlock", 1, "Rock Path", 11),
    LocationData("DungeonUnlock", 1, "Foggy Forest", 12),
    LocationData("DungeonUnlock", 1, "Forest Path", 13),
    LocationData("DungeonUnlock", 3, "Steam Cave", 14),  # 3 subareas
    LocationData("DungeonUnlock", 3, "Amp Plains", 17),  # 3 subareas
    LocationData("DungeonUnlock", 1, "Northern Desert", 20),
    LocationData("DungeonUnlock", 3, "Quicksand Cave", 21),  # 3 subareas
    LocationData("DungeonUnlock", 1, "Crystal Cave", 24),
    LocationData("DungeonUnlock", 2, "Crystal Crossing", 25),  # 2 subareas
    LocationData("DungeonUnlock", 1, "Chasm Cave", 27),
    LocationData("DungeonUnlock", 1, "Dark Hill", 28),
    LocationData("DungeonUnlock", 3, "Sealed Ruin", 29),  # 3 subareas
    LocationData("DungeonUnlock", 1, "Dusk Forest1", 32),
    LocationData("DungeonUnlock", 1, "Deep Dusk Forest", 33),
    LocationData("DungeonUnlock", 1, "Treeshroud Forest", 34),
    LocationData("DungeonUnlock", 3, "Brine Cave", 35),  # 3 subareas
    LocationData("DungeonUnlock", 3, "Hidden Land", 38),  # 3 subareas
    LocationData("DungeonUnlock", 3, "Temporal Tower1", 41),  # 3 subareas
    LocationData("DungeonUnlock", 2, "Mystifying Forest", 44),  # start of extra levels, 2 subareas
    LocationData("DungeonUnlock", 1, "Blizzard Island", 46),
    LocationData("DungeonUnlock", 3, "Crevice Cave", 47),  # 3 subareas
    LocationData("DungeonUnlock", 1, "Surrounded Sea", 50),
    LocationData("DungeonUnlock", 3, "Miracle Sea", 51),  # 3 subareas
    LocationData("DungeonUnlock", 8, "Ice Aegis Cave", 54),  # 8 subareas
    LocationData("DungeonUnlock", 1, "Mt. Travail", 62),
    LocationData("DungeonUnlock", 1, "The Nightmare", 63),
    LocationData("DungeonUnlock", 3, "Spacial Rift", 64),  # 3 subareas
    LocationData("DungeonUnlock", 3, "Dark Crater", 67),  # 3 subareas
    LocationData("DungeonUnlock", 2, "Concealed Ruins", 70),  # 2 subareas
    LocationData("DungeonUnlock", 1, "Marine Resort", 72),
    LocationData("DungeonUnlock", 2, "Bottomless Sea", 73),  # 2 subareas
    LocationData("DungeonUnlock", 2, "Shimmer Desert", 75),  # 2 subareas
    LocationData("DungeonUnlock", 2, "Mt. Avalanche", 77),  # 2 subareas
    LocationData("DungeonUnlock", 2, "Giant Volcano", 79),  # 2 subareas
    LocationData("DungeonUnlock", 2, "World Abyss", 81),  # 2 subareas
    LocationData("DungeonUnlock", 2, "Sky Stairway", 83),  # 2 subareas
    LocationData("DungeonUnlock", 2, "Mystery Jungle", 85),  # 2 subareas
    LocationData("DungeonUnlock", 1, "Serenity River", 87),
    LocationData("DungeonUnlock", 1, "Landslide Cave", 88),
    LocationData("DungeonUnlock", 1, "Lush Prairie", 89),
    LocationData("DungeonUnlock", 1, "Tiny Meadow", 90),
    LocationData("DungeonUnlock", 1, "Labyrinth Cave", 91),
    LocationData("DungeonUnlock", 1, "Oran Forest", 92),
    LocationData("DungeonUnlock", 1, "Lake Afar", 93),
    LocationData("DungeonUnlock", 1, "Happy Outlook", 94),
    LocationData("DungeonUnlock", 1, "Mt. Mistral", 95),
    LocationData("DungeonUnlock", 1, "Shimmer Hill", 96),
    LocationData("DungeonUnlock", 1, "Lost Wilderness", 97),
    LocationData("DungeonUnlock", 1, "Midnight Forest", 98),
    LocationData("DungeonUnlock", 1, "Zero Isle North", 99),
    LocationData("DungeonUnlock", 1, "Zero Isle East", 100),
    LocationData("DungeonUnlock", 1, "Zero Isle West", 101),
    LocationData("DungeonUnlock", 1, "Zero Isle South", 102),
    LocationData("DungeonUnlock", 1, "Zero Isle Center", 103),
    LocationData("DungeonUnlock", 1, "Destiny Tower", 104),
    LocationData("DungeonUnlock", 1, "Oblivion Forest", 107),
    LocationData("DungeonUnlock", 1, "Treacherous Waters", 108),
    LocationData("DungeonUnlock", 1, "Southeastern Islands", 109),
    LocationData("DungeonUnlock", 1, "Inferno Cave", 110),
    LocationData("DungeonUnlock", 12, "1st Station Pass", 111),  # 12 subareas
    # Special Episode Dungeons
    LocationData("SpecialDungeonUnlock", 1, "Murky Forest", 128),
    LocationData("SpecialDungeonUnlock", 1, "Eastern Cave", 129),
    LocationData("SpecialDungeonUnlock", 3, "Fortune Ravine", 130),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 3, "Barren Valley", 133),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 1, "Dark Wasteland", 136),
    LocationData("SpecialDungeonUnlock", 2, "Temporal Tower2", 137),  # 2 subareas
    LocationData("SpecialDungeonUnlock", 2, "Dusk Forest2", 139),  # 2 subareas
    LocationData("SpecialDungeonUnlock", 1, "Spacial Cliffs", 141),
    LocationData("SpecialDungeonUnlock", 3, "Dark Ice Mountain", 142),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 1, "Icicle Forest", 145),
    LocationData("SpecialDungeonUnlock", 3, "Vast Ice Mountain", 146),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 1, "Southern Jungle", 149),
    LocationData("SpecialDungeonUnlock", 3, "Boulder Quarry", 150),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 1, "Right Cave Path", 153),
    LocationData("SpecialDungeonUnlock", 1, "Left Cave Path", 154),
    LocationData("SpecialDungeonUnlock", 3, "Limestone Cavern", 155),  # 3 subareas
    LocationData("SpecialDungeonUnlock", 7, "Spring Cave", 158),  # 7 subareas
    LocationData("DungeonUnlock", 1,"Star Cave", 174),
    LocationData("Event", 0, "Final Boss", 163)
    # "Shaymin Village", 175,
    # "Armaldo's Shelter", 176,
    # "Luminous Spring", 177,
    # "Hot Spring", 178,
    # "Rescue", 179
]