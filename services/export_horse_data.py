import os
import zipfile
import shutil
import pandas as pd
import numpy as np
import datetime
from pathlib import Path
from dataclasses import asdict
from typing import List

# 馬情報クラスのインポート（添付ファイルから）
from domain.horce_info import HorseInfoDTO
from domain.race_history import RaceHistoryDto

class ExportHorseData:
    def __init__(self):
        # フォルダ名の時刻を確定
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = date_str + "_HorseInfomainon"
        # ダウウンロード先のパス確定
        user_folder = os.path.expanduser("~")
        download_folder = os.path.join(user_folder, "Downloads")
        self.output_path = os.path.join(download_folder, folder_name)
        out_dir = Path(self.output_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = out_dir

    def export_horse_data_to_csv(self, horse_list: List[HorseInfoDTO]) -> str:
        """
        競走馬データをCSVファイルとして出力する関数
        
        """
        # 出力ディレクトリの作成
        
        
        # 1. 基本情報のCSV
        self.export_basic_info(horse_list)
        
        # 2. 予想家向け分析データCSV
        self.export_analysis_data(horse_list)
        
        # 3. レース履歴詳細CSV
        self.export_race_history(horse_list)

        # 4. 圧縮
        self.compress_output()

        return self.output_path

    def export_basic_info(self, horse_list: List[HorseInfoDTO]):
        """基本情報のCSV出力"""
        basic_info_list = []
        for horse in horse_list:
            horse_dict = {
                "id": horse.id,
                "name": horse.name,
                "sex": horse.sex,
                "father": horse.father,
                "grandfather": horse.grandfather,
                "title": horse.title,
                "latest_race": horse.race_historys[0].race_name if horse.race_historys else "",
                "latest_position": horse.race_historys[0].finish_position if horse.race_historys else ""
            }
            basic_info_list.append(horse_dict)
        
        basic_df = pd.DataFrame(basic_info_list)
        basic_df.to_csv(f"{self.output_dir}/horses_basic.csv", index=False, encoding="utf-8-sig")

    def export_analysis_data(self, horse_list: List[HorseInfoDTO]):
        """予想家向け分析データの出力"""
        horse_analysis_list = []
        
        for horse in horse_list:
            race_history = horse.race_historys
            if not race_history:
                continue
                
            # 着順を数値に変換
            positions = []
            for race in race_history:
                try:
                    pos = int(race.finish_position)
                except ValueError:
                    pos = 99
                positions.append(pos)
            
            # 馬場別の成績
            turf_races = [r for r in race_history if '芝' in r.distance]
            dirt_races = [r for r in race_history if 'ダ' in r.distance]
            
            # 馬体重の変化
            weight_changes = []
            for race in race_history:
                weight_str = race.horse_weight
                if "(" in weight_str:
                    change = weight_str.split("(")[1].replace(")", "")
                    try:
                        weight_changes.append(int(change))
                    except ValueError:
                        weight_changes.append(0)
            
            # 各距離帯の成績
            distance_dict = {}
            for race in race_history:
                dist = race.distance
                if dist not in distance_dict:
                    distance_dict[dist] = []
                
                try:
                    pos = int(race.finish_position)
                    distance_dict[dist].append(pos)
                except ValueError:
                    distance_dict[dist].append(99)
            
            # 分析用特徴量の作成
            horse_features = {
                "id": horse.id,
                "name": horse.name,
                "sex": horse.sex,
                "father": horse.father,
                "grandfather": horse.grandfather,
                
                # 平均着順
                "avg_position_3": np.mean(positions[:3]) if len(positions) >= 3 else np.nan,
                "avg_position_5": np.mean(positions[:5]) if len(positions) >= 5 else np.nan,
                "avg_position_all": np.mean(positions),
                
                # 馬場別の平均着順
                "avg_turf_position": np.mean([int(r.finish_position) for r in turf_races if r.finish_position.isdigit()]) if turf_races else np.nan,
                "avg_dirt_position": np.mean([int(r.finish_position) for r in dirt_races if r.finish_position.isdigit()]) if dirt_races else np.nan,
                
                # 1着、2着、3着の回数
                "wins": positions.count(1),
                "seconds": positions.count(2),
                "thirds": positions.count(3),
                
                # 馬体重の平均と変化傾向
                "avg_weight_change": np.mean(weight_changes) if weight_changes else np.nan,
                "latest_weight": race_history[0].horse_weight.split("(")[0] if race_history else "",
                
                # 上がりの平均タイム
                "avg_rise": np.mean([float(r.rise) for r in race_history if r.rise.replace('.', '', 1).isdigit()]),
                
                # 最近の成績
                "recent_results": "-".join([r.finish_position for r in race_history[:5]])
            }
            
            # 各距離帯の平均着順を追加
            for dist, positions in distance_dict.items():
                dist_key = f"avg_position_{dist}"
                horse_features[dist_key] = np.mean(positions)
            
            horse_analysis_list.append(horse_features)
        
        analysis_df = pd.DataFrame(horse_analysis_list)
        analysis_df.to_csv(f"{self.output_dir}/horses_analysis.csv", index=False, encoding="utf-8-sig")

    def export_race_history(self, horse_list: List[HorseInfoDTO]):
        """レース履歴詳細のCSV出力"""
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
    
    def compress_output(self):
        zip_path = self.output_dir.parent / f'{self.output_dir.name}.zip'
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.output_dir.glob('*'):
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)

        # 圧縮が終わったら元フォルダを削除
        shutil.rmtree(self.output_dir)
