from dataclasses import dataclass

@dataclass
class JocekeyHistoryDto:
    date: str                      # 日付
    venue: str                     # 開催
    weather: str                   # 天気
    race_number: str               # レース番号
    race_name: str                 # レース名
    race_url: str                  # レースURL
    movie_link:str                 # 映像リンク
    horses_count: str              # 出走頭数
    frame_number: str              # 枠番
    horse_number: str              # 馬番
    odds: str                      # 単勝オッズ
    popularity: str                # 人気順
    order_of_finish: str           # 着順
    horse_name: str                # 馬名
    horse_url: str                 # 馬URL
    weight: str                    # 斤量
    distance: str                  # 距離
    track_condition: str           # 馬場状態
    time: str                      # タイム
    margin: str                    # 着差
    passage: str                   # 通過
    pace: str                      # ペース
    final_3f: str                  # 上り
    horse_weight: str              # 馬体重
    winner_horse: str              # 勝ち馬
    winner_url: str                # 勝ち馬URL
    prize_money: str               # 賞金