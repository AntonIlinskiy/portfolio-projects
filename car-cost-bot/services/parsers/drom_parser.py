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
            )
        }

    def get_info(self) -> Optional[dict]:
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Ошибка при запросе: {e}")
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        # Сохраняем HTML-страницу для отладки
        with open("debug_drom.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            print("📄 HTML-страница сохранена в debug_drom.html")

        try:
            # Обновлённые селекторы по сохранённому HTML
            title_elem = soup.select_one("h1.css-1fkrnxv.e162wx9x0")
            price_elem = soup.select_one("span.css-1uvydh2.e162wx9x0")

            title = title_elem.text.strip() if title_elem else None
            price_text = price_elem.text.strip() if price_elem else None
            price = int(''.join(filter(str.isdigit, price_text))) if price_text else None
        except Exception as e:
            print(f"❌ Ошибка при парсинге: {e}")
            return None

        if not title or not price:
            print("❌ Не удалось распарсить данные (title или price)")
            return None

        return {
            "title": title,
            "price": price
        }


# Тестовый запуск
if __name__ == "__main__":
    print("🔍 Тест запуска drom_parser начат")
    test_url = "https://auto.drom.ru/moscow/bmw/5-series/732577793.html"  # Тестовая ссылка
    parser = DromCarParser(test_url)
    info = parser.get_info()
    print("🔍 Полученная информация с Drom:", info)
