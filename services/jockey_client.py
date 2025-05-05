from concurrent.futures import ThreadPoolExecutor, as_completed
from services.base_client import BaseClient
from typing import List
import re
from output.output import Output
from domain.jockey_history import JocekeyHistoryDto

class JockeyClient(BaseClient):
    # url
    BASE_URL = "https://db.netkeiba.com/jockey/result/recent/{}/"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    def get_jockeys(self, ids: List[str]) -> List[JocekeyHistoryDto]:
        # マルチスレッドでジョッキー情報を並列取得
        jockeys = []
        
        # ThreadPoolExecutorで並列処理
        with ThreadPoolExecutor() as executor:
            # 各馬IDに対してタスクを登録
            future_to_id = {
                executor.submit(self.get_jockey, jockey_id): jockey_id
                for jockey_id in ids
            }
            
            # 完了したタスクから処理
            for future in as_completed(future_to_id):
                jockey_id = future_to_id[future]
                try:
                    jockey = future.result()
                    jockeys.append(jockey)
                except Exception as e:
                    print("馬ID {jockey_id} の取得に失敗: {str(e)}")
                    continue
        
        return jockeys

    def get_jockey(self, id:str):
        ## http://127.0.0.1:5000/api/races/data

        """
        ジョッキーの最近の成績を収集
        """
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        table = soup.find("table", class_="nk_tb_common race_table_01")
        race_results = []
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            try:
                cells = row.find_all('td')
                
                # 各セルからデータを抽出
                date_text, date_link = self.get_link_and_text(cells[0])
                venue_text, venue_link = self.get_link_and_text(cells[1])
                weather = self.get_cell_text(cells[2])
                race_number = self.get_cell_text(cells[3])
                race_name, race_url = self.get_link_and_text(cells[4])
                
                movie_link_cell = cells[5].find('a')
                movie_link = movie_link_cell.get('href') if movie_link_cell else None
                
                horses_count = self.get_cell_text(cells[6])
                frame_number = self.get_cell_text(cells[7])
                horse_number = self.get_cell_text(cells[8])
                odds = self.get_cell_text(cells[9])
                popularity = self.get_cell_text(cells[10])
                order_of_finish = self.get_cell_text(cells[11])
                horse_name, horse_url = self.get_link_and_text(cells[12])
                weight = self.get_cell_text(cells[13])
                distance = self.get_cell_text(cells[14])
                track_condition = self.get_cell_text(cells[15])
                time = self.get_cell_text(cells[16])
                margin = self.get_cell_text(cells[17])
                passage = self.get_cell_text(cells[18])
                pace = self.get_cell_text(cells[19])
                final_3f = self.get_cell_text(cells[20])
                horse_weight = self.get_cell_text(cells[21])
                winner_horse, winner_url = self.get_link_and_text(cells[22])
                prize_money = self.get_cell_text(cells[23])
                
                # DTOオブジェクトを作成
                race_result = JocekeyHistoryDto(
                    date=date_text,
                    venue=venue_text,
                    weather=weather,
                    race_number=race_number,
                    race_name=race_name,
                    race_url=race_url,
                    movie_link=movie_link,
                    horses_count=horses_count,
                    frame_number=frame_number,
                    horse_number=horse_number,
                    odds=odds,
                    popularity=popularity,
                    order_of_finish=order_of_finish,
                    horse_name=horse_name,
                    horse_url=horse_url,
                    weight=weight,
                    distance=distance,
                    track_condition=track_condition,
                    time=time,
                    margin=margin,
                    passage=passage,
                    pace=pace,
                    final_3f=final_3f,
                    horse_weight=horse_weight,
                    winner_horse=winner_horse,
                    winner_url=winner_url,
                    prize_money=prize_money
                )
                
                race_results.append(race_result)
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                continue
        
        return race_results
    

    def clean_text(self, text):
        """テキストから余分な空白や改行を削除"""
        if text is None:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    def get_cell_text(self, cell):
        """セルからテキストを抽出"""
        if cell is None:
            return ""
        return self.clean_text(cell.get_text())

    def get_link_and_text(self, cell):
        """セルからリンクとテキストを抽出"""
        if cell is None:
            return "", None
        
        link_tag = cell.find('a')
        if link_tag:
            text = self.clean_text(link_tag.get_text())
            link = link_tag.get('href')
            return text, link
        else:
            return self.clean_text(cell.get_text()), None

        