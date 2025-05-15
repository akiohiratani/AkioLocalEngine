from dataclasses import dataclass, asdict

@dataclass
class HorseDto:
    number:str
    horse_id:str
    name:str
    sex_age:str
    father:str
    grandfather:str
    carried:str
    jockey_id:str
    jockey:str
    trainer:str

    def to_dict(self):
        return asdict(self)
