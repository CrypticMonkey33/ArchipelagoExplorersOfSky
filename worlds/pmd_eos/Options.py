import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Toggle, Choice, PerGameCommonOptions, StartInventoryPool, NamedRange, Range, \
    DeathLink, OptionSet


class DungeonNameRandomizer(DefaultOnToggle):
    """NOT IMPLEMENTED YET
    Randomizes the names of the dungeons. IDs and completion requirements stay the same"""
    display_name = "Dungeon Name Randomization"


class Goal(Choice):
    """Change the desired goal to complete the game
    Dialga - Get X relic fragment shards to unlock hidden land. Find Temporal Tower location
            then go through hidden land via Lapras on the beach to beat dialga
    Darkrai - Beat Dialga (all the same requirements), then get X instruments to unlock Dark Crater"""
    display_name = "Goal"
    option_dialga = 0
    option_darkrai = 1
    default = 0


class FragmentShards(NamedRange):
    """ How many Relic Fragment Shards should be in the game (Macguffins)
     that you must get to unlock Hidden Land"""
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


class AllowedLegendaries(OptionSet):
    """ Set which Legendaries will be available for the item pool as recruits
    """
    display_name = "Allowed Legendary Recruits"
    valid_keys = [
        "Regirock",
        "Regice",
        "Registeel",
        "Groudon",
        "Uxie",
        "Mespirit",
        "Azelf",
        "Dialga",
        "Palkia",
        "Regigigas",
        "Giratina",
        "Celebi",
        "Articuno",
        "Heatran",
        "Primal Dialga",
        "Mew",
        "Phione",
        "Cresselia",
        "Rayquaza",
        "Kyogre",
        "Shaymin",
    ]
    default = valid_keys.copy()


class RequiredInstruments(NamedRange):
    """ How many Instruments should be in the game (Macguffins)
     that you must get to unlock Dark Crater if victory condition is Darkrai
     Instruments are not added to the item pool if the goal is Dialga"""
    range_start = 4
    range_end = 10
    special_range_names = {
        "easy": 4,
        "normal": 6,
        "hard": 8,
        "extreme": 10
    }
    default = 6


class ExtraInstruments(NamedRange):
    """ How many extra Instruments should be in the game?"""
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
        0 equals outlaws are not checks"""
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
    and Temporal Tower) should be checks? 0 equals outlaws are not checks"""
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
    """Start with recruitment enabled?
    If false, recruitment will be an item available in game"""
    display_name = "Recruitment Enable"


class RecruitmentEvolution(DefaultOnToggle):
    """Start with Recruitment Evolution Enabled?
    If false, evolution will be an item available in game"""
    display_name = "Recruitment Evolution Enable"


class HeroEvolution(DefaultOnToggle):
    """Start with Hero/Partner Evolution Enabled?
    If false, hero evolution will be an item available in game.
    Note: hero evolution does nothing until recruitment
    evolution has been unlocked"""
    display_name = "Partner/Hero Evolution Enable"


class FullTeamFormationControl(DefaultOnToggle):
    """ Start with full team formation control?
    If false, full team formation control will be an item
    available in game"""
    display_name = "Formation Control Enable"


class LevelScaling(DefaultOnToggle):
    """Allow for dungeons to scale to the highest level of your party members?
    This will not scale bosses at the end of dungeons"""
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
    Choose: Skip the quiz and go straight to choosing your starter and partner
    For both Choose and Override you will be able to pick partner exclusive pokemon for your starter as well as gender
    exclusive pokemon regardless of gender"""
    display_name = "Starter Choice Option"
    option_vanilla = 0
    option_random_starter = 1
    option_override = 2
    option_choose = 3
    default = 2


class IqScaling(Range):
    """Do you want to scale IQ to gain IQ faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY IQ. USE AT YOUR OWN RISK
    """

    display_name = "IQ Scaling"
    range_start = 0
    range_end = 15
    default = 1


class XpScaling(Range):
    """Do you want to scale XP to gain XP faster? What rate? (1x, 2x, 3x, etc.)
    WARNING: 0x WILL NOT GIVE YOU ANY XP. USE AT YOUR OWN RISK

    NOT CURRENTLY IMPLEMENTED

    """

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


class LegendariesInPool(Range):
    """How many Legendary Pokemon should be in the item pool for you to recruit?
        The Legendary will only come post-dialga if you get it early
        Legendaries are disabled if you are going for a dialga goal
        """

    display_name = "Legendaries in Item Pool"
    range_start = 0
    range_end = 21
    default = 3


class DeathlinkType(Toggle):
    """What type of deathlink do you want?
    Currently False is death even if you have revival seeds
    True will die and recover from revival seeds"""

    display_name = "Deathlink Type"


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
    req_instruments: RequiredInstruments
    extra_instruments: ExtraInstruments
    hero_evolution: HeroEvolution
    deathlink: DeathLink
    deathlink_type: DeathlinkType
    legendaries: LegendariesInPool
    allowed_legendaries: AllowedLegendaries

