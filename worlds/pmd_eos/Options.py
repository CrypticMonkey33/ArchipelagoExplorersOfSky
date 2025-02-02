import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Toggle, Choice, PerGameCommonOptions, StartInventoryPool, NamedRange


class DungeonNameRandomizer(DefaultOnToggle):
    """NOT IMPLEMENTED YET
    Randomizes the names of the dungeons. IDs and completion requirements stay the same"""
    display_name = "Dungeon Name Randomization"


class Goal(Choice):
    """Change the desired goal to complete the game (Currently only Dialga is implemented)"""
    display_name = "Goal"
    option_dialga = 0
    option_darkrai = 1
    default = 0


class FragmentShards(NamedRange):
    """ How many Relic Fragment Shards should be in the game
    (Macguffins) that you must get to unlock Hidden Land"""
    range_start = 4
    range_end = 10
    special_range_names = {
        "easy": 4,
        "normal": 6,
        "hard": 8,
        "extreme": 10
    }
    default = 6


class ExtraShards(NamedRange):
    """ How many extra Fragment Shards should be in the game?"""
    range_start = 0
    range_end = 10
    special_range_names = {
        "easy": 6,
        "normal": 4,
        "hard": 2,
        "extreme": 0
    }
    default = 4


class Recruitment(DefaultOnToggle):
    """Start with recruitment enabled?"""
    display_name = "Recruitment Enable"


class RecruitmentEvolution(DefaultOnToggle):
    """Start with Recruitment Evolution Enabled?"""
    display_name = "Recruitment Evolution Enable"


class FullTeamFormationControl(DefaultOnToggle):
    """ Start with full team formation control?"""
    display_name = "Formation Control Enable"


class LevelScaling(DefaultOnToggle):
    """Allow for dungeons to scale to the highest level of your party members?"""
    display_name = "Level Scaling"


class StartWithBag(DefaultOnToggle):
    """Start with bag? If False all bag upgrades will be randomized in the game.
    If true, you will get one bag upgrade (16 slots) and the rest will be randomized"""

    display_name = "Start with Bag?"


class DojoDungeons(Choice):
    """How many dojo dungeons should be randomized?"""
    display_name = "Dojo Dungeons Randomized"
    option_all_open = 10
    option_all_random = 0
    option_start_with_three = 3
    option_start_with_one = 1
    default = 0


@dataclass
class EOSOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    dungeon_rando: DungeonNameRandomizer
    goal: Goal
    recruit: Recruitment
    recruit_evo: RecruitmentEvolution
    team_form: FullTeamFormationControl
    level_scale: LevelScaling
    bag_on_start: StartWithBag
    dojo_dungeons: DojoDungeons
    shard_fragments: FragmentShards
    extra_shards: ExtraShards
