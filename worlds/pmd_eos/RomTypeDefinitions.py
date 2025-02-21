from typing import List, NamedTuple


class SubXBitfield (NamedTuple):
    bitfield_bit_number: int
    subX_area: int
    subX_bit_number: int
    flag_definition: str  # name
    prerequisites: List[str]
    default_item: str  # what item is normally there?

subX_table = [
    SubXBitfield(0, 1, 0, "Bag Upgrade 0", ["Clear Beach Cave"], "Bag Upgrade"),

]