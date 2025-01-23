import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet


class DungeonNameRandomizer(DefaultOnToggle):
    """Randomizes the names of the dungeons. IDs and completion requirements stay the same"""
    display_name = "Dungeon Name Randomization"


class Goal(Choice):
    """Change the desired goal to complete the game (Currently only Dialga is implemented)"""
    display_name = "Goal"
    option_dialga = 50
    option_darkrai = 0
    default = 0


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


class StartWithBag(Toggle):
    """Start with bag? If False all bag upgrades will be randomized in the game"""
    display_name = "Start with Bag?"

@dataclass
class EOSOptions(PerGameCommonOptions):
    dungeon_rando: DungeonNameRandomizer
    goal: Goal
    recruit: Recruitment
    recruit_evo: RecruitmentEvolution
    team_form: FullTeamFormationControl
    level_scale: LevelScaling
    bag_on_start: StartWithBag
