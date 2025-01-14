from BaseClasses import Location

BASE_OFFSET = 100000000

class EOSLocation(Location):

    groups: str = ""
    classification: int = -1
    dungeon_length: int = 1
    id: int = -1
    def __init__(self, item_id, classification, dungeon_length, groups):
        self.groups = groups
        self.classification = classification
        self.dungeon_length = dungeon_length
        self.id = None if item_id is None else item_id + BASE_OFFSET


EOS_location_table = {
    "Test Dungeon": 0,  # Should be unused
    "Beach Cave": 1,
    "Drenched Bluff": 3,
    "Mt. Bristle": 4,  # 2 subareas
    "Waterfall Cave": 6,
    "Apple Woods": 7,
    "Craggy Coast": 8,
    "Side Path": 9,
    "Mt. Horn": 10,
    "Rock Path": 11,
    "Foggy Forest": 12,
    "Forest Path": 13,
    "Steam Cave": 14,  # 3 subareas
    "Amp Plains": 17,  # 3 subareas
    "Northern Desert": 20,
    "Quicksand Cave": 21,  # 3 subareas
    "Crystal Cave": 24,
    "Crystal Crossing": 25,  # 2 subareas
    "Chasm Cave": 27,
    "Dark Hill": 28,
    "Sealed Ruin": 29,  # 3 subareas
    "Dusk Forest1": 32,
    "Deep Dusk Forest": 33,
    "Treeshroud Forest": 34,
    "Brine Cave": 35,  # 3 subareas
    "Hidden Land": 38,  # 3 subareas
    "Temporal Tower1": 41,  # 3 subareas
    "Mystifying Forest": 44,  # start of extra levels, 2 subareas
    "Blizzard Island": 46,
    "Crevice Cave": 47,  # 3 subareas
    "Surrounded Sea": 50,
    "Miracle Sea": 51,  # 3 subareas
    "Ice Aegis Cave": 54,  # 8 subareas
    "Mt. Travail": 62,
    "The Nightmare": 63,
    "Spacial Rift": 64,  # 3 subareas
    "Dark Crater": 67,  # 3 subareas
    "Concealed Ruins": 70,  # 2 subareas
    "Marine Resort": 72,
    "Bottomless Sea": 73,  # 2 subareas
    "Shimmer Desert": 75,  # 2 subareas
    "Mt. Avalanche": 77,  # 2 subareas
    "Giant Volcano": 79,  # 2 subareas
    "World Abyss": 81,  # 2 subareas
    "Sky Stairway": 83,  # 2 subareas
    "Mystery Jungle": 85,  # 2 subareas
    "Serenity River": 87,
    "Landslide Cave": 88,
    "Lush Prairie": 89,
    "Tiny Meadow": 90,
    "Labyrinth Cave": 91,
    "Oran Forest": 92,
    "Lake Afar": 93,
    "Happy Outlook": 94,
    "Mt. Mistral": 95,
    "Shimmer Hill": 96,
    "Lost Wilderness": 97,
    "Midnight Forest": 98,
    "Zero Isle North": 99,
    "Zero Isle East": 100,
    "Zero Isle West": 101,
    "Zero Isle South": 102,
    "Zero Isle Center": 103,
    "Destiny Tower": 104,
    "[M:D1]Dummy0": 105,
    "[M:D1]Dummy1": 106,
    "Oblivion Forest": 107,
    "Treacherous Waters": 108,
    "Southeastern Islands": 109,
    "Inferno Cave": 110,
    "1st Station Pass": 111,  # 12 subareas
    "Star Cave1": 123,  # 5 subareas
    "Murky Forest": 128,
    "Eastern Cave": 129,
    "Fortune Ravine": 130,  # 3 subareas
    "Barren Valley": 133,  # 3 subareas
    "Dark Wasteland": 136,
    "Temporal Tower2": 137,  # 2 subareas
    "Dusk Forest2": 139,  # 2 subareas
    "Spacial Cliffs": 141,
    "Dark Ice Mountain": 142,  # 3 subareas
    "Icicle Forest": 145,
    "Vast Ice Mountain": 146,  # 3 subareas
    "Southern Jungle": 149,
    "Boulder Quarry": 150,  # 3 subareas
    "Right Cave Path": 153,
    "Left Cave Path": 154,
    "Limestone Cavern": 155,  # 3 subareas
    "Spring Cave": 158,  # 7 subareas
    "[M:D1]Dummy2": 165,  # unused
    "[M:D1]Dummy3": 166,  # unused
    "[M:D1]Dummy4": 167,  # unused
    "[M:D1]Dummy5": 168,  # unused
    "[M:D1]Dummy6": 169,  # unused
    "[M:D1]Dummy7": 170,  # unused
    "[M:D1]Dummy8": 171,  # unused
    "[M:D1]Dummy9": 172,  # unusued 2 subareas
    "Star Cave2": 174,
    "Shaymin Village": 175,
    "Armaldo's Shelter": 176,
    "Luminous Spring": 177,
    "Hot Spring": 178,
    "Rescue": 179
}