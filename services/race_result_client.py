from concurrent.futures import ThreadPoolExecutor, as_completed
from services.base_client import BaseClient
from typing import List
import re
from domain.race_result_info import RaceResultInfoDto
from output.output import Output

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
        Output().outputTableForClass(soup, "race_table_01 nk_tb_common")
        table = soup.find("table", class_="race_table_01 nk_tb_common")
        rows = table.find_all('tr')[1:]  # ヘッダー除外
        results = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 15:
                continue
            try:
                rank = cells[0].text.strip()
                frame_number = cells[1].find('span').text.strip()
                horse_number = cells[2].text.strip()
                horse_name = cells[3].find('a').text.strip()
                sex_age = cells[4].text.strip()
                weight_carried = cells[5].text.strip()
                jockey = cells[6].find('a').text.strip()
                time = cells[7].text.strip()
                margin = cells[8].text.strip()
                time_index = cells[9].text.strip()  # プレミアム会員でない場合は「**」等
                passing = cells[10].text.strip()
                last_3f = cells[11].find('span').text.strip() if cells[11].find('span') else cells[11].text.strip()
                odds = cells[12].text.strip()
                popularity = cells[13].find('span').text.strip()
                horse_weight = cells[14].text.strip()

                result = RaceResultInfoDto(
                    rank=rank,
                    frame_number=frame_number,
                    horse_number=horse_number,
                    horse_name=horse_name,
                    sex_age=sex_age,
                    weight_carried=weight_carried,
                    jockey=jockey,
                    time=time,
                    margin=margin,
                    time_index=time_index,
                    passing=passing,
                    last_3f=last_3f,
                    odds=odds,
                    popularity=popularity,
                    horse_weight=horse_weight
                )
                results.append(result)
            except Exception as e:
                print("Error: {e}")
        return results   