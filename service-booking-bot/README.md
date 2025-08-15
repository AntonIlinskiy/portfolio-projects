🗓 Service Booking Bot — запись клиентов в Telegram

Телеграм-бот для записи клиентов на услуги (например, техобслуживание авто).
Пользователь выбирает услугу → дату → время → вводит марку/модель → бронирование сохраняется в SQLite.
В боте также есть просмотр своих записей и отмена брони.

✨ Возможности

Выбор услуги из списка (пример: «ТО», «Диагностика», «Замена масла»)

Календарь на ближайшие дни и свободные интервалы

Подтверждение брони c записью в БД (SQLite)

Просмотр «Мои записи» и отмена

Поддержка любой марки и модели (ввод текстом)

Персистентная БД в bot/data/booking.db

🧰 Стек

Python 3.11+

aiogram 3.x

SQLite (встроенная sqlite3)

python-dotenv (переменные окружения)

🚀 Быстрый старт

Клонировать репозиторий и перейти в проект:

git clone https://github.com/AntonIlinskiy/portfolio-projects.git
cd portfolio-projects/service-booking-bot

Создать и активировать виртуальное окружение, поставить зависимости:

python -m venv .venv

# Windows PowerShell:

.\.venv\Scripts\Activate.ps1

# macOS/Linux:

source .venv/bin/activate

pip install -r requirements.txt

Настроить .env (создай файл service-booking-bot/.env):

BOT*TOKEN=ваш*токен*бота*из_BotFather

# опционально — таймзона, час начала/окончания при автосидах и т.п. (если используются)

Инициализировать базу и засеять свободные слоты (команда на Windows/PowerShell):

python -c "from services.repo import init_db, seed_default_week; init_db(reset=True); seed_default_week(); print('DB recreated & seeded.')"

Скрипт создаст bot/data/booking.db, таблицы slots и bookings, и заполнит неделю слотов.

Запустить бота:

python -m bot.main

Открой бота в Telegram и проверь путь: «Записаться → выбрать услугу → дату → время → указать марку/модель».

🗂 Структура проекта
service-booking-bot/
├─ bot/
│ ├─ handlers/
│ │ ├─ start.py # старт, меню
│ │ ├─ booking.py # основная логика записи (даты/время/подтверждение)
│ │ └─ **init**.py # сборка роутеров
│ ├─ keyboards.py # инлайн/реплай клавиатуры
│ ├─ main.py # входная точка бота
│ └─ data/
│ └─ booking.db # SQLite база (создаётся автоматически/скриптом)
├─ services/
│ ├─ repo.py # слой работы с БД (CRUD), схема таблиц
│ └─ slots.py # бизнес-логика слотов (free/ reserve/ cancel)
├─ .env # токен бота
├─ requirements.txt
└─ README.md

🧪 Полезные команды для БД (проверка)

Показать таблицы, последние брони и занятые слоты:

python - << "PY"
import sqlite3, pathlib
p = pathlib.Path("bot/data/booking.db")
con = sqlite3.connect(p)
c = con.cursor()
print("📦 DB:", p.resolve())
print("\n📚 Таблицы:", [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")])
print("\n📝 Последние bookings:")
for r in c.execute("SELECT id,user_id,service,brand,model,slot_date,slot_time,created_at FROM bookings ORDER BY id DESC LIMIT 10"):
print(" ", r)
print("\n⏰ Занятые слоты:")
for r in c.execute("SELECT slot_date,slot_time,taken FROM slots WHERE taken=1 ORDER BY slot_date,slot_time LIMIT 20"):
print(" ", r)
con.close()
PY

Полностью пересоздать базу и пересеять неделю:

python -c "from services.repo import init_db, seed_default_week; init_db(reset=True); seed_default_week(); print('DB recreated & seeded.')"
