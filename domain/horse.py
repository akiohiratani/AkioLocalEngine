from dataclasses import dataclass, asdict

@dataclass
class HorseDTO:
    id: str
    name: str
    image: str
    sex: str
    birthyear: str
    trainer: str
    sire: str
    mare: str
    bms: str
    owner: str
    breeder: str
    prize: str

    def to_dict(self):
        return asdict(self)
