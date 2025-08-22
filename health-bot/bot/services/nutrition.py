from dataclasses import dataclass

ACTIVITY = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

@dataclass
class Macros:
    kcal: int
    protein_g: int
    fat_g: int
    carbs_g: int

def bmr_mifflin(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    if sex == "male":
        return 10*weight_kg + 6.25*height_cm - 5*age + 5
    return 10*weight_kg + 6.25*height_cm -5*age - 161    

def tdee(bmr: float, activity: str) -> float:
    return bmr * ACTIVITY.get(activity, 1.2)

def target_kcal(tdee_value: float, goal: str) -> int:
    if goal == "lose":
        return int(tdee_value - 400)
    if goal == "gain":
        return int(tdee_value + 300)
    return int(tdee_value)

def macros_for(kcal: int, weight_kg: float, goal: str) -> Macros:
    protein_per_kg = 2.0 if goal == "lose" else 1.7
    protein_g = round(weight_kg * protein_per_kg)
    fat_kcal = round(kcal * 0.30)
    fat_g = round(fat_kcal / 9)
    carbs_kcal = max(kcal - protein_g * 4 - fat_kcal, 0)
    carbs_g = round(carbs_kcal / 4)
    return Macros(kcal=kcal, protein_g=protein_g, fat_g=fat_g, carbs_g=carbs_g)

def format_macros(m: Macros) -> str:
    return( "<b>Нормы на день</b>\n"
        f"Калории: <b>{m.kcal}</b> ккал\n"
        f"Белки: <b>{m.protein_g}</b> г\n"
        f"Жиры: <b>{m.fat_g}</b> г\n"
        f"Углеводы: <b>{m.carbs_g}</b> г\n"
    )