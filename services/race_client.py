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