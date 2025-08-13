# services/gsheets.py
import os
from datetime import datetime
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")        # creds/service_account.json
SHEET_ID             = os.getenv("GOOGLE_SHEET_ID")                    # id таблицы
DEFAULT_LEADS_SHEET  = os.getenv("GOOGLE_LEADS_SHEET", "Leads")        # имя листа по умолчанию

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _client() -> gspread.Client:
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError("GOOGLE_SERVICE_ACCOUNT_FILE не найден")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return gspread.authorize(creds)

def _open_worksheet(worksheet_name: str):
    if not SHEET_ID:
        raise NameError("GOOGLE_SHEET_ID не задан")
    client = _client()
    sh = client.open_by_key(SHEET_ID)
    try:
        return sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        return sh.add_worksheet(title=worksheet_name, rows=200, cols=20)

def ping() -> str:
    """Проверка подключения к таблице (читает A1 у листа по умолчанию)."""
    ws = _open_worksheet(DEFAULT_LEADS_SHEET)
    _ = ws.acell("A1").value  # просто триггерим чтение
    return "ok"

def append_row(
    worksheet_name: Optional[str],
    row: list,
):
    """Безопасная запись строки в лист."""
    ws = _open_worksheet(worksheet_name or DEFAULT_LEADS_SHEET)
    ws.append_row(row, value_input_option="USER_ENTERED")

def append_lead_row(
    when: datetime,
    name: str,
    phone: str,
    username: Optional[str],
    source: str,
    service: Optional[str],
    comment: Optional[str],
    worksheet_name: Optional[str] = None,
):
    """Унифицированная запись заявки."""
    row = [
        when.strftime("%Y-%m-%d %H:%M:%S"),
        name,
        phone,
        username or "-",
        source,
        service or "-",
        comment or "-",
    ]
    append_row(worksheet_name or DEFAULT_LEADS_SHEET, row)
