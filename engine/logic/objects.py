from dataclasses import dataclass, field

@dataclass
class Stat:

    stat_name: str

    min_stat: int
    max_stat: int
    stat_value: int
    modification_state: str

    rune_tier1: int
    rune_tier2: int
    rune_tier3: int

    row_name: str

@dataclass
class Item:
    item_type: str
    mage_type: str
    sink: int

    stats: list[Stat] = field(default_factory=list)