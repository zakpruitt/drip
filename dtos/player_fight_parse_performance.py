from dataclasses import dataclass

from dtos.performance_type import PerformanceType


@dataclass
class PlayerFightParsePerformance:
    name: str
    player_class: str
    player_spec: str
    rank_percent: float
    amount: float
    performance_type: PerformanceType
