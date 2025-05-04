from dataclasses import dataclass, asdict

@dataclass
class RaceInfoDTO:
    id: str
    name: str
    place: str
    date: str
    distance: str

    def to_dict(self):
        return asdict(self)