import time
import requests
from bs4 import BeautifulSoup
from typing import Optional


class DromCarParser:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/115.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://auto.drom.ru/',
        }

    def get_info(self) -> Optional[dict]:
        try:
            print("🌐 Отправляю запрос к Drom...")
            time.sleep(2)  # Задержка для обхода блокировки
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Ошибка при запросе: {e}")
            return None
        except Exception as e:
            print(f"❌ Другая ошибка при запросе: {e}")
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        try:
            title_tag = soup.find("span", {"data-ftid": "advert_title"})
            price_tag = soup.find("span", {"data-ftid": "bull_price"})

            if not title_tag or not price_tag:
                print("❌ Не удалось распарсить данные (title или price)")
                return None

            title = title_tag.text.strip()
            price_str = price_tag.text.strip()
            price = int(''.join(filter(str.isdigit, price_str)))

            return {
                "title": title,
                "price": price
            }
        except Exception as e:
            print(f"❌ Ошибка парсинга HTML: {e}")
            return None


# Тестовый запуск
if __name__ == "__main__":
    print("🔍 Тест запуска drom_parser начат")
    test_url = "https://auto.drom.ru/moskva/cars/mercedes-benz/s-class/621726982.html"  # ⚠️ Вставь сюда актуальный URL
    parser = DromCarParser(test_url)
    info = parser.get_info()
    print("📦 Получено:", info)
