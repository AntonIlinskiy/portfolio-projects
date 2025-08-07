import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
import random


class AvitoCarParser:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru,en;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.avito.ru/",
        }

    def get_info(self) -> Optional[dict]:
        html = None
        for attempt in range(3):
            try:
                response = requests.get(self.url, headers=self.headers, timeout=10)
                response.raise_for_status()
                html = response.text
                break
            except Exception as e:
                print(f"❌ Попытка {attempt + 1} — ошибка запроса к Avito: {e}")
                time.sleep(3 + random.uniform(0.5, 1.5))

        if html is None:
            return None

        soup = BeautifulSoup(html, "lxml")

        try:
            title_tag = soup.find("span", {"itemprop": "name"})
            price_tag = soup.find("span", {"itemprop": "price"})
            if not title_tag or not price_tag:
                raise AttributeError("Не найдены теги title или price")

            title = title_tag.text.strip()
            price = int(''.join(filter(str.isdigit, price_tag.text)))
        except AttributeError as e:
            print(f"❌ Не удалось распарсить данные: {e}")
            return None

        return {
            "title": title,
            "price": price
        }


# Тестовый запуск
if __name__ == "__main__":
    print("🔍 Тест запуска avito_parser начат")
    test_url = "https://www.avito.ru/moskva/avtomobili/bmw_3_seriya_2.0_at_2012_250_000_km_7401611722"
    parser = AvitoCarParser(test_url)
    info = parser.get_info()
    print("📦 Полученные данные:", info)
