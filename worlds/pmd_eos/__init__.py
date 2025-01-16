import typing
import os
import json
from .Items import EOS_item_table
from .Locations import EOS_location_table, EOSLocation
from .Options import EOSOptions
from .Rules import set_rules
from .Regions import EoS_regions
from BaseClasses import Item, Tutorial, ItemClassification, Region, Location
from ..AutoWorld import World, WebWorld


class EOSWeb(WebWorld):
    theme = "ocean"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A Guide to setting up Explorers of Sky for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CrypticMonkey33"]
    )]


class EOSItem(Item):
    game: str = "Explorers of Sky"


class EOSLocation(Location):
    game: str = "Explorers of Sky"


class EOSWorld(World):
    """
    This is for Pokemon Mystery Dungeon Explorers of Sky, a game where you inhabit a pokemon and explore through dungeons,
    solve quests, and help out other Pokemon in the colony
    """

    game = "Explorers Of Sky"
    options: EOSOptions

#    web = EOSWeb

    item_name_to_id = {name: id for
                       id, name in EOS_item_table}
    location_name_to_id = {name:id for
                           id, name in EOS_location_table}

#    item_name_groups = {
#
#    }
#
#    location_name_groups={
#
#    }

    required_client_version = (0, 0, 0)

    options_dataclass = EOSOptions

    def generate_early(self) -> None:
        test = 0

    def create_regions(self) -> None:
        main_region = Region("Overworld", self.player, self.multiworld)
        self.multiworld.regions.append(main_region)

        for location in EOS_location_table:
            main_region.locations.append(EOSLocation(self.player, location.name, location.id,main_region))

        boss_region = Region("Boss Room", self.player, self.multiworld)

        boss_region.locations.append(EOSLocation(self.player, "Final Boss", None, boss_region))

        main_region.connect(boss_region)
#        test = 0

    def create_items(self) -> None:
        test = 0

    def set_rules(self) -> None:
        test = 0

    def generate_basic(self):
        test = 0


