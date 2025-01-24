import typing

import typing_extensions

from BaseClasses import Location


class LocationData:
    name: str = ""
    classification: str = ""
    dungeon_length: int = 1
    id: int = -1
    dungeon_start_id: int = -1

    def __init__(self,  classification, dungeon_length, name, id, dungeon_start_id):
        self.name = name
        self.classification = classification
        self.dungeon_length = dungeon_length
        self.id = id
        self.dungeon_start_id = dungeon_start_id


class EOSLocation(Location):
    game: str = "Pokemon Mystery Dungeon Explorers of Sky"


# lowered locations by 1 to ignore bosses
EOS_location_table: typing.List[LocationData] = [
    # "Test Dungeon", 0,  # Should be unused
    LocationData("DungeonUnlock", 2,  "Beach Cave", 1,  1),
    LocationData("DungeonUnlock", 1,  "Drenched Bluff", 3,  3),
    LocationData("DungeonUnlock", 2,  "Mt. Bristle", 4,  4),   # 2 subareas
    LocationData("DungeonUnlock", 1,  "Waterfall Cave", 6,  6),
    LocationData("DungeonUnlock", 1,  "Apple Woods", 7,  7),
    LocationData("DungeonUnlock", 1,  "Craggy Coast", 8,  8),
    LocationData("DungeonUnlock", 1,  "Side Path", 9,  9),
    LocationData("DungeonUnlock", 1,  "Mt. Horn", 10,  10),
    LocationData("DungeonUnlock", 1,  "Rock Path", 11,  11),
    LocationData("DungeonUnlock", 1,  "Foggy Forest", 12,  12),
    LocationData("DungeonUnlock", 1,  "Forest Path", 13,  13),
    LocationData("DungeonUnlock", 3,  "Steam Cave", 15,  14),   # 3 subareas
    LocationData("DungeonUnlock", 3,  "Amp Plains", 18,  17),   # 3 subareas
    LocationData("DungeonUnlock", 1,  "Northern Desert", 20,  20),
    LocationData("DungeonUnlock", 3,  "Quicksand Cave", 22,  21),   # 3 subareas
    LocationData("DungeonUnlock", 1,  "Crystal Cave", 24,  24),
    LocationData("DungeonUnlock", 2,  "Crystal Crossing", 25,  25),   # 2 subareas
    LocationData("DungeonUnlock", 1,  "Chasm Cave", 27,  27),
    LocationData("DungeonUnlock", 1,  "Dark Hill", 28,  28),
    LocationData("DungeonUnlock", 3,  "Sealed Ruin", 30,  29),   # 3 subareas
    LocationData("DungeonUnlock", 1,  "Dusk Forest1", 32,  32),
    LocationData("DungeonUnlock", 1,  "Deep Dusk Forest", 33,  33),
    LocationData("DungeonUnlock", 1,  "Treeshroud Forest", 34,  34),
    LocationData("DungeonUnlock", 3,  "Brine Cave", 36,  35),   # 3 subareas
    LocationData("DungeonUnlock", 3,  "Hidden Land", 39,  38),   # 3 subareas
    LocationData("DungeonUnlock", 3,  "Temporal Tower1", 42,  41),   # 3 subareas
    LocationData("DungeonUnlock", 2,  "Mystifying Forest", 44,  44),   # start of extra levels
    LocationData("DungeonUnlock", 1,  "Blizzard Island", 46,  46),
    LocationData("DungeonUnlock", 3,  "Crevice Cave", 48,  47),   # 3 subareas
    LocationData("DungeonUnlock", 1,  "Surrounded Sea", 50,  50),
    LocationData("DungeonUnlock", 3,  "Miracle Sea", 52,  51),   # 3 subareas
    #LocationData("DungeonUnlock", 8,  "Ice Aegis Cave", 60,  54),   # 8 subareas             we hate aegis cave. also it's kinda broken rn so we're gonna remove it for now
    LocationData("DungeonUnlock", 1,  "Mt. Travail", 62,  62),
    LocationData("DungeonUnlock", 1,  "The Nightmare", 63,  63),
    LocationData("DungeonUnlock", 3,  "Spacial Rift", 65,  64),   # 3 subareas
    LocationData("DungeonUnlock", 3,  "Dark Crater", 68,  67),   # 3 subareas
    LocationData("DungeonUnlock", 2,  "Concealed Ruins", 70,  70),   # 2 subareas
    LocationData("DungeonUnlock", 1,  "Marine Resort", 72,  72),
    LocationData("DungeonUnlock", 2,  "Bottomless Sea", 73,  73),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "Shimmer Desert", 75,  75),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "Mt. Avalanche", 77,  77),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "Giant Volcano", 79,  79),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "World Abyss", 81,  81),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "Sky Stairway", 83,  83),   # 2 subareas
    LocationData("DungeonUnlock", 2,  "Mystery Jungle", 85,  85),   # 2 subareas
    LocationData("DungeonUnlock", 1,  "Serenity River", 87,  87),
    LocationData("DungeonUnlock", 1,  "Landslide Cave", 88,  88),
    LocationData("DungeonUnlock", 1,  "Lush Prairie", 89,  89),
    LocationData("DungeonUnlock", 1,  "Tiny Meadow", 90,  90),
    LocationData("DungeonUnlock", 1,  "Labyrinth Cave", 91,  91),
    LocationData("DungeonUnlock", 1,  "Oran Forest", 92,  92),
    LocationData("DungeonUnlock", 1,  "Lake Afar", 93,  93),
    LocationData("DungeonUnlock", 1,  "Happy Outlook", 94,  94),
    LocationData("DungeonUnlock", 1,  "Mt. Mistral", 95,  95),
    LocationData("DungeonUnlock", 1,  "Shimmer Hill", 96,  96),
    LocationData("DungeonUnlock", 1,  "Lost Wilderness", 97,  97),
    LocationData("DungeonUnlock", 1,  "Midnight Forest", 98,  98),
    LocationData("DungeonUnlock", 1,  "Zero Isle North", 99,  99),
    LocationData("DungeonUnlock", 1,  "Zero Isle East", 100,  100),
    LocationData("DungeonUnlock", 1,  "Zero Isle West", 101,  101),
    LocationData("DungeonUnlock", 1,  "Zero Isle South", 102,  102),
    LocationData("DungeonUnlock", 1,  "Zero Isle Center", 103,  103),
    LocationData("DungeonUnlock", 1,  "Destiny Tower", 104,  104),
    LocationData("DungeonUnlock", 1,  "Oblivion Forest", 107,  107),
    LocationData("DungeonUnlock", 1,  "Treacherous Waters", 108,  108),
    LocationData("DungeonUnlock", 1,  "Southeastern Islands", 109,  109),
    LocationData("DungeonUnlock", 1,  "Inferno Cave", 110,  110),
    LocationData("DungeonUnlock", 12,  "1st Station Pass", 121,  111),   # 12 subareas
    # Special Episode Dungeons
    #LocationData("SpecialDungeonUnlock", 5, "Star Cave1", 127, 123),
    #LocationData("SpecialDungeonUnlock", 1,  "Murky Forest", 128,  128),
    #LocationData("SpecialDungeonUnlock", 1,  "Eastern Cave", 129,  129),
    #LocationData("SpecialDungeonUnlock", 3,  "Fortune Ravine", 132,  130),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 3,  "Barren Valley", 135,  133),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 1,  "Dark Wasteland", 136,  136),
    #LocationData("SpecialDungeonUnlock", 2,  "Temporal Tower2", 138,  137),   # 2 subareas
    #LocationData("SpecialDungeonUnlock", 2,  "Dusk Forest2", 140,  139),   # 2 subareas
    #LocationData("SpecialDungeonUnlock", 1,  "Spacial Cliffs", 141,  141),
    #LocationData("SpecialDungeonUnlock", 3,  "Dark Ice Mountain", 144,  142),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 1,  "Icicle Forest", 145,  145),
    #LocationData("SpecialDungeonUnlock", 3,  "Vast Ice Mountain", 148,  146),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 1,  "Southern Jungle", 149,  149),
    #LocationData("SpecialDungeonUnlock", 3,  "Boulder Quarry", 152,  150),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 1,  "Right Cave Path", 153,  153),
    #LocationData("SpecialDungeonUnlock", 1,  "Left Cave Path", 154,  154),
    #LocationData("SpecialDungeonUnlock", 3,  "Limestone Cavern", 157,  155),   # 3 subareas
    #LocationData("SpecialDungeonUnlock", 7,  "Spring Cave", 164,  158),   # 7 subareas
    LocationData("DungeonUnlock", 1, "Star Cave", 174,  174),
    # Add Dojo dungeons as optional
    LocationData("Event", 0,  "Final Boss", 300, 300),
    # "Shaymin Village", 175,
    # "Armaldo's Shelter", 176,
    # "Luminous Spring", 177,
    # "Hot Spring", 178,
    # "Rescue", 179

    LocationData("ProgressiveBagUpgrade", 0, "Progressive Bag", 500, 500)
]

location_Dict_by_id: typing.Dict[int, LocationData] = {location.id: location for location in EOS_location_table}
