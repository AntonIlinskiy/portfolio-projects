🏗 Construction Bot — Telegram-бот для ремонта и строительства
Бот помогает клиентам быстро получить информацию об услугах, посмотреть примеры работ и оставить заявку прямо в чате.

Возможности:

🛠 Просмотр услуг (ремонт, строительство, проектирование)

📁 Портфолио работ

💬 Отзывы клиентов

🔥 Актуальные акции и скидки

❓ FAQ

📞 Оставить заявку (с автоматической записью в Google Sheets)

⚙️ Стек технологий
Python 3.11+

aiogram 3.x (Telegram Bot API)

python-dotenv — загрузка переменных окружения

gspread + google-auth — интеграция с Google Sheets

🚀 Установка и запуск

1. Клонировать репозиторий
   bash
   Копировать
   Редактировать
   git clone https://github.com/AntonIlinskiy/portfolio-projects.git
   cd portfolio-projects/construction-bot
2. Создать и активировать виртуальное окружение
   bash
   Копировать
   Редактировать
   python -m venv .venv

# Windows PowerShell

.\.venv\Scripts\Activate.ps1

# macOS / Linux

source .venv/bin/activate 3. Установить зависимости
bash
Копировать
Редактировать
pip install -r requirements.txt 4. Настроить .env
env
Копировать
Редактировать
BOT*TOKEN=ВАШ*ТОКЕН*БОТА
GOOGLE_SERVICE_ACCOUNT_FILE=creds/service_account.json
GOOGLE_SHEET_ID=ID*ТАБЛИЦЫ
GOOGLE_LEADS_SHEET=Заявки
Примечания:

GOOGLE_SHEET_ID — это ID из URL Google-таблицы (между /d/ и /edit).

В Google Sheets добавьте client_email из creds/service_account.json в доступ с ролью Редактор.

5. Запустить бота
   bash
   Копировать
   Редактировать
   python -m bot.main
   🧭 Команды бота
   /start — главное меню

🏗 Услуги — выбор направления

📁 Портфолио

💬 Отзывы

🔥 Акции

❓ FAQ

ℹ️ О компании

📞 Оставить заявку — с записью в Google Sheets

📒 Структура проекта
bash
Копировать
Редактировать
construction-bot/
├── bot/
│ ├── handlers/ # Обработчики
│ │ ├── start.py
│ │ ├── services.py
│ │ ├── portfolio.py
│ │ ├── reviews.py
│ │ ├── promos.py
│ │ ├── faq.py
│ │ ├── info.py
│ │ ├── request.py # Форма заявки (FSM)
│ │ └── **init**.py # Сборка роутеров
│ ├── keyboards.py
│ └── main.py
├── services/
│ └── gsheets.py # Запись в Google Sheets
├── creds/
│ └── service_account.json
├── requirements.txt
└── README.md
✅ Проверка Google Sheets
После отправки заявки через бота:

Откройте таблицу, указанную в GOOGLE_SHEET_ID

Убедитесь, что данные попали в лист GOOGLE_LEADS_SHEET

Если не работает:

Проверьте ID таблицы

Убедитесь, что лист с таким именем существует

Проверьте доступ client_email из service_account.json

📦 Установка зависимостей
Все необходимые зависимости перечислены в requirements.txt.

🧹 Примечания по коду
Лишние тестовые обработчики удалены

Все рабочие роутеры собраны в bot/handlers/**init**.py

Код соответствует структуре продакшн-проекта

📤 Публикация изменений
bash
Копировать
Редактировать
git add .
git commit -m "cleanup: remove test handlers; finalize routers; add project README"
git push
