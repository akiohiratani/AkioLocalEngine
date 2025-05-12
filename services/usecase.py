import datetime
from typing import List

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
    
    def get_racecourse_robust(self, race_id):
        """
        レースIDから競馬場を特定する関数
        """
        try:
            # 数値や他の型を文字列に変換
            race_id_str = str(race_id).strip()
            
            # 文字列が数字のみで構成されているか確認
            if not race_id_str.isdigit():
                return ""
            
            # IDの長さをチェック
            if len(race_id_str) < 12:
                return ""
            
            # 競馬場コードを抽出
            course_code = race_id_str[4:6]
            
            # 競馬場コードと競馬場名の対応表（拡張版）
            racecourse_dict = {
                "01": "札幌",
                "02": "函館",
                "03": "福島",
                "04": "新潟",
                "05": "東京",
                "06": "中山",
                "07": "中京",
                "08": "京都",
                "09": "阪神",
                "10": "小倉",
                # 以下は追加情報があれば拡張できます
                # "11": "その他競馬場1",
                # "12": "その他競馬場2",
            }
            
            # 対応表から競馬場名を取得、不明な場合はコードも表示
            return racecourse_dict.get(course_code)
        
        except Exception as e:
            return ""