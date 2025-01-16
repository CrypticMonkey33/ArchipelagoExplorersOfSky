from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_rule, forbid_item
from .Locations import EOS_location_table, EOSLocation
from .Options import EOSOptions

if TYPE_CHECKING:
    from . import EOSWorld


def ready_for_final_boss():
    return True


def set_rules(world: "EosWorld"):
    player = world.player
    options = world.options

    set_rule(world.get_location("Temporal Tower1"),
             lambda state: ready_for_final_boss())