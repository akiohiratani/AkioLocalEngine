import requests
from bs4 import BeautifulSoup
from services.rate_limiter import RateLimiter

class BaseClient:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": self.USER_AGENT}
        self.rate_limiter = RateLimiter(1.000, 1.250)

    def get_soup(self, url: str) -> BeautifulSoup:
        # リクエスト前に間隔を空ける
        self.rate_limiter.wait()
        with self.session.get(url, headers=self.headers) as response:
            response.encoding = 'EUC-JP'
            return BeautifulSoup(response.text, 'lxml')