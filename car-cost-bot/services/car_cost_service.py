from services.parsers.avito_parser_playwright import AvitoCarParser
from services.cost_calculator import calculate_total_cost
from typing import Optional, Dict

def get_final_car_cost(url: str) -> Optional[Dict[str, int]]:
    print("\n▶️ Вызов get_final_car_cost")

    try:
        parser = AvitoCarParser(url)
        car_info = parser.get_info()
        print("\U0001F9FE car_info получен:", car_info)
    except Exception as e:
        print(f"❌ Ошибка при получении информации: {e}")
        return None

    if not car_info or not car_info.get("price"):
        print("❌ car_info пустой или не содержит цену")
        return None

    base_price = car_info.get("price")
    print("\U0001F4B0 Извлечён base_price:", base_price)

    cost_result = calculate_total_cost(base_price)
    return cost_result


# Тест запуска для отладки парсера
if __name__ == "__main__":
    test_url = "https://www.avito.ru/moskva/avtomobili/bmw_3_seriya_2.0_at_2012_250_000_km_7401611722"
    result = get_final_car_cost(test_url)

    print("\n📦 Результат get_final_car_cost:", result)

    if result:
        for key, value in result.items():
            print(f"{key}: {value} ₽")
    else:
        print("❌ Не удалось получить стоимость автомобиля")
