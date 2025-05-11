from services.base_client import BaseClient
from typing import List
import re
from domain.horse import HorseDto
from services.horce_client import HorseClient

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

    def get_candidate_list(self, id:str)->List[HorseDto]:
        horse_clinet = HorseClient()
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        table = soup.find("table", class_="Shutuba_Table RaceTable01 ShutubaTable")
        # 馬情報が含まれる行を全て取得
        rows = table.find_all('tr', class_='HorseList')        
        horse_list = []
        for tr in rows:
            # 馬番を取得
            number_cell = tr.find('td', class_=['Umaban1 Txt_C', 'Umaban2 Txt_C', 'Umaban3 Txt_C', 'Umaban4 Txt_C', 'Umaban5 Txt_C', 'Umaban6 Txt_C', 'Umaban7 Txt_C', 'Umaban8 Txt_C'])
            number = number_cell.get_text(strip=True) if number_cell else ''
            
            # 馬名を取得
            name_span = tr.find('span', class_='HorseName')
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
            sex_age_cell = tr.find('td', class_='Barei')
            sex_age = sex_age_cell.get_text(strip=True) if sex_age_cell else ''
            
            # 斤量を取得
            carried_cells = tr.find_all('td', class_='Txt_C')
            if carried_cells:
                carried = carried_cells[0].get_text(strip=True)
            else:
                carried = ''
            
            # 騎手を取得
            jockey_cell = tr.find('td', class_='Jockey')
            jockey = jockey_cell.get_text(strip=True) if jockey_cell else ''

            # 騎手のId取得
            ## 失敗したら諦める
            jockey_id = ""
            try:
                jockey_href = jockey_cell.find('a').get("href")
                jockey_id = jockey_href.split('/')[6]
            except:
                print("Fail Get Jocekey Id")

            # 調教師を取得
            trainer_cell = tr.find('td', class_='Trainer')
            trainer = trainer_cell.get_text(strip=True) if trainer_cell else ''
            
            # DTOを作成してリストに追加
            horse_list.append(
                HorseDto(
                    number=number,
                    horse_id=horse_id,
                    name=name, 
                    sex_age=sex_age, 
                    father=father,
                    grandfather=grandfather,
                    carried=carried, 
                    jockey_id=jockey_id,
                    jockey=jockey, 
                    trainer=trainer
                )
            )
        
        return horse_list