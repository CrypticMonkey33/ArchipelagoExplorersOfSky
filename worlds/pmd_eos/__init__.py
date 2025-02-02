import typing
import os
import json
import pkgutil
import settings
from typing import List, Dict, Set, Any

import worlds.oot
from .Items import EOS_item_table, EOSItem, item_table, item_frequencies, item_table_by_id, item_table_by_groups
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id
from .Options import EOSOptions
from .Rules import set_rules, ready_for_late_game, ready_for_dialga
from .Regions import EoS_regions
from BaseClasses import Tutorial, ItemClassification, Region, Location
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, forbid_item
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

    required_client_version = (0, 5, 1)
    required_server_version = (0, 5, 1)

    item_name_groups = item_table_by_groups
    disabled_locations: Set[str] = []

    def generate_early(self) -> None:
        if self.options.bag_on_start.value:
            item_name = "Bag Upgrade"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.dojo_dungeons.value > 0:
            dojo_amount = self.options.dojo_dungeons.value
            dojo_table = item_table_by_groups["Dojo Dungeons"]
            random_open_dungeons = self.random.sample(sorted(dojo_table), k=dojo_amount)
            for item_name in random_open_dungeons:
                self.multiworld.push_precollected(self.create_item(item_name))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        early_dungeons_region = Region("Early Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(early_dungeons_region)

        late_dungeons_region = Region("Late Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(late_dungeons_region)

        end_game_region = Region("Boss Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(end_game_region)

        extra_items_region = Region("Extra Items", self.player,self.multiworld)
        self.multiworld.regions.append(extra_items_region)

        rule_dungeons_region = Region("Rule Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(rule_dungeons_region)

        for location in EOS_location_table:
            if (location.name == "Beach Cave") or (location.name == "Progressive Bag loc 1"):
                menu_region.locations.append(EOSLocation(self.player, location.name,
                                                         location.id, menu_region))
            elif ((location.classification == "EarlyDungeonComplete")
                  or (location.classification == "SpecialDungeonComplete")):
                early_dungeons_region.locations.append(EOSLocation(self.player, location.name,
                                                                   location.id, early_dungeons_region))
            elif location.classification == "LateDungeonComplete":
                late_dungeons_region.locations.append(EOSLocation(self.player, location.name,
                                                                  location.id, late_dungeons_region))
            elif location.classification == "BossDungeonComplete":
                end_game_region.locations.append(EOSLocation(self.player, location.name,
                                                             location.id, end_game_region))
            elif ((location.classification == "ProgressiveBagUpgrade") or (location.classification == "ShopItem")
                  or (location.classification == "DojoDungeonComplete") or (location.classification == "SEDungeonUnlock")):
                extra_items_region.locations.append(EOSLocation(self.player, location.name,
                                                                location.id, extra_items_region))
            elif location.classification == "RuleDungeonComplete":
                rule_dungeons_region.locations.append(EOSLocation(self.player, location.name,
                                                                  location.id, rule_dungeons_region))

        menu_region.connect(extra_items_region)

        menu_region.connect(early_dungeons_region)

        early_dungeons_region.connect(late_dungeons_region, "Late Game Door",
                                      lambda state: ready_for_late_game(state, self.player))

        late_dungeons_region.connect(end_game_region, "Boss Door")
                                     #lambda state: ready_for_final_boss(state, self.player))

        boss_region = Region("Boss Room", self.player, self.multiworld)

        boss_region.locations.append(EOSLocation(self.player, "Final Boss", None, boss_region))

        end_game_region.connect(boss_region, "End Game")
                                #lambda state: state.has("Temporal Tower", self.player))
        late_dungeons_region.connect(rule_dungeons_region, "Rule Dungeons")

        self.get_location("Final Boss").place_locked_item(self.create_item("Victory"))

    def create_item(self, name: str, classification: ItemClassification = None) -> EOSItem:
        item_data = item_table[name]
        return EOSItem(item_data.name, item_data.classification, item_data.id, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "Goal": self.options.goal.value,
            "BagOnStart": self.options.bag_on_start.value,
            "Recruitment": self.options.recruit.value,
            "TeamFormation": self.options.team_form.value,
            "LevelScaling": self.options.level_scale.value,
            "RecruitmentEvolution": self.options.recruit_evo.value,
            "DojoDungeonsRandomization": self.options.dojo_dungeons.value,
            "ShardFragmentAmount": self.options.shard_fragments.value,
        }

    def create_items(self) -> None:
        required_items = []
        filler_items = []

        precollected = [item.name for item in self.multiworld.precollected_items[self.player]]
        for i in range(self.options.shard_fragments.value + self.options.extra_shards.value):
            required_items.append(self.create_item("Relic Fragment Shard", ItemClassification.progression))

        if self.options.goal == 1:
            required_items.append(self.create_item("Cresselia Feather", ItemClassification.progression))

        for item_name in item_table:
            if (item_name == "Dark Crater") and (self.options.goal.value == 1):
                continue
            if (item_name in precollected) or (item_name in item_frequencies):
                freq = 0
                if item_name in item_frequencies:
                    freq = item_frequencies.get(item_name, 1)

                freq = max(freq - precollected.count(item_name), 0)
                required_items += [self.create_item(item_name) for _ in range(freq)]

            elif item_table[item_name].name in ["Victory", "Relic Fragment Shard", "Cresselia Feather"]:
                continue

            elif item_table[item_name].classification == ItemClassification.filler:
                if item_name in ["Golden Apple", "Gold Ribbon"]:
                    continue
                filler_items.append(self.create_item(item_name, ItemClassification.filler))

            elif item_table[item_name].classification == ItemClassification.trap:
                filler_items.append(self.create_item(item_name, ItemClassification.trap))

            elif item_table[item_name].classification == ItemClassification.progression:
                required_items.append(self.create_item(item_name, ItemClassification.progression))

            else:
                required_items.append(self.create_item(item_name, ItemClassification.useful))

        remaining = len(EOS_location_table) - len(required_items) - 1  # subtracting 1 for the event check

        self.multiworld.itempool += required_items
        for i in range(5):
            filler_items += filler_items
        self.multiworld.itempool += [self.create_item(filler_item.name) for filler_item
                                     in self.random.sample(filler_items, remaining)]

    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = EOSProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/archipelago-base.bsdiff"))
        write_tokens(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

