from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from domain.horce_info import HorseInfoDTO
from domain.race_history import RaceHistoryDto
from services.base_client import BaseClient
from bs4 import BeautifulSoup

class HorseClient(BaseClient):
    BASE_URL = "https://db.netkeiba.com/horse/{}"

    def __init__(self):
        super().__init__()

    def get_horses(self, ids: List[str]) -> List[HorseInfoDTO]:
        # マルチスレッドで馬情報を並列取得
        horses = []
        
        # ThreadPoolExecutorで並列処理
        with ThreadPoolExecutor() as executor:
            # 各馬IDに対してタスクを登録
            future_to_id = {
                executor.submit(self.get_horse, horse_id): horse_id
                for horse_id in ids
            }
            
            # 完了したタスクから処理
            for future in as_completed(future_to_id):
                horse_id = future_to_id[future]
                try:
                    horse = future.result()
                    horses.append(horse)
                except Exception as e:
                    print("馬ID {horse_id} の取得に失敗: {str(e)}")
                    continue
        
        return horses

    def get_horse(self, id: str) -> HorseInfoDTO:
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        
        # 馬の基本情報を取得
        ## 例：ヴァルキリーバース 現役　牝3歳
        horse_info = self.get_horse_base_info(soup)

        # 馬の画像URL取得
        image = self.get_horse_image(soup)

        # 馬の血統を取得
        ## 例：父：エピファネイア, 母父：ハーツクライ
        blood = self.get_horse_blood(soup)

        # 馬の主な勝鞍を取得
        title = self.get_horse_title(soup)

        # 戦歴を取得
        historys = self.get_historys(soup)
        
        return HorseInfoDTO(
            id=id,
            name=horse_info["name"],
            sex=horse_info["sex"],
            image=image,
            father=blood["father"],
            grandfather=blood["grandfather"],
            title=title,
            race_historys=historys
        )

    def get_horse_base_info(self, soup: BeautifulSoup):
        horse_info = soup.find("div", class_="horse_title")
        name = horse_info.find("h1").text
        info = horse_info.find("p", class_="txt_01").text
        sex = info.split('\u3000')
        return {"name": name, "sex": sex[1]}

    def get_horse_image(self, soup: BeautifulSoup) -> str:
        main_photo = soup.find(id="HorseMainPhoto")
        return main_photo.get("src") if main_photo else ""

    def get_horse_blood(self, soup: BeautifulSoup):
        blood_table = soup.find("table", class_="blood_table")
        horse_names = [a.text for td in blood_table.find_all("td") if (a := td.find("a"))]
        return {"father": horse_names[0], "grandfather": horse_names[1]}

    def get_horse_title(self, soup: BeautifulSoup):
        horse_info = {}
        prof_table = soup.find("table", class_="db_prof_table")
        for tr in prof_table.find_all('tr'):
            th, td = tr.find('th'), tr.find('td')
            if th and td:
                key = th.get_text(strip=True)
                if key == '主な勝鞍' and (a := td.find('a')):
                    horse_info['title'] = a.get_text(strip=True)
        return horse_info.get("title", "")
    
    def get_historys(self, soup: BeautifulSoup)->List[RaceHistoryDto]:
        results = []
        table = soup.find("table", class_="db_h_race_results nk_tb_common")
        if table:
            for row in table.find_all("tr"):
                cells = row.find_all('td')

                if(len(cells) < 26):
                    continue

                # 主要データの抽出
                date = cells[0].text.strip()
                venue = cells[1].text.strip()
                race_name = cells[4].text.strip()
                weather=cells[2].text.strip()
                race_number=cells[3].text.strip()
                horses_count=cells[6].text.strip()
                gate_number=cells[7].text.strip()
                horse_number=cells[8].text.strip()
                odds=cells[9].text.strip()
                popularity=cells[10].text.strip()
                finish_position=cells[11].text.strip()
                jockey=cells[12].text.strip()
                weight=cells[13].text.strip()
                distance=cells[14].text.strip()
                track_condition=cells[15].text.strip()
                time = cells[17].text.strip()
                margin = cells[18].text.strip()
                pace = cells[21].text.strip()
                horse_weight = cells[23].text.strip()
                winner = cells[26].text.strip()
                rise = cells[22].text.strip()

                # DTOオブジェクトの作成
                results.append(RaceHistoryDto(
                    date=date,
                    venue=venue,
                    weather=weather,
                    race_number=race_number,
                    race_name=race_name,
                    horses_count=horses_count,
                    gate_number=gate_number,
                    horse_number=horse_number,
                    odds=odds,
                    popularity=popularity,
                    finish_position=finish_position,
                    jockey=jockey,
                    weight=weight,
                    distance=distance,
                    track_condition=track_condition,
                    time=time,
                    margin=margin,
                    pace=pace,
                    horse_weight=horse_weight,
                    winner=winner,
                    rise=rise
                ))
            
            return results

