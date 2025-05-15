from services.base_client import BaseClient
from typing import List
import re
from domain.race_result_info import RaceResultInfoDto
from services.horce_client import HorseClient
from services.usecase import Usecase

class RaceClient(BaseClient):
    # url
    BASE_URL = "https://race.netkeiba.com/race/shutuba.html?race_id={}&rf=race_list"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # 競走馬の情報を取得
    def get_horse_ids(self, id:str)->List[str]:
        """
        レースIdから、競走馬のIdを取得
        
        """
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)

        # 馬名リンク（<td class="HorseInfo">内の<a href=.../horse/数字10桁>）を全て取得
        horse_links = soup.select("td.HorseInfo .HorseName a[href*='/horse/']")
        horse_ids = []
        for horse_link in horse_links:
            # href属性からid（10桁の数字）を正規表現で抽出
            m = re.search(r'/horse/(\d{10})', horse_link['href'])
            if m:
                horse_ids.append(m.group(1))
        return horse_ids
    
    def get_jockey_ids(self, id:str)->List[str]:
        """
        レースIdから、ジョッキーのIdを取得
        
        """
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)

        # 馬名リンク（<td class="Jockey">内の<a href=.../jockey/result/recent/数字5桁>）を全て取得
        jockey_links = soup.select("td.Jockey a[href*='/jockey/result/recent/']")
        jockey_ids = []
        for jockey_link in jockey_links:
            # href属性からid（5桁の数字）を正規表現で抽出
            m = re.search(r'/horse/(\d{5})', jockey_link['href'])
            if m:
                jockey_ids.append(m.group(1))
        return jockey_ids

    def get_candidate_list(self, id:str)->List[RaceResultInfoDto]:
        horse_clinet = HorseClient()
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)

        # レースの基本情報を取得
        base_race_info = soup.find("div", class_="RaceData01")

        ## 1. 距離情報: 芝1600m の取得
        distance = ""
        distance_span = base_race_info.find('span')
        if distance_span:
            distance = distance_span.get_text(strip=True)

        ## 2. 天気情報: 晴 の取得
        # div全体のテキストを取得
        weather = ""
        full_text = distance_span.get_text()
        weather_match = re.search(r'天候:([^/]+)', full_text)
        if weather_match:
            weather = weather_match.group(1).strip()

        # 3. 馬場状態: 良 の取得
        track_condition = ""
        track_match = re.search(r'馬場:([^/]+)', full_text)
        if track_match:
            track_condition = track_match.group(1).strip()

        # 開催場所を取得
        location = Usecase().get_racecourse_robust(id)

        ## 出走馬の情報を取得
        table = soup.find("table", class_="Shutuba_Table RaceTable01 ShutubaTable")
        # 馬情報が含まれる行を全て取得
        rows = table.find_all('tr', class_='HorseList')        
        horse_list = []
        for tr in rows:
            # 馬番を取得
            number = ""
            number_cell = tr.find('td', class_=['Umaban1 Txt_C', 'Umaban2 Txt_C', 'Umaban3 Txt_C', 'Umaban4 Txt_C', 'Umaban5 Txt_C', 'Umaban6 Txt_C', 'Umaban7 Txt_C', 'Umaban8 Txt_C'])
            if number_cell:
                number = number_cell.get_text(strip=True) if number_cell else '--'
            
            # 枠番を取得
            frame_number = ""
            frame_number_cell = tr.find('td', class_=['Waku1 Txt_C', 'Waku2 Txt_C', 'Waku3 Txt_C', 'Waku4 Txt_C', 'Waku5 Txt_C', 'Waku6 Txt_C', 'Waku7 Txt_C', 'Waku8 Txt_C'])
            if frame_number_cell:
                frame_number_span =  frame_number_cell.find('span')
                frame_number = frame_number_span.get_text(strip=True) if number_cell else '--'

            # 馬名を取得
            name = ""
            name_span = tr.find('span', class_='HorseName')
            if name_span:
                name = name_span.get_text(strip=True) if name_span else ''

            # 馬のId取得
            # 血統情報を取得
            ## 失敗したら諦める
            horse_id = ""
            father = ""
            grandfather = ""
            try:
                horse_href = name_span.find('a').get("href")
                horse_id = horse_href.split('/')[4]
                blood = horse_clinet.get_blood(horse_id)
                father = blood.father
                grandfather = blood.grandfather
            except:
                print("Fail Get Horse Id")

            # 性齢を取得
            sex_age = ""
            sex_age_cell = tr.find('td', class_='Barei')
            if sex_age_cell:
                sex_age = sex_age_cell.get_text(strip=True) if sex_age_cell else ''
            
            # 斤量を取得
            carried = ""
            carried_cells = tr.find_all('td', class_='Txt_C')
            if carried_cells:
                carried = carried_cells[0].get_text(strip=True)

            # 馬体重を取得
            horse_weight_cell = tr.find_all('td', class_='Weight')
            if horse_weight_cell:
                horse_weight = horse_weight_cell[0].get_text(strip=True)
            else:
                horse_weight = '--'
            
            # 騎手を取得
            jockey = ""
            jockey_cell = tr.find('td', class_='Jockey')
            if jockey_cell:
                jockey = jockey_cell.get_text(strip=True) if jockey_cell else ''

            # DTOを作成してリストに追加
            horse_list.append(
                RaceResultInfoDto(
                    type="未来",
                    date="",
                    rank="",
                    frame_number=frame_number,
                    horse_number=number,
                    horse_id=horse_id,
                    horse_name=name,
                    horse_link=f"https://db.netkeiba.com/horse/{horse_id}",
                    sex_age=sex_age,
                    fathder=father,
                    grandfather=grandfather,
                    weight_carried=carried,
                    jockey=jockey,
                    time="",
                    margin="",
                    passing="",
                    last_3f="",
                    odds="",
                    popularity="",
                    horse_weight=horse_weight,
                    location=location,
                    distance=distance,
                    weather=weather,
                    track_condition=track_condition,
                )
            )
        
        return horse_list