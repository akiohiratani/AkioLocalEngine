from typing import Optional
from dataclasses import dataclass

@dataclass
class RaceHistoryDto:
    date: str
    venue: str
    race_number: str
    race_name: str
    distance: str
    horses_count: str
    gate_number: str
    horse_number: str
    weight: str
    jockey: str
    finish_position: str
    time: str
    margin: str
    rise: str
    popularity: str
    odds: str
    horse_weight: str
    pace: str
    track_condition: str
    weather: str
    winner: str