
from typing import List, NamedTuple

common_weight = 20
uncommon_weight = 10
rare_weight = 5
ultra_rare_weight = 1


class DeathMessages(NamedTuple):
    death_string: str = ""
    message_weight: int = 0


death_message_list = [
    DeathMessages(" was defeated by Lappy's silliness", ultra_rare_weight),
    DeathMessages(" got YOOM-TAH'd", uncommon_weight),
    DeathMessages(" got on Chatot's Bad Side", uncommon_weight),
    DeathMessages(" tried (and failed) to steal from Kecleon", rare_weight),
    DeathMessages(" drowned in the C of Time", rare_weight),
    DeathMessages(" drowned in the Sea of Time", uncommon_weight),
    DeathMessages(" was done in by a monster house", common_weight),
    DeathMessages(" couldn't move diagonally", uncommon_weight),
    DeathMessages(" was done in by a Chestnut Trap whilst fighting a monster house", uncommon_weight),
    DeathMessages(" fell asleep during Sentry Duty", uncommon_weight),
    DeathMessages(" died from a Wonder Tile", rare_weight),
    DeathMessages(" was transformed into a Spoink and stopped bouncing!", rare_weight),
    DeathMessages(" ran out of Reviver Seeds", common_weight),
]

death_message_weights = [message.message_weight for message in death_message_list]