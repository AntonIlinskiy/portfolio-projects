# 🤖 Portfolio Projects — Telegram Bots

Добро пожаловать!  
Здесь собраны **3 полноценных Telegram-бота**, которые я разработал для разных задач:  
здоровый образ жизни, строительство и сервисное обслуживание автомобилей.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/aiogram-3.x-green?logo=telegram" />
  <img src="https://img.shields.io/badge/FastAPI-optional-teal?logo=fastapi" />
  <img src="https://img.shields.io/badge/SQLite-DB-lightgrey?logo=sqlite" />
</p>

---

## 📂 Список проектов

### 1. 🏋️ Health Bot

Телеграм-бот для **здорового образа жизни**: питание, тренировки и мотивация.

**Функционал**:

- Анкета пользователя (возраст, вес, цели)
- Расчёт **норм калорий и БЖУ**
- План тренировок (неделя + кнопка «сегодня»)
- Напоминания: вода и тренировки ⏰
- История тренировок и streak
- Подписка на премиум

<details>
<summary>📸 Скриншоты</summary>
<p align="center">
  <img src="https://placehold.co/300x500?text=Health+Bot+1" />
  <img src="https://placehold.co/300x500?text=Health+Bot+2" />
</p>
</details>

---

### 2. 🛠️ Construction Bot

Телеграм-бот для **продвижения услуг по ремонту и строительству**.

**Функционал**:

- Каталог услуг: ремонт квартир, строительство коттеджей, проектирование 🏠
- Портфолио работ с изображениями
- Сбор номера телефона клиента
- Удобная навигация и обратная связь

<details>
<summary>📸 Скриншоты</summary>
<p align="center">
  <img src="https://placehold.co/300x500?text=Construction+Bot+1" />
  <img src="https://placehold.co/300x500?text=Construction+Bot+2" />
</p>
</details>

---

### 3. 🚗 Service Booking Bot

Телеграм-бот для **записи автомобилей на техобслуживание**.

**Функционал**:

- Запись на услуги (ТО, диагностика, ремонт) 🔧
- Выбор мастера и даты/времени
- Напоминания о визите
- История записей
- Админ-панель для управления заявками

<details>
<summary>📸 Скриншоты</summary>
<p align="center">
  <img src="https://placehold.co/300x500?text=Service+Bot+1" />
  <img src="https://placehold.co/300x500?text=Service+Bot+2" />
</p>
</details>

---

## 🚀 Запуск проектов

Каждый проект находится в отдельной папке (`health-bot`, `construction-bot`, `service-booking-bot`).  
Для запуска любого из них:

```bash
git clone https://github.com/AntonIlinskiy/portfolio-projects.git
cd portfolio-projects/<название-проекта>
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m bot.main
🔑 Не забудьте указать BOT_TOKEN в файле .env.

🛠️ Технологии
Python 3.12

Aiogram 3.x — для работы с Telegram API

APScheduler — планировщик задач (напоминания)

SQLite — база данных

SQLAlchemy — ORM

Docker (опционально) — для развёртывания

📌 Структура репозитория
bash
Копировать
Редактировать
portfolio-projects/
│
├── health-bot/         # Бот про ЗОЖ и тренировки
├── construction-bot/   # Бот про ремонт и строительство
├── service-booking-bot # Бот записи на ТО
└── README.md           # Общая документация
✨ Контакты
👨‍💻 Автор: Anton Ilinskiy
📩 Telegram: @твой_ник

⭐️ Если вам понравились проекты — поставьте звезду репозиторию!
```
