import requests
from bs4 import BeautifulSoup
from typing import Optional

class AvitoCarParser:
    def __init__(self, url: str):
        self.url = url

    def get_info(self) -> Optional[dict]:
        print("🔧 Заглушка работает — возвращаю тестовые данные")
        return {
            'title': "BMW 3 серия, 2013",
            'price': 1230000
        }


    def get_info(self) -> Optional[dict]:
        print("🔧 Заглушка работает — возвращаю тестовые данные")
        return {
        'title': "BMW 3 серия, 2013",
        'price': 1230000
    }




# Тестовый запуск
if __name__ == "__main__":
    test_url = "https://www.avito.ru/moskva/avtomobili/bmw/3_seriya-ASgBAgICAkTgtg3klyjitg32myg"
    parser = AvitoCarParser(test_url)
    info = parser.get_info()
    print("Результат парсинга:", info)
