from services.base_client import BaseClient
from typing import List
import re

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