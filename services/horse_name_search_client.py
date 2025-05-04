import urllib.parse
from services.base_client import BaseClient
from typing import List
import re

class HorseNameSearchClient(BaseClient):
    # url
    BASE_URL = "https://db.netkeiba.com/?pid=horse_list&word={}&match=partial_match"
    MAX_RESULTS = 9

    # コンストラクタ
    def __init__(self):
        super().__init__()

    def search_horse_ids(self, word: str) -> List[str]:
        encoded_word = urllib.parse.quote(word)
        list_url = self.BASE_URL.format(encoded_word)
        soup = self.get_soup(list_url)
        table = soup.find("table", class_="nk_tb_common")
        horse_ids = []
        
        if table:
            for row in table.find_all("tr")[1:self.MAX_RESULTS+1]:
                cells = row.find_all("td")
                if len(cells) < 12:
                    continue
                horse_id_url = cells[1].find("a").get("href") if cells[1].find("a") else ""
                horse_id = horse_id_url.split('/')[2]

                if horse_id.isdecimal() :
                    horse_ids.append(horse_id)
                else:
                    # 完全一致して競走馬のリンクにリダイレクトして場合の例外処理
                    href = cells[24].find("a")['href']
                    # 正規表現でid=の値を抽出
                    match = re.search(r'id=(\d+)', href)
                    if match:
                        id_value = match.group(1)
                        print(id_value)  # 2021105560
                        horse_ids.append(id_value)
                        break
                
        return horse_ids
