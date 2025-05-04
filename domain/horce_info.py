from dataclasses import dataclass, asdict
from typing import List
from domain.race_history import RaceHistoryDto

@dataclass
class HorseInfoDTO:
    id: str
    name: str
    sex: str
    image: str
    father: str
    grandfather: str
    title: str
    race_historys: List[RaceHistoryDto]
    def to_dict(self):
        return asdict(self)
