# 🚗 Car Cost Bot

Telegram-бот для расчёта полной стоимости автомобиля по ссылке на объявление Avito или Drom.ru.

## ⚙️ Функциональность

- 🔍 Парсинг объявлений с Avito (и скоро — Drom.ru)
- 💰 Расчёт полной стоимости автомобиля:
  - Базовая цена
  - Доставка
  - Таможенные сборы
  - Сервисный сбор
- 🤖 Telegram-интерфейс с командой `/start` и обработкой ссылок

## 📁 Структура проекта

```
car-cost-bot/
├── bot/                      # Telegram-бот
│   ├── handlers/            # Обработчики команд
│   │   ├── start.py
│   │   └── link_handler.py
│   ├── config.py            # Загрузка токена и .env
│   └── main.py              # Запуск бота
├── services/                # Бизнес-логика
│   ├── cost_calculator.py   # Расчёт стоимости
│   ├── car_cost_service.py  # Объединение логики
│   └── parsers/
│       ├── avito_parser.py  # Парсер Avito
│       └── drom_parser.py   # Парсер Drom (в процессе)
├── .env.example             # Пример переменных окружения
├── requirements.txt         # Зависимости
└── README.md                # Документация
```

## 🧪 Пример использования

Скопируй ссылку на авто с Avito и отправь её боту — он посчитает полную стоимость с учётом всех сборов.

Пример:

```
/start
https://www.avito.ru/moskva/avtomobili/bmw/3_seriya-ASgBAgICAkTgtg3klyjitg32myg
```

## 🔐 Переменные окружения

Создай `.env` файл на основе `.env.example`:

```
BOT_TOKEN=твой_токен_бота
```

## 🛠️ Установка и запуск

```bash
git clone https://github.com/AntonIlinskiy/car-cost-bot.git
cd car-cost-bot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m bot.main
```

## 📌 Планы

- ✅ Avito-парсер
- 🛠️ Парсер Drom.ru
- 💬 Мультиязычный интерфейс
- 🧾 Учёт дополнительных сборов
- 🔒 Авторизация (опционально)

---

Сделано с ❤️ Антоном Ilinskiy
