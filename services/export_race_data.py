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

# 馬情報クラスのインポート（添付ファイルから）
from domain.race_history import RaceHistoryDto

class ExportRaceData(ExportBase):
    def __init__(self):
        super().__init__()

    def export_horse_data_to_csv(self, race_results: List[RaceHistoryDto]) -> str:
        """
        レース結果データをCSVファイルとして出力する関数
        
        """
        # 出力ディレクトリの作成
        race_df = pd.DataFrame([asdict(result) for result in race_results])
        race_df.to_csv(f"{self.output_dir}/detailed_race_results_from_the_past.csv", index=False, encoding="utf-8-sig")
        
        # 圧縮
        self.compress_output()

        return self.output_path