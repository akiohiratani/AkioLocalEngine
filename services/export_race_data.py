import pandas as pd
from dataclasses import asdict
from typing import List
from services.base.base_export import ExportBase
from domain.horce_info import HorseInfoDTO
from services.base.dataset_type import DatasetType
from domain.race_result_info import RaceResultInfoDto

class ExportRaceData(ExportBase):
    def __init__(self):
        super().__init__()

    def export_past_race_data_to_csv(self, file_name:str, race_results: List[RaceResultInfoDto]) -> str:
        """
        レース結果データをCSVファイルとして出力する関数
        
        """
        # 出力ディレクトリの作成
        race_df = pd.DataFrame([asdict(result) for result in race_results])

        column_mapping = {
            'type':'データ種別',
            'date':'日付',
            'rank':'着順',
            'frame_number' : '枠番',
            'horse_number' : '馬番',
            'horse_id': '馬ID',
            'horse_name': '馬名',
            'horse_link': '馬リンク',
            'sex_age': '性齢',
            'fathder': '父',
            'grandfather': '母父',
            'weight_carried' : '斤量',
            'jockey' : '騎手',
            'time' : 'タイム',
            'margin' : '着差',
            'passing' : 'ペース',
            'last_3f' : "上がり3F",
            'odds' : 'オッズ',
            'popularity' : '人気',
            'horse_weight' : '馬体重',
            'location' : '開催場所',
            'distance' : '距離',
            'weather' : '天気',
            'track_condition' : '馬場状態',
        }
        race_df.rename(columns=column_mapping, inplace=True)

        # 日付として解釈されやすい列のリスト
        date_like_columns = ['ペース', '着差', '通過']
        
        # これらの列に対して処理を行う
        for col in date_like_columns:
            if col in race_df.columns:
                # NaN値を処理
                race_df[col] = race_df[col].fillna('')
                # 文字列に変換して先頭にタブを付ける
                race_df[col] = "'" + race_df[col].astype(str)

        race_df.to_csv(f"{self.output_dir}/{file_name}.csv", index=False, encoding="utf-8-sig")
        return
    
    def export_horse_history(self, file_name:str, horse_list: List[HorseInfoDTO]):
        """競走馬のレース履歴詳細のCSV出力"""
        race_records = []
        
        for horse in horse_list:
            for race in horse.race_historys:
                race_dict = asdict(race)
                # 先頭に馬の識別情報を追加
                race_dict = {
                    "horse_id": horse.id,
                    "horse_name": horse.name,
                    "horse_link": horse.link,
                    "horse_sex": horse.sex,
                    "horse_father": horse.father,
                    "horse_grandfather": horse.grandfather,
                    **race_dict  # レース情報を後ろに展開
                }
                race_records.append(race_dict)
        race_df = pd.DataFrame(race_records)
        # カラム順を明示的に指定（必要に応じて調整）
        cols = [
            "horse_id", "horse_name", "horse_link", "horse_sex", "horse_father", "horse_grandfather"
        ] + [c for c in race_df.columns if c not in ("horse_id", "horse_name", "horse_link", "horse_sex", "horse_father", "horse_grandfather")]
        race_df = race_df[cols]

        column_mapping = {
            'horse_id': '馬ID',
            'horse_name': '馬名',
            'horse_link': '馬リンク',
            'horse_sex': '性齢',
            'horse_father': '父',
            'horse_grandfather': '母父',
            'date': '日付',
            'venue': '開催場所',
            'weather': '天気',
            'race_number': 'レース番号',
            'race_name' : 'レース名',
            'horses_count': '出走数',
            'gate_number' : '枠番',
            'horse_number' : '馬番',
            'odds' : 'オッズ',
            'popularity' : '人気',
            'finish_position' : '着順',
            'jockey' : '騎手',
            'weight' : '斤量',
            'distance' : '距離',
            'track_condition' : '馬場状態',
            'time' : 'タイム',
            'margin' : '着差',
            'pace' : 'ペース',
            'horse_weight' : '馬体重',
            'winner' : '勝ち馬',
            'rise' : "上がり3F"
        }
        race_df.rename(columns=column_mapping, inplace=True)

        race_df.to_csv(f"{self.output_dir}/{file_name}.csv", index=False, encoding="utf-8-sig")
        return