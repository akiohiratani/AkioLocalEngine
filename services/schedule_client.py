from domain.race_info import RaceInfoDTO
from services.base_client import BaseClient
from typing import List

class ScheduleClient(BaseClient):

    # url
    BASE_URL = "https://race.netkeiba.com/top/schedule.html"

    # コンストラクタ
    def __init__(self):
        super().__init__()

    # 重賞関連のid取得(00xx)
    def search_g_race_list(self, days: List[str])->List[RaceInfoDTO]:
        soup = self.get_soup(self.BASE_URL)
        table = soup.find("table", class_="nk_tb_common race_table_01")
        races = []
        if(table):
            for row in soup.select('tr.schedule_list3, tr.schedule_list4'):
                cells = row.find_all('td')
                if not cells:
                    continue
                    
                date = cells[0].get_text(strip=True)
                if date not in days:
                    # 指定した日付以外はスキップ
                    continue

                # 必要な要素を指定して取得
                race_name_tag = cells[1].find('a')
                race_name = race_name_tag.get_text(strip=True) if race_name_tag else cells[1].get_text(strip=True)
                race_id = race_name_tag['href'].split('id=')[-1] if race_name_tag else ''
                races.append(RaceInfoDTO(
                    id=f"{race_id}" if race_id else '',
                    name=race_name,
                    place=cells[3].get_text(strip=True),
                    date=date,
                    distance=cells[4].get_text(strip=True)
                ))
        return races