from services.base_client import BaseClient
import re

class SpecialClient(BaseClient):

    # url
    BASE_URL = "https://race.netkeiba.com/special/index.html?id={}"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # レースを一意に認識できるId取得(202505020211)
    def get_race_id(self, id:str):
        url = self.BASE_URL.format(id)
        soup = self.get_soup(url)
        divs = soup.find_all("div", class_="Top_RaceMenu_Inner")
        race_id = None

        for div in divs:
            for link in div.find_all("a", href=True):
                match = re.search(r'race_id=(\d{12})', link['href'])
                if match:
                    race_id = match.group(1)
        return race_id