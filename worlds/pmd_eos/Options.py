import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet


class DungeonNameRandomizer(DefaultOnToggle):
    """Randomizes the names of the dungeons. IDs and completion requirements stay the same"""
    display_name = "Dungeon Name Randomization"

class Goal(Choice):
    """Change the desired goal to complete the game"""
    display_name = "Goal"
    option_dialga = 0
    default = 0

@dataclass
class EOSOptions(PerGameCommonOptions):
    dungeon_rando: DungeonNameRandomizer
    goal: Goal
