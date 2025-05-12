from concurrent.futures import ThreadPoolExecutor, as_completed
from services.base_client import BaseClient
from services.horce_client import HorseClient
from typing import List
from domain.race_result_info import RaceResultInfoDto
from services.usecase import Usecase
import re

class RaceResultClient(BaseClient):
    # url
    BASE_URL = "https://db.netkeiba.com/race/{}/"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    def get_race_results(self, ids:List[str])->List[RaceResultInfoDto]:
        # マルチスレッドで馬情報を並列取得
        race_results = []

        # ThreadPoolExecutorで並列処理
        with ThreadPoolExecutor(max_workers=20) as executor:
            # 各馬IDに対してタスクを登録
            future_to_id = {
                executor.submit(self.get_race_result, race_id): race_id
                for race_id in ids
            }
            
            # 完了したタスクから処理
            for future in as_completed(future_to_id):
                race_id = future_to_id[future]
                try:
                    results = future.result()
                    race_results.extend(results)
                except Exception as e:
                    print("馬ID {race_id} の取得に失敗: {str(e)}")
                    continue
        
        return race_results

    # レース結果を取得
    def get_race_result(self, id:str)->List[RaceResultInfoDto]:
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)

        # 日付を取得
        date = ""
        p_smalltxt = soup.find("p", class_="smalltxt")
        if p_smalltxt:
            # 正規表現で日付パターンを抽出
            text = p_smalltxt.get_text(strip=True)
            date_pattern = re.search(r'\d{4}年\d{1,2}月\d{1,2}日', text)
            if date_pattern:
                date = date_pattern.group(0)

        # レース条件の取得
        dl = soup.find("dl", class_="racedata fc")
        span = dl.find('span')

        distance = ""
        weather = ""
        track_condition = ""

        if span:
            text = span.get_text(strip=True)
            # スラッシュで分割
            parts = text.split('/')
            
            # 各情報を抽出
            course = parts[0].strip()  # "芝左1600m"
            weather = parts[1].strip()  # "天候 : 晴"
            turf_condition = parts[2].strip()  # "芝 : 良"

            # クリーンな形式に変換
            # 1. "芝左1600m" → "芝1600m" （「左」を削除）
            distance = course.replace('左', '').replace('右', '')
            
            # 2. "天候 : 晴" → "晴" （「天候 : 」を削除）
            weather = weather.split(':')[-1].strip()
            
            # 3. "芝 : 良" → "良" （「芝 : 」を削除）
            track_condition = turf_condition.split(':')[-1].strip()
        
        # 開催場所
        location = Usecase().get_racecourse_robust(id)
            
        # 結果一覧の取得
        table = soup.find("table", class_="race_table_01 nk_tb_common")
        rows = table.find_all('tr')[1:]  # ヘッダー除外
        results = []
        horse_client = HorseClient()
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 15:
                continue
            try:
                rank = cells[0].text.strip()
                frame_number = cells[1].find('span').text.strip()
                horse_number = cells[2].text.strip()
                horse_name = cells[3].find('a').text.strip()

                # 馬のIDから血統を取得
                horse_href = cells[3].find('a').get("href")
                horse_id = horse_href.split('/')[2]
                blood = horse_client.get_blood(horse_id)
                father = blood.father
                grandfater = blood.grandfather

                sex_age = cells[4].text.strip()
                weight_carried = cells[5].text.strip()
                jockey = cells[6].find('a').text.strip()
                time = cells[7].text.strip()
                margin = cells[8].text.strip()
                passing = cells[10].text.strip()
                last_3f = cells[11].find('span').text.strip() if cells[11].find('span') else cells[11].text.strip()
                odds = cells[12].text.strip()
                popularity = cells[13].find('span').text.strip()
                horse_weight = cells[14].text.strip()

                result = RaceResultInfoDto(
                    type="過去",
                    date=date,
                    rank=rank,
                    frame_number=frame_number,
                    horse_number=horse_number,
                    horse_id=horse_id,
                    horse_name=horse_name,
                    horse_link=f"https://db.netkeiba.com/horse/{horse_id}",
                    sex_age=sex_age,
                    fathder=father,
                    grandfather=grandfater,
                    weight_carried=weight_carried,
                    jockey=jockey,
                    time=time,
                    margin=margin,
                    passing=passing,
                    last_3f=last_3f,
                    odds=odds,
                    popularity=popularity,
                    horse_weight=horse_weight,
                    location=location,
                    distance=distance,
                    weather=weather,
                    track_condition=track_condition
                )
                results.append(result)
            except Exception as e:
                print("Error: {e}")
        return results   