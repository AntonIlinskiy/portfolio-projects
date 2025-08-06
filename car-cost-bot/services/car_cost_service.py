from typing import Optional, Dict

from services.parsers.avito_parser import AvitoCarParser
from services.parsers.drom_parser import DromCarParser
from services.cost_calculator import calculate_total_cost


def get_final_car_cost(url: str) -> Optional[Dict[str, int]]:
    print("▶️ Вызов get_final_car_cost")

    # Выбор парсера по домену
    if "avito.ru" in url:
        parser = AvitoCarParser(url)
    elif "drom.ru" in url:
        parser = DromCarParser(url)
    else:
        print("❌ Неизвестный источник ссылки")
        return None

    car_info = parser.get_info()
    print("🧾 car_info получен:", car_info)

    if not car_info:
        print("❌ car_info пустой или None")
        return None

    base_price = car_info.get("price")
    print("💰 Извлечён base_price:", base_price)

    cost_result = calculate_total_cost(base_price)
    return cost_result


# Локальный тест
if __name__ == "__main__":
    # 🔧 Подставь сюда ссылку с Avito или Drom для проверки
    test_url = "https://auto.drom.ru/moskva/cars/bmw/3-series/1234567890.html"

    result = get_final_car_cost(test_url)
    print("📦 Результат get_final_car_cost:", result)

    if result:
        for key, value in result.items():
            print(f"{key}: {value} ₽")
    else:
        print("Ошибка: результат отсутствует.")
