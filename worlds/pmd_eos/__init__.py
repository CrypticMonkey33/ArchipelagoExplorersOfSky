import typing
import os
import json
import pkgutil
import settings
from typing import List, Dict, Set, Any
from .Items import EOS_item_table, EOSItem, item_table, item_frequencies
from .Locations import EOS_location_table, EOSLocation
from .Options import EOSOptions
from .Rules import set_rules
from .Regions import EoS_regions
from BaseClasses import Tutorial, ItemClassification, Region, Location
from worlds.AutoWorld import World, WebWorld
from .Client import EoSClient
from .Rom import EOSProcedurePatch, write_tokens


class EOSWeb(WebWorld):
    theme = "ocean"
    game = "Pokemon Mystery Dungeon Explorers of Sky"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A Guide to setting up Explorers of Sky for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CrypticMonkey33", "Chesyon"]
    )]


class EOSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the EoS EU rom"""

        copy_to = "POKEDUN_SORA_C2SP01_00.nds"
        description = "Explorers of Sky (EU) ROM File"
        md5s = ["6735749e060e002efd88e61560e45567"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class EOSWorld(World):
    """
    This is for Pokemon Mystery Dungeon Explorers of Sky, a game where you inhabit a pokemon and explore
    through dungeons, solve quests, and help out other Pokemon in the colony
    """

    game = "Pokemon Mystery Dungeon Explorers of Sky"
    options: EOSOptions
    options_dataclass = EOSOptions
    web = EOSWeb()
    settings: typing.ClassVar[EOSSettings]

    item_name_to_id = {item.name: item.id for
                       item in EOS_item_table}
    location_name_to_id = {location.name: location.id for
                           location in EOS_location_table}
    origin_region_name = "Overworld"

    required_client_version = (0, 5, 1)

    def generate_early(self) -> None:
        test = 0

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Overworld", self.player, self.multiworld)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

        for location in EOS_location_table:
            if location.classification == "DungeonUnlock" or location.classification == "SpecialDungeonUnlock":
                main_region.locations.append(EOSLocation(self.player, location.name, location.id, main_region))
            elif location.classification == "ProgressiveBagUpgrade":
                main_region.locations.append(EOSLocation(self.player, location.name, location.id, main_region))

        boss_region = Region("Boss Room", self.player, self.multiworld)

        boss_region.locations.append(EOSLocation(self.player, "Final Boss", None, boss_region))

        main_region.connect(boss_region)

        self.get_location("Final Boss").place_locked_item(self.create_item("Victory"))

    def create_item(self, name: str, classification: ItemClassification = None) -> EOSItem:
        item_data = item_table[name]
        return EOSItem(item_data.name, item_data.classification, item_data.id, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
        }

    def create_items(self) -> None:
        required_items = []
        filler_items = []
        precollected = [item for item in item_table if item in self.multiworld.precollected_items]

        for item_name in item_table:
            if item_name in item_frequencies:
                freq = item_frequencies.get(item_name, 1)
                if item_name in precollected:
                    freq = max(freq - precollected.count(item_name), 0)
                if self.options.bag_on_start:
                    precollected += [item_name]
                required_items += [self.create_item(item_name) for _ in range(freq)]

            elif item_table[item_name].classification == ItemClassification.filler:
                filler_items.append(self.create_item(item_name, ItemClassification.filler))
            elif item_table[item_name].classification == ItemClassification.useful:
                required_items.append(self.create_item(item_name, ItemClassification.useful))
            elif item_table[item_name].name == "Victory":
                continue
            else:
                required_items.append(self.create_item(item_name, ItemClassification.progression))

        self.multiworld.itempool += required_items

    def set_rules(self) -> None:
        test = 0
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = EOSProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/archipelago-base.bsdiff"))
        write_tokens(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

