from typing import Dict


def calculate_total_cost(base_price: int) -> Dict[str, int]:
    """
    Расчёт финальной стоимости авто
    """
    delivery_cost = 80000
    customs_fee = int(base_price * 0.15)
    service_fee = 25000

    total = base_price + delivery_cost + customs_fee + service_fee

    return {
        "base_price": base_price,
        "delivery_cost": delivery_cost,
        "customs_fee": customs_fee,
        "service_fee": service_fee,
        "total_cost": total
    }


# Тест (не обязателен)
if __name__ == "__main__":
    result = calculate_total_cost(1230000)
    for key, value in result.items():
        print(f"{key}: {value} ₽")
