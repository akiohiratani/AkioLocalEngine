from dataclasses import dataclass

@dataclass
class RaceResultInfoDto:
    type: str            # 過去/未来
    date:str             # 日付
    location: str        # 開催
    distance: str        # 距離
    horse_id: str        # 馬ID
    horse_name: str      # 馬名
    horse_link: str      # 馬Link
    sex_age: str         # 性齢
    fathder: str         # 父
    grandfather: str     # 母父
    frame_number: str    # 枠番
    horse_number: str    # 馬番
    weight_carried: str  # 斤量
    jockey: str          # 騎手
    rank: str            # 着順
    time: str            # タイム
    margin: str          # 着差
    last_3f: str         # 上り
    popularity: str      # 人気
    odds: str            # オッズ
    horse_weight: str    # 馬体重
    passing: str         # 通過
    track_condition: str # 馬場状態
    weather: str         # 天気