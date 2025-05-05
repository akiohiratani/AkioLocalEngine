import os
import zipfile
import shutil
import pandas as pd
import numpy as np
import datetime
from pathlib import Path
from dataclasses import asdict
from typing import List
from services.base.base_export import ExportBase
from domain.horce_info import HorseInfoDTO

# 馬情報クラスのインポート（添付ファイルから）
from domain.race_history import RaceHistoryDto

class ExportRaceData(ExportBase):
    def __init__(self):
        super().__init__()

    def export_past_race_data_to_csv(self, race_results: List[RaceHistoryDto]) -> str:
        """
        レース結果データをCSVファイルとして出力する関数
        
        """
        # 出力ディレクトリの作成
        race_df = pd.DataFrame([asdict(result) for result in race_results])
        race_df.to_csv(f"{self.output_dir}/detailed_race_results_from_the_past.csv", index=False, encoding="utf-8-sig")

        return self.output_path
    
    def export_horse_history(self, horse_list: List[HorseInfoDTO]):
        """競走馬のレース履歴詳細のCSV出力"""
        race_records = []
        
        for horse in horse_list:
            for race in horse.race_historys:
                race_dict = asdict(race)
                # 先頭に馬の識別情報を追加
                race_dict = {
                    "horse_id": horse.id,
                    "horse_name": horse.name,
                    "horse_sex": horse.sex,
                    "horse_father": horse.father,
                    "horse_grandfather": horse.grandfather,
                    **race_dict  # レース情報を後ろに展開
                }
                race_records.append(race_dict)
        race_df = pd.DataFrame(race_records)
        # カラム順を明示的に指定（必要に応じて調整）
        cols = [
            "horse_id", "horse_name", "horse_sex", "horse_father", "horse_grandfather"
        ] + [c for c in race_df.columns if c not in ("horse_id", "horse_name", "horse_sex", "horse_father", "horse_grandfather")]
        race_df = race_df[cols]
        race_df.to_csv(f"{self.output_dir}/race_history_details.csv", index=False, encoding="utf-8-sig")

        return self.output_path