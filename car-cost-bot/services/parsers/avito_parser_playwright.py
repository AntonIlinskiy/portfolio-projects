from typing import Optional, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class AvitoCarParser:
    def __init__(self, url: str):
        self.url = url

    def get_info(self) -> Optional[Dict[str, str]]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                print("🔍 Открываю страницу Avito...")
                page.goto(self.url, timeout=20000)
                page.wait_for_selector("span[itemprop='price']", timeout=15000)

                title = page.locator("h1").text_content()
                price_element = page.locator("span[itemprop='price']")
                price_raw = price_element.get_attribute("content") or price_element.text_content()

                # Сохраняем HTML-страницу на случай ошибки
                with open("avito_debug.html", "w", encoding="utf-8") as f:
                    f.write(page.content())

                price = int("".join(filter(str.isdigit, price_raw)))

                print(f"✅ Успешно извлечено:\n📌 title = {title}\n💰 price = {price}")
                return {"title": title.strip(), "price": price}

        except PlaywrightTimeoutError:
            print("❌ Таймаут ожидания загрузки страницы Avito.")
        except Exception as e:
            print(f"❌ Ошибка при парсинге Avito: {e}")
        return None


# 🔍 Тест
if __name__ == "__main__":
    test_url = "https://www.avito.ru/moskva/avtomobili/bmw_3_seriya_2.0_at_2012_250_000_km_7401611722"
    parser = AvitoCarParser(test_url)
    result = parser.get_info()

    print("📦 Результат:", result)
