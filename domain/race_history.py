from typing import Optional
from dataclasses import dataclass

@dataclass
class RaceHistoryDto:
    date: str
    venue: str
    weather: str
    race_number: str
    race_name: str
    horses_count: str
    gate_number: str
    horse_number: str
    odds: str
    popularity: str
    finish_position: str
    jockey: str
    weight: str
    distance: str
    track_condition: str
    time: str
    margin: str
    pace: str
    horse_weight: str
    winner: str
    rise: str