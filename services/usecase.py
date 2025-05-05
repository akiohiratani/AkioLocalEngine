import datetime
from typing import List
from domain.race_result_info import RaceResultInfoDto

class Usecase:
    def get_holidays(self):
        """
        今週末の日付情報を返却する
        """
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        weekends = []
        weekdays_jp = ['月', '火', '水', '木', '金', '土', '日']
        for i in range(7):
            current_day = monday + datetime.timedelta(days=i)
            if current_day.weekday() >= 5:  # 土曜(5) or 日曜(6)
                formatted = current_day.strftime("%m/%d") + f"({weekdays_jp[current_day.weekday()]})"
                weekends.append(formatted)
        return weekends
    def get_horse_ids(self, raceResults:List[RaceResultInfoDto]):
        """
        レース結果から出場した馬のIdのリストを返却する
        """
        horse_ids = [raceResult.horse_id for raceResult in raceResults]
        return list(set(horse_ids))
    
    def get_joceky_ids(self, raceResults:List[RaceResultInfoDto]):
        """
        レース結果から出場した騎手のIdのリストを返却する
        """
        jockey_ids = [raceResult.jockey_id for raceResult in raceResults]
        return list(set(jockey_ids))