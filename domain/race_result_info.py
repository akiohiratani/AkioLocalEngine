from dataclasses import dataclass

@dataclass
class RaceResultInfoDto:
    rank: str            # 着順
    frame_number: str    # 枠番
    horse_number: str    # 馬番
    horse_name: str      # 馬名
    sex_age: str         # 性齢
    fathder: str         # 父
    grandfather: str     # 母父
    weight_carried: str  # 斤量
    jockey: str          # 騎手
    time: str            # タイム
    margin: str          # 着差
    passing: str         # 通過
    last_3f: str         # 上り
    odds: str            # 単勝
    popularity: str      # 人気
    horse_weight: str    # 馬体重
