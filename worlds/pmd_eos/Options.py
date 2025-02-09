import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Toggle, Choice, PerGameCommonOptions, StartInventoryPool, NamedRange, Range


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


class EarlyMissionChecks(NamedRange):
    """ How many Missions per dungeon pre dialga should be checks?
        0 equals missions are not checks"""
    range_start = 0
    range_end = 50
    special_range_names = {
        "off": 0,
        "some": 4,
        "lots": 10,
        "insanity": 50
    }
    default = 4


class LateMissionChecks(NamedRange):
    """ How many Missions per dungeon post-dialga (including Hidden Land
    and Temporal Tower) should be checks? 0 equals missions are not checks"""
    range_start = 0
    range_end = 50
    special_range_names = {
        "off": 0,
        "some": 4,
        "lots": 10,
        "insanity": 50
    }
    default = 4


class EarlyOutlawChecks(NamedRange):
    """ How many outlaws per dungeon pre dialga should be checks?
        0 equals missions are not checks"""
    range_start = 0
    range_end = 50
    special_range_names = {
        "off": 0,
        "some": 2,
        "lots": 10,
        "insanity": 50
    }
    default = 2


class LateOutlawChecks(NamedRange):
    """ How many Missions per dungeon post-dialga (including Hidden Land
    and Temporal Tower) should be checks? 0 equals missions are not checks"""
    range_start = 0
    range_end = 50
    special_range_names = {
        "off": 0,
        "some": 2,
        "lots": 10,
        "insanity": 50
    }
    default = 2


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


class TypeSanity(Toggle):
    """ Allow for your partner to share a type with your main character
    WARNING: The game is not balanced around this, and we have not done anything to change that.
    Use at your own risk
    """
    display_name = "Type Sanity"


class StarterOption(Choice):
    """How would you like your starter and partner to be chosen?
    Vanilla: You do the quiz and are stuck with what the quiz gives you. Choose your partner as normal
    Random: Both your MC and partner will be completely random. This means they can be the same type
            WARNING: game is not balanced for same type team, use at your own risk (until we fix typesanity)
    Override: Do the quiz, but you can override the hero it gives you. Choose your partner as normal
    Choose: Skip the quiz and go straight to choosing your starter and partner"""
    display_name = "Starter Choice Option"
    option_vanilla = 0
    option_name_random = 1
    option_override = 2
    option_choose = 3
    default = 2


class IqScaling(Range):
    """Do you want to scale IQ to gain IQ faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY IQ. USE AT YOUR OWN RISK

    Not currently Implemented
    """

    display_name = "IQ Scaling"
    range_start = 0
    range_end = 15
    default = 1


class XpScaling(Range):
    """Do you want to scale XP to gain XP faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY XP. USE AT YOUR OWN RISK

    Not currently Implemented"""
    display_name = "XP Scaling"
    range_start = 0
    range_end = 15
    default = 1


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
    early_mission_checks: EarlyMissionChecks
    late_mission_checks: LateMissionChecks
    early_outlaw_checks: EarlyOutlawChecks
    late_outlaw_checks: LateOutlawChecks
    type_sanity: TypeSanity
    starter_option: StarterOption
    iq_scaling: IqScaling
    xp_scaling: XpScaling
