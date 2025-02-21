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
    ItemData("Drenched Bluff", 3, ItemClassification.progression, 3, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x3),
    ItemData("Mt. Bristle", 4, ItemClassification.progression, 4, ["Unique", "EarlyDungeons", "MissionDungeons"], 0x4),
    ItemData("Waterfall Cave", 6, ItemClassification.progression, 6, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x6),
    ItemData("Apple Woods", 7, ItemClassification.progression, 7, ["Unique", "EarlyDungeons", "MissionDungeons"], 0x7),
    ItemData("Craggy Coast", 8, ItemClassification.progression, 8, ["Unique", "EarlyDungeons", "MissionDungeons"], 0x8),
    ItemData("Side Path", 9, ItemClassification.progression, 9, ["Unique", "EarlyDungeons", "MissionDungeons"], 0x9),
    ItemData("Mt. Horn", 10, ItemClassification.progression, 10, ["Unique", "EarlyDungeons", "MissionDungeons"], 0xA),
    ItemData("Rock Path", 11, ItemClassification.progression, 11, ["Unique", "EarlyDungeons", "MissionDungeons"], 0xB),
    ItemData("Foggy Forest", 12, ItemClassification.progression, 12, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0xC),
    ItemData("Forest Path", 13, ItemClassification.progression, 13, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0xD),
    ItemData("Steam Cave", 14, ItemClassification.progression, 14, ["Unique", "EarlyDungeons", "MissionDungeons"], 0xE),
    ItemData("Amp Plains", 17, ItemClassification.progression, 17, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0X11),
    ItemData("Northern Desert", 20, ItemClassification.progression, 20, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x14),
    ItemData("Quicksand Cave", 21, ItemClassification.progression, 21, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x15),
    ItemData("Crystal Cave", 24, ItemClassification.progression, 24, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x18),
    ItemData("Crystal Crossing", 25, ItemClassification.progression, 25, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x19),
    ItemData("Chasm Cave", 27, ItemClassification.progression, 27, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x1B),
    ItemData("Dark Hill", 28, ItemClassification.progression, 28, ["Unique", "EarlyDungeons", "MissionDungeons"], 0x1C),
    ItemData("Sealed Ruin", 29, ItemClassification.progression, 29, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x1D),
    ItemData("Dusk Forest", 32, ItemClassification.progression, 32, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x20),
    ItemData("Deep Dusk Forest", 33, ItemClassification.progression, 33, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x21),
    ItemData("Treeshroud Forest", 34, ItemClassification.progression, 34,
             ["Unique", "EarlyDungeons", "MissionDungeons"], 0x22),
    ItemData("Brine Cave", 35, ItemClassification.progression, 35, ["Unique", "EarlyDungeons", "MissionDungeons"],
             0x23),
    #ItemData("Hidden Land", 38, ItemClassification.progression, 38, ["Unique", "BossDungeons"], 0x26),
    ItemData("Temporal Tower", 41, ItemClassification.progression, 41, ["Unique", "BossDungeons"], 0x29),
    ItemData("Mystifying Forest", 44, ItemClassification.progression, 44, ["Unique", "LateDungeons", "MissionDungeons"],
             0x2C),
    ItemData("Blizzard Island", 46, ItemClassification.progression, 46, ["Unique", "LateDungeons", "MissionDungeons"],
             0x2E),
    ItemData("Crevice Cave", 47, ItemClassification.progression, 47, ["Unique", "LateDungeons", "MissionDungeons"],
             0x2F),
    ItemData("Surrounded Sea", 50, ItemClassification.progression, 50, ["Unique", "LateDungeons", "MissionDungeons"],
             0x32),
    ItemData("Miracle Sea", 51, ItemClassification.progression, 51, ["Unique", "LateDungeons", "MissionDungeons"],
             0x33),
    #ItemData("Ice Aegis Cave", 54, ItemClassification.useful, 54, ["Unique", "Dungeons"], 0x36),
    ItemData("Mt. Travail", 62, ItemClassification.progression, 62, ["Unique", "LateDungeons", "MissionDungeons"],
             0x3E),
    ItemData("The Nightmare", 63, ItemClassification.progression, 63, ["Unique", "LateDungeons", "MissionDungeons"],
             0x3F),
    ItemData("Spacial Rift", 64, ItemClassification.progression, 64, ["Unique", "LateDungeons", "MissionDungeons"],
             0x40),
    ItemData("Dark Crater", 67, ItemClassification.progression, 67, ["Unique", "BossDungeons"], 0x43),
    ItemData("Concealed Ruins", 70, ItemClassification.progression, 70, ["Unique", "LateDungeons", "MissionDungeons"],
             0x46),
    ItemData("Marine Resort", 72, ItemClassification.progression, 72, ["Unique", "LateDungeons", "MissionDungeons"],
             0x48),
    ItemData("Bottomless Sea", 73, ItemClassification.progression, 73, ["Unique", "LateDungeons", "MissionDungeons"],
             0x49),
    ItemData("Shimmer Desert", 75, ItemClassification.progression, 75, ["Unique", "LateDungeons", "MissionDungeons"],
             0x4B),
    ItemData("Mt. Avalanche", 77, ItemClassification.progression, 77, ["Unique", "LateDungeons", "MissionDungeons"],
             0x4D),
    ItemData("Giant Volcano", 79, ItemClassification.progression, 79, ["Unique", "LateDungeons", "MissionDungeons"],
             0x4F),
    ItemData("World Abyss", 81, ItemClassification.progression, 81, ["Unique", "LateDungeons", "MissionDungeons"],
             0x51),
    ItemData("Sky Stairway", 83, ItemClassification.progression, 83, ["Unique", "LateDungeons", "MissionDungeons"],
             0x53),
    ItemData("Mystery Jungle", 85, ItemClassification.progression, 85, ["Unique", "LateDungeons", "MissionDungeons"],
             0x55),
    ItemData("Serenity River", 87, ItemClassification.progression, 87, ["Unique", "LateDungeons", "MissionDungeons"],
             0x57),
    ItemData("Landslide Cave", 88, ItemClassification.progression, 88, ["Unique", "LateDungeons", "MissionDungeons"],
             0x58),
    ItemData("Lush Prairie", 89, ItemClassification.progression, 89, ["Unique", "LateDungeons", "MissionDungeons"],
             0x59),
    ItemData("Tiny Meadow", 90, ItemClassification.progression, 90, ["Unique", "LateDungeons", "MissionDungeons"],
             0x5A),
    ItemData("Labyrinth Cave", 91, ItemClassification.progression, 91, ["Unique", "LateDungeons", "MissionDungeons"],
             0x5B),
    ItemData("Oran Forest", 92, ItemClassification.progression, 92, ["Unique", "LateDungeons", "MissionDungeons"],
             0x5C),
    ItemData("Lake Afar", 93, ItemClassification.progression, 93, ["Unique", "LateDungeons", "MissionDungeons"], 0x5D),
    ItemData("Happy Outlook", 94, ItemClassification.progression, 94, ["Unique", "LateDungeons", "MissionDungeons"],
             0x5E),
    ItemData("Mt. Mistral", 95, ItemClassification.progression, 95, ["Unique", "LateDungeons", "MissionDungeons"],
             0x5F),
    ItemData("Shimmer Hill", 96, ItemClassification.progression, 96, ["Unique", "LateDungeons", "MissionDungeons"],
             0x60),
    ItemData("Lost Wilderness", 97, ItemClassification.progression, 97, ["Unique", "LateDungeons", "MissionDungeons"],
             0x61),
    ItemData("Midnight Forest", 98, ItemClassification.progression, 98, ["Unique", "LateDungeons", "MissionDungeons"],
             0x62),
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
    ItemData("1st Station Pass", 111, ItemClassification.progression, 111,
             ["Unique", "LateDungeons", "MissionDungeons"], 0x6F),
    ItemData("Bidoof's Wish'", 123, ItemClassification.progression, 123, ["Unique", "Special Dungeons"], 0x0),
    # ItemData("SE Star Cave", 123, ItemClassification.useful, 123, ["Unique", "Special Dungeons"], 0x7B),
    ItemData("Igglybuff the Prodigy", 128, ItemClassification.progression, 128, ["Unique", "Special Dungeons"], 0x1),
    # ItemData("Murky Forest", 128, ItemClassification.useful, 128, ["Unique", "Special Dungeons"], 0x80),
    # ItemData("Eastern Cave", 129, ItemClassification.useful, 129, ["Unique", "Special Dungeons"], 0x81),
    # ItemData("Fortune Ravine", 130, ItemClassification.useful, 130, ["Unique", "Special Dungeons"], 0x82),
    ItemData("In the Future of Darkness", 133, ItemClassification.progression, 133, ["Unique", "Special Dungeons"], 0x4),
    # ItemData("Barren Valley", 133, ItemClassification.useful, 133, ["Unique", "Special Dungeons"], 0x85),
    # ItemData("Dark Wasteland", 136, ItemClassification.useful, 136, ["Unique", "Special Dungeons"], 0x88),
    # ItemData("Temporal Tower2", 137, ItemClassification.useful, 137, ["Unique", "Special Dungeons"], 0x89),
    # ItemData("Dusk Forest2", 139, ItemClassification.useful, 139, ["Unique", "Special Dungeons"], 0x8B),
    # ItemData("Spacial Cliffs", 141, ItemClassification.useful, 141, ["Unique", "Special Dungeons"], 0x8D),
    # ItemData("Dark Ice Mountain", 142, ItemClassification.useful, 142, ["Unique", "Special Dungeons"], 0x8E),
    # ItemData("Icicle Forest", 145, ItemClassification.useful, 145, ["Unique", "Special Dungeons"], 0x91),
    # ItemData("Vast Ice Mountain", 146, ItemClassification.useful, 146, ["Unique", "Special Dungeons"], 0x92),
    ItemData("Here Comes Team Charm!", 149, ItemClassification.progression, 149, ["Unique", "Special Dungeons"], 0x3),
    # ItemData("Southern Jungle", 149, ItemClassification.useful, 149, ["Unique", "Special Dungeons"], 0x95),
    # ItemData("Boulder Quarry", 150, ItemClassification.useful, 150, ["Unique", "Special Dungeons"], 0x96),
    # ItemData("Right Cave Path", 153, ItemClassification.useful, 153, ["Unique", "Special Dungeons"], 0x99),
    # ItemData("Left Cave Path", 154, ItemClassification.useful, 154, ["Unique", "Special Dungeons"], 0x9A),
    # ItemData("Limestone Cavern", 155, ItemClassification.useful, 155, ["Unique", "Special Dungeons"], 0x9B),
    ItemData('Today\'s "Oh My Gosh"', 158, ItemClassification.progression, 158, ["Unique", "Special Dungeons"], 0x2),
    # ItemData("Spring Cave", 158, ItemClassification.useful, 158, ["Unique", "Special Dungeons"], 0x9E),
    ItemData("Star Cave", 174, ItemClassification.progression, 174, ["Unique", "LateDungeons", "MissionDungeons"],
             0xAE),
    ItemData("Shaymin Village", 175, ItemClassification.useful, 175, ["Unique", "ExtraDungeons"], 0xAF),
    ItemData("Luminous Spring", 177, ItemClassification.useful, 177, ["Unique", "ExtraDungeons"], 0xB1),
    ItemData("Hot Spring", 178, ItemClassification.useful, 178, ["Unique", "ExtraDungeons"], 0xB2),

    #ItemData("Dojo Normal/Fly Maze", 180, ItemClassification.progression, 180, ["Unique", "Dojo Dungeons"], 0xB4),

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
    ItemData("Relic Fragment Shard", 200, ItemClassification.progression_skip_balancing, 200, ["Macguffin"], 0x00),
    #ItemData("Cresselia Feather", 201, ItemClassification.progression, 201, ["Macguffin"], 0x00),

    ItemData("Victory", 300, ItemClassification.progression, 0, [], 0x00),
    ItemData("Bag Upgrade", 370, ItemClassification.progression, 0, ["ProgressiveBag", "Generic"], 0x00),

    ItemData("Secret Rank", 409, ItemClassification.progression, 0, ["Rank"], 0x0),
    ItemData("Mystery Part", 500, ItemClassification.useful, 0, ["Item", "Single"], 0xAD),
    ItemData("Secret Slab", 501, ItemClassification.useful, 0, ["Item", "Single"], 0xAE),
    ItemData("Amber Tear", 502, ItemClassification.useful, 0, ["Item", "Single"], 0x3A),
    ItemData("Friend Bow", 503, ItemClassification.useful, 0, ["Item", "Single"], 0x35),

    ItemData("Regirock", 504, ItemClassification.useful, 0, ["Legendary"], 0x0),
    ItemData("Regice", 505, ItemClassification.useful, 0, ["Legendary"], 0x1),
    ItemData("Registeel", 506, ItemClassification.useful, 0, ["Legendary"], 0x2),
    ItemData("Groudon", 507, ItemClassification.useful, 0, ["Legendary"], 0x3),
    ItemData("Uxie", 508, ItemClassification.useful, 0, ["Legendary"], 0x4),
    ItemData("Mespirit", 509, ItemClassification.useful, 0, ["Legendary"], 0x5),
    ItemData("Azelf", 510, ItemClassification.useful, 0, ["Legendary"], 0x6),
    ItemData("Dialga", 511, ItemClassification.useful, 0, ["Legendary"], 0x7),
    ItemData("Palkia", 512, ItemClassification.useful, 0, ["Legendary"], 0x8),
    ItemData("Regigigas", 513, ItemClassification.useful, 0, ["Legendary"], 0x9),
    ItemData("Giratina", 514, ItemClassification.useful, 0, ["Legendary"], 0xA),
    ItemData("Celebi", 515, ItemClassification.useful, 0, ["Legendary"], 0xB),
    ItemData("Articuno", 516, ItemClassification.useful, 0, ["Legendary"], 0xC),
    ItemData("Heatran", 517, ItemClassification.useful, 0, ["Legendary"], 0xD),
    ItemData("Primal Dialga", 518, ItemClassification.useful, 0, ["Legendary"], 0xE),
    ItemData("Mew", 519, ItemClassification.useful, 0, ["Legendary"], 0xF),
    ItemData("Manaphy", 520, ItemClassification.useful, 0, ["Legendary"], 0x10),
    ItemData("Phione", 521, ItemClassification.useful, 0, ["Legendary"], 0x11),
    ItemData("Cresselia", 522, ItemClassification.useful, 0, ["Legendary"], 0x12),
    ItemData("Rayquaza", 523, ItemClassification.useful, 0, ["Legendary"], 0x13),
    ItemData("Kyogre", 524, ItemClassification.useful, 0, ["Legendary"], 0x14),
    ItemData("Shaymin", 525, ItemClassification.useful, 0, ["Legendary"], 0x15),

    ItemData("Icy Flute", 526, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x3B),
    ItemData("Fiery Drum", 527, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x3C),
    ItemData("Terra Cymbal", 528, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x3D),
    ItemData("Aqua-Monica", 529, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x3E),
    ItemData("Rock Horn", 530, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x3F),
    ItemData("Grass Cornet", 531, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x40),
    ItemData("Sky Melodica", 532, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x41),
    ItemData("Stellar Symphony", 533, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x56B),
    ItemData("Null Bagpipes", 534, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x56C),
    ItemData("Glimmer Harp", 535, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x56D),
    ItemData("Toxic Sax", 536, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x56E),
    ItemData("Biting Bass", 537, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x56F),
    ItemData("Knockout Bell", 538, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x570),
    ItemData("Spectral Chimes", 539, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x571),
    ItemData("Liar's Lyre", 540, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x572),
    ItemData("Charge Synth", 541, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x573),
    ItemData("Norma-ccordion", 542, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x574),
    ItemData("Psychic Cello", 543, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x575),
    ItemData("Dragu-teki", 544, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x576),
    ItemData("Steel Guitar", 545, ItemClassification.progression_skip_balancing, 0, ["Item", "Instrument"], 0x577),

    ItemData("Hero Evolution", 550, ItemClassification.useful, 0, ["Generic"], 0),
    ItemData("Recruit Evolution", 551, ItemClassification.useful, 0, ["Generic"], 0),
    ItemData("Recruitment", 552, ItemClassification.useful, 0, ["Generic"], 0),
    ItemData("Formation Control", 553, ItemClassification.useful, 0, ["Generic"], 0),
    ItemData("Miracle Chest", 464, ItemClassification.useful, 0, ["Item", "Single"], 0x42),  # Boosts Exp
    ItemData("Wonder Chest", 465, ItemClassification.useful, 0, ["Item", "Single"], 0x43),  # Boosts Exp

    # ItemData("Poke x-1000", 570, ItemClassification.trap, 0, ["Money"], 0),
]
filler_items = [
    ItemData("Heavy Box", 301, ItemClassification.filler, 10, ["Item", "Box"], 0x171),
    ItemData("Shiny Box", 302, ItemClassification.filler, 10, ["Item", "Box"], 0x174),
    ItemData("Nifty Box", 303, ItemClassification.filler, 10, ["Item", "Box"], 0x177),
    ItemData("Dainty Box", 304, ItemClassification.filler, 10, ["Item", "Box"], 0x17A),
    ItemData("Glittery Box", 305, ItemClassification.filler, 10, ["Item", "Box"], 0x17D),
    ItemData("Pretty Box", 306, ItemClassification.filler, 10, ["Item", "Box"], 0x180),
    ItemData("Deluxe Box", 307, ItemClassification.filler, 10, ["Item", "Box"], 0x183),
    ItemData("Light Box", 308, ItemClassification.filler, 10, ["Item", "Box"], 0x186),
    ItemData("Cute Box", 309, ItemClassification.filler, 10, ["Item", "Box"], 0x189),
    ItemData("Hard Box", 310, ItemClassification.filler, 10, ["Item", "Box"], 0x18C),
    ItemData("Sinister Box", 311, ItemClassification.filler, 10, ["Item", "Box"], 0x18F),
    ItemData("Link Box", 312, ItemClassification.filler, 10, ["Item", "Single"], 0x16A),
    ItemData("Sky Gift", 313, ItemClassification.filler, 10, ["Item", "Single"], 0xB4),
    ItemData("Poké x100", 560, ItemClassification.filler, 20, ["Money"], 100),
    ItemData("Poké x500", 561, ItemClassification.filler, 20, ["Money"], 500),
    ItemData("Poké x1000", 562, ItemClassification.filler, 20, ["Money"], 1000),
    ItemData("Poké x5000", 563, ItemClassification.filler, 5, ["Money"], 5000),
    ItemData("Poké x200", 564, ItemClassification.filler, 20, ["Money"], 200),
    ItemData("Poké x1", 565, ItemClassification.filler, 50, ["Money"], 1),
    ItemData("Secret of the Waterfall", 405, ItemClassification.filler, 2, ["Generic"], 0x0),
    ItemData("Chatot Repellent", 406, ItemClassification.filler, 2, ["Generic"], 0x0),
    ItemData("Sky Jukebox", 407, ItemClassification.filler, 2, ["Generic"], 0x0),
    ItemData("Recruitment Sensor", 408, ItemClassification.filler, 2, ["Generic"], 0x0),
    ItemData("Rare Fossil", 410, ItemClassification.filler, 10, ["Item", "Multi"], 0xA),
    ItemData("Reviver Seed", 411, ItemClassification.filler, 5, ["Item", "Single"], 0x49),
    ItemData("Oran Berry", 412, ItemClassification.filler, 20, ["Item", "Single"], 0x46),
    ItemData("Heal Seed", 413, ItemClassification.filler, 20, ["Item", "Single"], 0x45),
    ItemData("Apple", 414, ItemClassification.filler, 20, ["Item", "Single"], 0x6D),
    ItemData("Golden Seed", 393, ItemClassification.filler, 3, ["Item", "Single"], 0x5D),
    ItemData("Ginseng", 394, ItemClassification.filler, 1, ["Item", "Single"], 0x58),
    #ItemData("Gold Ribbon", 395, ItemClassification.filler, 0, ["Item"], 0x20),
    ItemData("Inspiration Strikes!", 400, ItemClassification.trap, 20, ["Trap"], 0x0),
    ItemData("Get Unowned!", 401, ItemClassification.trap, 20, ["Trap"], 0x0),
    ItemData("Nap Time!", 402, ItemClassification.trap, 20, ["Trap"], 0x0),
    ItemData("Sentry Duty!", 403, ItemClassification.trap, 20, ["Trap"], 0x0),
    ItemData("Touch Grass", 404, ItemClassification.trap, 20, ["Trap"], 0x0),
    ItemData("Protein", 480, ItemClassification.filler, 10, ["Item", "Single"], 0x64),
    ItemData("Calcium", 481, ItemClassification.filler, 10, ["Item", "Single"], 0x65),
    ItemData("Iron", 482, ItemClassification.filler, 10, ["Item", "Single"], 0x66),
    ItemData("Nectar", 483, ItemClassification.filler, 10, ["Item", "Single"], 0x67),
    ItemData("Max Elixir", 484, ItemClassification.filler, 10, ["Item", "Single"], 0x63),
    ItemData("Gabite Scale", 485, ItemClassification.filler, 10, ["Item", "Single"], 0x5c),
    ItemData("Zinc", 486, ItemClassification.filler, 10, ["Item", "Single"], 0x6c),

    # specific item Types
    ItemData("Joy Globe", 487, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1FD),  # Normal
    ItemData("Fiery Globe", 488, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x201),  # Fire
    ItemData("Aqua Globe", 489, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x205),  # Water
    ItemData("Soothe Globe", 415, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x209),  # Grass
    ItemData("Volt Globe", 416, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x20D),  # Electric
    ItemData("Icy Globe", 417, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x211),  # Ice
    ItemData("Power Globe", 418, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x215),  # Fighting
    ItemData("Poison Globe", 419, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x219),  # Poison
    ItemData("Terra Globe", 420, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x21D),  # Ground
    ItemData("Sky Globe", 421, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x221),  # Flying
    ItemData("Psyche Globe", 422, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x225),  # Psychic
    ItemData("Defend Globe", 423, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x229),  # Bug
    ItemData("Rock Globe", 424, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x22D),  # Rock
    ItemData("Nether Globe", 425, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x231),  # Ghost
    ItemData("Dragon Globe", 426, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x235),  # Dragon
    ItemData("Dusk Globe", 427, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x239),  # Dark
    ItemData("Steel Globe", 428, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x23D),  # Steel

    # Legendary specific items
    ItemData("Freeze Veil", 429, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1D8),  # Articuno
    ItemData("Thunder Veil", 430, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1D9),  # Zapdos
    ItemData("Fire Veil", 431, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DA),  # Moltres
    ItemData("Havoc Robe", 432, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DB),  # Mewtwo
    ItemData("Life Ring", 433, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DC),  # Mew
    ItemData("Bolt Fang", 434, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DD),  # Raikou
    ItemData("Flare Fang", 435, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DE),  # Entei
    ItemData("Aqua Mantle", 436, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1DF),  # Suicune
    ItemData("Silver Veil", 437, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E0),  # Lugia
    ItemData("Rainbow Veil", 438, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E1),  # Ho-oh
    ItemData("Chrono Veil", 439, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E2),  # Celebi
    ItemData("Rock Sash", 440, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E3),  # Regirock
    ItemData("Ice Sash", 441, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E4),  # Regice
    ItemData("Steel Sash", 442, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E5),  # Registeel
    ItemData("Heart Brooch", 443, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E6),  # Latias
    ItemData("Eon Veil", 444, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E7),  # Latios
    ItemData("Seabed Veil", 445, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E8),  # Kyogre
    ItemData("Terra Ring", 446, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1E9),  # Groudon
    ItemData("SkyHigh Veil", 447, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1EA),  # Rayquaza
    ItemData("Wish Mantle", 448, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1EB),  # Jirachi
    ItemData("Revive Robe", 449, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1EC),  # Deoxys
    ItemData("Edify Robe", 450, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1EF),  # Uxie
    ItemData("Charity Robe", 451, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F0),  # Mesprit
    ItemData("Hope Robe", 452, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F1),  # Azelf
    ItemData("Time Shield", 453, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F2),  # Dialga
    ItemData("Air Blade", 454, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F3),  # Palkia
    ItemData("Searing Ring", 455, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F4),  # Heatran
    ItemData("Ancient Ring", 456, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F5),  # Regigigas
    ItemData("Nether Veil", 457, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F6),  # Giratina
    ItemData("Lunar Veil", 458, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F7),  # Cresselia
    ItemData("Ripple Cape", 459, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x3E5),  # Phione
    ItemData("Marine Cache", 460, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1D7),  # Phione
    ItemData("Tidal Cape", 461, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F8),  # Manaphy
    ItemData("Eclipse Robe", 462, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x1F9),  # Darkrai
    ItemData("Purify Veil", 463, ItemClassification.filler, 3, ["Item", "Exclusive"], 0x547),  # Shaymin

]
filler_item_weights = [item.start_number for item in filler_items]
filler_item_table: Dict[str, ItemData] = {item.name: item for item in filler_items}

item_frequencies: Dict[str, int] = {
    "Bag Upgrade": 5
}

item_table: Dict[str, ItemData] = {item.name: item for item in EOS_item_table}
item_table.update(filler_item_table)
item_table_by_id: Dict[int, ItemData] = {item.id: item for item in item_table.values()}

item_table_by_groups = get_item_table_by_groups()
lootbox_table: Dict[str, Dict[str, int]] = {
    "Gorgeous Box": {
        "Gold Ribbon": 0x20,
    },
    "Heavy Box": {
        "Gravelerock": 0x7,
        "Geo Pebble": 0x8,
        "Gravelyrock": 0x89,
        "Iron Thorn": 0x2,
        "Silver Spike": 0x3,
        "Gold Fang": 0x4,
        "Cacnea Spike": 0x5,
        "Corsola Twig": 0x6,
        "Stick": 0x1,
        "Gold Thorn": 0x9,
        "Rare Fossil": 0xA,
        "Gone Pebble": 0xA7,
    },
    "Shiny Box": {
        "Used TM": 0xBB,
        "Focus Punch": 0xBC,
        "Dragon Claw": 0xBD,
        "Water Pulse": 0xBE,
        "Calm Mind": 0xBF,
        "Roar": 0xC0,
        "Toxic": 0xC1,
        #"Hail": 0xC2,
        "Bulk Up": 0xC3,
        "Bullet Seed": 0xC4,
        "Hidden Power": 0xC5,
        "Taunt": 0xC7,
        "Ice Beam": 0xC8,
        "Blizzard": 0xC9,
        "Hyper Beam": 0xCA,
        "Light Screen": 0xCB,
        "Protect": 0xCC,
        "Giga Drain": 0xCE,
        "Safeguard": 0xCF,
        "Frustration": 0xD0,
        "Solar Beam": 0xD1,
        "Iron Tail": 0xD2,
        "Thunderbolt": 0xD3,
        "Thunder": 0xD4,
        "Earthquake": 0xD5,
        "Return": 0xD6,
        "Dig": 0xD7,
        "Psychic": 0xD8,
        "Shadow Ball": 0xD9,
        "Brick Break": 0xDA,
        "Reflect": 0xDC,
        "Shock Wave": 0xDD,
        "Flamethrower": 0xDE,
        "Sludge Bomb": 0xDF,
        "Fire Blast": 0xE1,
        "Aerial Ace": 0xE3,
        "Torment": 0xE4,
        "Facade": 0xE5,
        "Secret Power": 0xE6,
        "Rest": 0xE7,
        "Attract": 0xE8,
        "Thief": 0xE9,
        "Steel Wing": 0xEA,
        "Skill Swap": 0xEB,
        "Overheat": 0xED,
        "Roost": 0xEE,
        "Focus Blast": 0xEF,
        "Energy Ball": 0xF0,
        "False Swipe": 0xF1,
        "Brine": 0xF2,
        "Fling": 0xF3,
        "Charge Beam": 0xF4,
        "Endure": 0xF5,
        "Dragon Pulse": 0xF6,
        "Drain Punch": 0xF7,
        "Will-O-Wisp": 0xF8,
        "Silver Wind": 0xF9,
        "Embargo": 0xFA,
        "Explosion": 0xFB,
        "Shadow Claw": 0xFC,
        "Payback": 0xFD,
        "Recycle": 0xFE,
        "Giga Impact": 0xFF,
        "Rock Polish": 0x100,
        "Wide Slash": 0x101,
        "Vaccum Cut": 0x104,
        "Dive": 0x105,
        "Flash": 0x106,
        "Stone Edge": 0x107,
        "Avalanche": 0x108,
        "Thunder Wave": 0x109,
        "Gyro Ball": 0x10A,
        "Swords Dance": 0x10B,
        "Stealth Rock": 0x10C,
        "Psych Up": 0x10D,
        "Captivate": 0x10E,
        "Dark Pulse": 0x10F,
        "Rock Slide": 0x110,
        "X-Scissor": 0x111,
        "Sleep Talk": 0x112,
        "Natural Gift": 0x113,
        "Poison Jab": 0x114,
        "Dream EAter": 0x115,
        "Grass Knot": 0x116,
        "Swagger": 0x117,
        "Pluck": 0x118,
        "U-turn": 0x119,
        "Substitute": 0x11A,
        "Flash Cannon": 0x11B,
        "Trick Room": 0x11C,
        "Cut": 0x11D,
        "Fly": 0x11E,
        "Surf": 0x11F,
        "Strength": 0x120,
        "Defog": 0x121,
        "Rock Smash": 0x122,
        "Waterfall": 0x123,
        "Rock Climb": 0x124,
    },
    "Nifty Box": {
        "Mobile Scarf": 0x10,
        "Scope Lens": 0x13,
        "No Stick Cap": 0x15,
        "X-Ray Specs": 0x18,
        "Tight Belt": 0x1E,
        "Goggle Specs": 0x21,
        "Diet Ribbon": 0x22,
        "Pass Scarf": 0x33,
        "Weather Band": 0x34,
        "Space Globe": 0x2B,
        "IQ Booster": 0x44,
        "Gaggle Specs": 0xF,
        "Y-Ray Specs": 0xE,
        "No-Slip Cap": 0xD,
        "Curve Band": 0x2E,
        "Whiff Specs": 0x2F,
        "Patsy Band": 0x14,
    },
    "Dainty Box": {
        "White Gummi": 0x77,
        "Red Gummi": 0x78,
        "Blue Gummi": 0x79,
        "Grass Gummi": 0x7A,
        "Yellow Gummi": 0x7B,
        "Clear Gummi": 0x7C,
        "Orange Gummi": 0x7D,
        "Pink Gummi": 0x7E,
        "Brown Gummi": 0x7F,
        "Sky Gummi": 0x80,
        "Gold Gummi": 0x81,
        "Green Gummi": 0x82,
        "Gray Gummi": 0x83,
        "Purple Gummi": 0x84,
        "Royal Gummi": 0x85,
        "Black Gummi": 0x86,
        "Silver Gummi": 0x87,
        "Wonder Gummi": 0x88,
        "Wander Gummi": 0xA8
    },
    "Glittery Box": {
        "Oran Berry": 0x46,
        "Oren Berry": 0x75,
        "Reviver Seed": 0x49,
        "Reviser Seed": 0x69,
        "Max Elixir": 0x63,
        "Mix Elixir": 0x74,
        "Heal Seed": 0x45,
        "Sitrus Berry": 0x47,
        "Eyedrop Seed": 0x48,
        "Life Seed": 0x4D,
        "Rawst Berry": 0x4E,
        "Quick Seed": 0x50,
        "Pecha Berry": 0x51,
        "Cheri Berry": 0x52,
        "Totter Seed": 0x53,
        "Sleep Seed": 0x54,
        "Warp Seed": 0x56,
        "Blast Seed": 0x57,
        "Ginseng": 0x58,
        "Joy Seed": 0x59,
        "Chesto Berry": 0x5A,
        "Stun Seed": 0x5B,
        "Gabite Scale": 0x5C,
        "Pure Seed": 0x5E,
        "Violent Seed": 0x60,
        "Vanish Seed": 0x61,
        "Protein": 0x64,
        "Calcium": 0x65,
        "Iron": 0x66,
        "Nectar": 0x67,
        "Slip Seed": 0x6A,
        "Vila Seed": 0x6B,
        "Zinc": 0x6C,
        "Apple": 0x6D,
        "Big Apple": 0x6E,
        "Huge Apple": 0x70,
        "Dough Seed": 0x76,
    },
    "Pretty Box": {
        "Upgrade": 0x8B,
        "King's Rock": 0x8C,
        "Thunderstone": 0x8D,
        "Deepseascale": 0x8E,
        "Deepseatooth": 0x8F,
        "Sun Stone": 0x90,
        "Moon Stone": 0x91,
        "Fire Stone": 0x92,
        "Water Stone": 0x93,
        "Metal Coat": 0x94,
        "Leaf Stone": 0x95,
        "Dragon Scale": 0x96,
        "Link Cable": 0x97,
        "Dubious Disc": 0x98,
        "Protector": 0x99,
        "Reaper Cloth": 0x9A,
        "Razor Fang": 0x9B,
        "Razor Claw": 0x9C,
    },
    "Deluxe Box": {
        "Gold Ribbon": 0x20,
        "Golden Seed": 0x50,
        "Golden Apple": 0x73,
    },
    "Light Box": {
        "Prize Ticket": 0xA9,
        "Silver Ticket": 0xAA,
        "Gold Ticket": 0xAB,
        "Prism Ticket": 0xAC,
    },
    "Cute Box": {
        "Silver Bow": 0x1AC,
        "Brown Bow": 0x1AD,
        "Red Bow": 0x1AE,
        "Pick Bow": 0x1AF,
        "Orange Bow": 0x1B0,
        "Yellow Bow": 0x1B1,
        "Lime Bow": 0x1B2,
        "Green Bow": 0x1B3,
        "Viridian Bow": 0x1B4,
        "Minty Bow": 0x1B5,
        "Sky Blue Bow": 0x1B6,
        "Blue Bow": 0x1B7,
        "Cobalt Bow": 0x1B8,
        "Purple Bow": 0x1B9,
        "Violet Bow": 0x1BA,
        "Fuchsia Bow": 0x1BB,

    },
    "Hard Box": {
        "Key": 0xB6,
        "Lost Loot": 0xBA,
        "Unown Rock A": 0x190,
        "Unown Rock B": 0x191,
        "Unown Rock C": 0x192,
        "Unown Rock D": 0x193,
        "Unown Rock E": 0x194,
        "Unown Rock F": 0x195,
        "Unown Rock G": 0x196,
        "Unown Rock H": 0x197,
        "Unown Rock I": 0x198,
        "Unown Rock J": 0x199,
        "Unown Rock K": 0x19A,
        "Unown Rock L": 0x19B,
        "Unown Rock M": 0x19C,
        "Unown Rock N": 0x19D,
        "Unown Rock O": 0x19E,
        "Unown Rock P": 0x19F,
        "Unown Rock Q": 0x1A0,
        "Unown Rock R": 0x1A1,
        "Unown Rock S": 0x1A2,
        "Unown Rock T": 0x1A3,
        "Unown Rock U": 0x1A4,
        "Unown Rock V": 0x1A5,
        "Unown Rock W": 0x1A6,
        "Unown Rock X": 0x1A7,
        "Unown Rock Y": 0x1A8,
        "Unown Rock Z": 0x1A9,
        "Unown Rock !": 0x1AA,
        "Unown Rock ?": 0x1AB,

    },
    "Sinister Box": {
        "Blinker Seed": 0x4A,
        "Doom Seed": 0x4B,
        "X-Eye Seed": 0x4C,
        "Hunger Seed": 0x4F,
        "Totter Seed": 0x53,
        "Sleep Seed": 0x54,
        "Stun Seed": 0x5B,
        "Vile Seed": 0x5E,
        "DropEye Seed": 0x68,
        "Grimy Food": 0x6F
    },

}
