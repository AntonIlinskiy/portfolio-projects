from __future__ import annotations
from services.repo import list_free_slots, reserve_slot

def get_free_slots(date_str: str, limit: int | None = None) -> list[str]:
    return list_free_slots(date_str, limit)

def reserve_slot_wrapper(
    date_str: str,
    time_str: str,
    user_id: int,
    service: str | None,
    brand: str | None,
    model: str | None,
) -> bool:
    return reserve_slot(date_str, time_str, user_id, service, brand, model)
