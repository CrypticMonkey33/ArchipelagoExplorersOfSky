import math
import typing
import os
import json
import pkgutil
import settings
from typing import List, Dict, Set, Any

import worlds.oot
from .Items import (EOSItem, item_table, item_frequencies, item_table_by_id, item_table_by_groups,
                    filler_item_table, filler_item_weights, trap_item_table, trap_item_weights)
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id, expanded_EOS_location_table
from .Options import EOSOptions
from .Rules import set_rules, ready_for_late_game, has_relic_shards
from BaseClasses import Tutorial, ItemClassification, Region, Location, LocationProgressType, Item
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
                       item in item_table.values()}
    location_name_to_id = {location.name: location.id for
                           location in expanded_EOS_location_table}

    required_client_version = (0, 5, 1)
    required_server_version = (0, 5, 1)

    item_name_groups = item_table_by_groups
    disabled_locations: Set[str] = []
    extra_locations_added = 0
    mission_start_id = 1000
    excluded_locations = 0

    def generate_early(self) -> None:
        if self.options.bag_on_start.value:
            item_name = "Bag Upgrade"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.hero_evolution.value:
            item_name = "Hero Evolution"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.recruit_evo.value:
            item_name = "Recruit Evolution"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.dojo_dungeons.value > 0:
            dojo_amount = self.options.dojo_dungeons.value
            dojo_table = item_table_by_groups["Dojo Dungeons"]
            random_open_dungeons = self.random.sample(sorted(dojo_table), k=dojo_amount)
            for item_name in random_open_dungeons:
                self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.recruit.value:
            item_name = "Recruitment"
            self.multiworld.push_precollected(self.create_item(item_name))
        if self.options.team_form.value:
            item_name = "Formation Control"
            self.multiworld.push_precollected(self.create_item(item_name))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        early_dungeons_region = Region("Early Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(early_dungeons_region)

        #early_dungeons_region2 = Region("Early Dungeons2", self.player, self.multiworld)
        #self.multiworld.regions.append(early_dungeons_region2)

        late_dungeons_region = Region("Late Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(late_dungeons_region)

        end_game_region = Region("Boss Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(end_game_region)

        extra_items_region = Region("Extra Items", self.player, self.multiworld)
        self.multiworld.regions.append(extra_items_region)

        rule_dungeons_region = Region("Rule Dungeons", self.player, self.multiworld)
        self.multiworld.regions.append(rule_dungeons_region)

        for location in EOS_location_table:
            if location.name == "Beach Cave":
                menu_region.locations.append(EOSLocation(self.player, location.name,
                                                         location.id, menu_region))
                if "Mission" in location.group:
                    for j in range(self.options.early_mission_checks.value):
                        location_name: str = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        menu_region.locations.append(EOSLocation(self.player, location_name,
                                                                 location_id, menu_region))

                        self.extra_locations_added += 1
                    for j in range(self.options.early_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        menu_region.locations.append(EOSLocation(self.player, location_name,
                                                                 location_id, menu_region))

                        self.extra_locations_added += 1
            elif location.classification == "Free":
                menu_region.locations.append(EOSLocation(self.player, location.name,
                                                         location.id, menu_region))
            elif location.classification in ["EarlyDungeonComplete", "EarlySubX", "Rank"]:
                early_dungeons_region.locations.append(EOSLocation(self.player, location.name,
                                                                   location.id, early_dungeons_region))
                if "Mission" in location.group:
                    for j in range(self.options.early_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        early_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                           location_id, early_dungeons_region))

                        set_rule(self.multiworld.get_location(location_name, self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))
                        self.extra_locations_added += 1

                    for j in range(self.options.early_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        early_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                           location_id, early_dungeons_region))

                        set_rule(self.multiworld.get_location(location_name, self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))
                        self.extra_locations_added += 1

            elif location.classification == "SpecialDungeonComplete":
                early_dungeons_region.locations.append(EOSLocation(self.player, location.name,
                                                                   location.id, early_dungeons_region))

            elif location.classification in ["LateDungeonComplete", "LateSubX"]:
                late_dungeon = EOSLocation(self.player, location.name,
                                           location.id, late_dungeons_region)
                if self.options.goal.value == 0:  # if dialga is the goal, make the location excluded
                    self.excluded_locations += 1
                    continue

                late_dungeons_region.locations.append(late_dungeon)
                if self.options.goal.value == 1 and ("Mission" in location.group):
                    for j in range(self.options.late_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        late_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                          location_id, late_dungeons_region))

                        set_rule(self.multiworld.get_location(f"{location.name} Mission {j + 1}", self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))
                        self.extra_locations_added += 1

                    for j in range(self.options.late_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        late_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                          location_id, late_dungeons_region))

                        set_rule(self.multiworld.get_location(f"{location.name} Outlaw {j + 1}", self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))

                        self.extra_locations_added += 1
            elif (location.classification in ["Manaphy", "SecretRank", "Legendary", "Instrument"]
                  or location.name == "Bag Upgrade 5"):
                late_dungeon = EOSLocation(self.player, location.name,
                                           location.id, late_dungeons_region)
                if self.options.goal.value == 0:  # if dialga is the goal, make the location excluded
                    self.excluded_locations += 1
                    continue
                    #late_dungeon.progress_type = LocationProgressType.EXCLUDED
                    #Manaphy's discovery can only be collected if manaphy is in the game
                    #if location.name == "Manaphy's Discovery":
                    #    continue
                late_dungeons_region.locations.append(late_dungeon)
            elif location.classification == "SpindaDrinkEvent":
                if int(location.name[-2:]) <= self.options.drink_events:
                    menu_region.locations.append(EOSLocation(self.player, location.name,
                                                             location.id, menu_region))
                else:
                    self.excluded_locations += 1
            elif location.classification == "SpindaDrink":
                if int(location.name[-2:]) <= self.options.spinda_drinks:
                    menu_region.locations.append(EOSLocation(self.player, location.name,
                                                             location.id, menu_region))
                else:
                    self.excluded_locations += 1

            elif location.classification == "BossDungeonComplete":
                location_data = EOSLocation(self.player, location.name,
                                            location.id, end_game_region)
                if location.name == "Dark Crater" and self.options.goal.value == 0:
                    location_data.progress_type = LocationProgressType.EXCLUDED

                end_game_region.locations.append(location_data)
                if (self.options.goal.value == 1) and ("Mission" in location.group):
                    for j in range(self.options.late_mission_checks.value):
                        location_name = f"{location.name} Mission {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j
                        late_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                          location_id, late_dungeons_region))

                        set_rule(self.multiworld.get_location(f"{location.name} Mission {j + 1}", self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))
                        self.extra_locations_added += 1

                    for j in range(self.options.late_outlaw_checks.value):
                        location_name = f"{location.name} Outlaw {j + 1}"
                        location_id = location.id + self.mission_start_id + (100 * location.id) + j + 50
                        late_dungeons_region.locations.append(EOSLocation(self.player, location_name,
                                                                          location_id, late_dungeons_region))

                        set_rule(self.multiworld.get_location(f"{location.name} Outlaw {j + 1}", self.player),
                                 lambda state, ln=location.name, p=self.player: state.has(ln, p))

                        self.extra_locations_added += 1
            elif ((location.classification == "ProgressiveBagUpgrade") or (location.classification == "ShopItem")
                  or (location.classification == "DojoDungeonComplete") or (
                          location.classification == "SEDungeonUnlock")):
                extra_items_region.locations.append(EOSLocation(self.player, location.name,
                                                                location.id, extra_items_region))
            elif location.classification in ["RuleDungeonComplete", "OptionalSubX"]:
                if self.options.long_location.value == 0:
                    self.excluded_locations += 1
                    continue
                    #location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    #location.progress_type = LocationProgressType.EXCLUDED
                    #rule_dungeons_region.locations.append(location)
                else:
                    location = EOSLocation(self.player, location.name, location.id, rule_dungeons_region)
                    rule_dungeons_region.locations.append(location)

        menu_region.connect(extra_items_region)

        menu_region.connect(early_dungeons_region)

        early_dungeons_region.connect(late_dungeons_region, "Late Game Door")

        #early_dungeons_region.connect(early_dungeons_region2)

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
        if classification is not None:
            return EOSItem(item_data.name, classification, item_data.id, self.player)
        else:
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
            "ShardFragmentAmount": self.options.required_fragments.value,
            "ExtraShardsAmount": self.options.total_shards.value,
            "EarlyMissionsAmount": self.options.early_mission_checks.value,
            "EarlyOutlawsAmount": self.options.early_outlaw_checks.value,
            "LateMissionsAmount": self.options.late_mission_checks.value,
            "LateOutlawsAmount": self.options.late_outlaw_checks.value,
            "TypeSanity": self.options.type_sanity.value,
            "StarterOption": self.options.starter_option.value,
            "IQScaling": self.options.iq_scaling.value,
            "XPScaling": self.options.xp_scaling.value,
            "RequiredInstruments": self.options.req_instruments.value,
            "ExtraInstruments": self.options.total_instruments.value,
            "HeroEvolution": self.options.hero_evolution.value,
            "Deathlink": self.options.deathlink.value,
            "LegendaryAmount": self.options.legendaries.value,
            "AllowedLegendaries": self.options.allowed_legendaries.value,
            "SkyPeakType": self.options.sky_peak_type.value,
            "SpecialEpisodeSanity": self.options.special_episode_sanity.value,
            "TrapsAllowed": self.options.allow_traps.value,
            "InvisibleTraps": self.options.invisible_traps.value,
            "TrapPercentage": self.options.trap_percent.value,
            "LongLocations": self.options.long_location.value,
            "CursedAegisCave": self.options.cursed_aegis_cave.value,
            "DrinkEvents": self.options.drink_events.value,
            "SpindaDrinks": self.options.spinda_drinks.value,
        }

    def create_items(self) -> None:
        required_items = []
        filler_items = []
        trap_items = []
        trap_weights = []
        instruments = []
        item_weights = []
        if self.options.goal.value == 1:
            instruments_to_add = 0
            if self.options.total_instruments.value < self.options.req_instruments.value:
                instruments_to_add = self.options.req_instruments.value
            else:
                instruments_to_add = self.options.total_instruments.value

            instrument_table = item_table_by_groups["Instrument"]
            instruments = self.random.sample(sorted(instrument_table), instruments_to_add)
            for item in instruments:
                required_items.append(self.create_item(item, ItemClassification.progression_skip_balancing))

        precollected = [item.name for item in self.multiworld.precollected_items[self.player]]
        relics_to_add = 0
        if self.options.required_fragments.value > self.options.total_shards.value:
            relics_to_add = self.options.required_fragments.value
        else:
            relics_to_add = self.options.total_shards.value

        for i in range(relics_to_add):
            required_items.append(self.create_item("Relic Fragment Shard", ItemClassification.progression))

        if self.options.goal == 1:
            required_items.append(self.create_item("Manaphy", ItemClassification.progression))
        else:
            # self.excluded_locations += 1
            test = 0
        if self.options.goal.value == 1 and (
                self.options.legendaries.value > len(self.options.allowed_legendaries.value)):
            for item in self.options.allowed_legendaries.value:
                required_items.append(self.create_item(item, ItemClassification.useful))
        elif self.options.goal.value == 1:
            new_list = self.random.sample(sorted(self.options.allowed_legendaries.value),
                                          self.options.legendaries.value)
            for item in new_list:
                required_items.append(self.create_item(item, ItemClassification.useful))

        for item_name in item_table:
            if (item_name == "Dark Crater") and (self.options.goal.value == 1):
                continue
            if (item_name in precollected) or (item_name in item_frequencies):
                freq = 0
                if item_name in item_frequencies:
                    freq = item_frequencies.get(item_name, 1)

                freq = max(freq - precollected.count(item_name), 0)
                required_items += [self.create_item(item_name) for _ in range(freq)]

            elif item_table[item_name].name in ["Victory", "Relic Fragment Shard"]:
                continue
            elif "Legendary" in item_table[item_name].group:
                continue
            elif "Instrument" in item_table[item_name].group:
                continue
            elif item_table[item_name].classification == ItemClassification.filler:
                if item_name in ["Golden Apple", "Gold Ribbon"]:
                    continue
                filler_items.append(self.create_item(item_name, ItemClassification.filler))

            elif item_table[item_name].classification == ItemClassification.trap:
                trap_items.append(self.create_item(item_name, ItemClassification.trap))

            elif item_table[item_name].classification == ItemClassification.progression:
                classification = ItemClassification.progression
                if (self.options.goal.value == 0) and "LateDungeons" in item_table[item_name].group:
                    continue
                    #classification = ItemClassification.useful

                if "Aegis" in item_table[item_name].group:
                    if self.options.goal.value == 0:
                        #classification = ItemClassification.useful
                        continue
                    else:
                        classification = ItemClassification.progression
                    if self.options.cursed_aegis_cave.value == 0:
                        if item_name == "Progressive Seal":
                            for i in range(3):
                                required_items.append(self.create_item(item_name, classification))
                                continue
                        else:
                            continue
                    else:
                        if item_name == "Progressive Seal":
                            continue
                        else:
                            required_items.append(self.create_item(item_name, classification))
                            continue

                if "SkyPeak" in item_table[item_name].group:
                    if self.options.sky_peak_type.value == 1:
                        if item_name == "Progressive Sky Peak":
                            if self.options.goal.value == 0:
                                continue
                                #classification = ItemClassification.useful
                            else:
                                classification = ItemClassification.progression
                            for i in range(10):
                                required_items.append(self.create_item(item_name, classification))
                            continue
                        else:
                            continue
                    elif self.options.sky_peak_type.value == 2:
                        if item_name == "Progressive Sky Peak":
                            continue
                        else:
                            if self.options.goal.value == 0:
                                #classification = ItemClassification.useful
                                continue
                            else:
                                classification = ItemClassification.progression
                    elif self.options.sky_peak_type.value == 3:
                        if item_name == "1st Station Pass":
                            if self.options.goal.value == 0:
                                continue
                                #classification = ItemClassification.useful
                            else:
                                classification = ItemClassification.progression

                        else:
                            continue

                required_items.append(self.create_item(item_name, classification))


            else:
                required_items.append(self.create_item(item_name, ItemClassification.useful))

        remaining = len(EOS_location_table) + self.extra_locations_added - len(
            required_items) - 1 - self.excluded_locations  # subtracting 1 for the event check

        self.multiworld.itempool += required_items
        item_weights += filler_item_weights
        trap_weights += trap_item_weights
        for i in range(6):
            filler_items += filler_items
            trap_items += trap_items
            item_weights += item_weights
            trap_weights += trap_weights
        if self.options.allow_traps.value in [1, 2]:
            filler_items_toadd = math.ceil(remaining * (100 - self.options.trap_percent) / 100)
            traps_toadd = math.floor(remaining * self.options.trap_percent / 100)
            self.multiworld.itempool += [self.create_item(filler_item.name) for filler_item
                                         in self.random.sample(filler_items, filler_items_toadd, counts=item_weights)]
            self.multiworld.itempool += [self.create_item(trap.name) for trap
                                         in self.random.sample(trap_items, traps_toadd, counts=trap_item_weights)]

        else:
            self.multiworld.itempool += [self.create_item(filler_item.name) for filler_item
                                         in self.random.sample(filler_items, remaining, counts=item_weights)]

    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = EOSProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/archipelago-base.bsdiff"))
        hint_item_list: list[Item] = []
        for i in range(10):
            hint_item_list += [self.multiworld.get_location(f"Shop Item {1 + i}", self.player).item]
        write_tokens(self, patch, hint_item_list)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
