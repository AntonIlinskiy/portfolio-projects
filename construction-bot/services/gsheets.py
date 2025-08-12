import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

def _get_client() -> gspread.Client:
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not creds_path or not os.path.exists(creds_path):
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT_FILE не задан или файл не найден. "
            "Укажи путь в .env: GOOGLE_SERVICE_ACCOUNT_FILE=creds/service_account.json"
        )
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    return gspread.authorize(creds)

def append_lead_row(
    when: datetime,
    name: str,
    phone: str,
    username: str | None,
    source: str,
    service: str | None,
    comment: str | None,
    worksheet_title: str = "Leads",
) -> None:
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
    if not spreadsheet_id:
        raise RuntimeError("Не задан GOOGLE_SHEETS_SPREADSHEET_ID в .env")

    client = _get_client()
    sh = client.open_by_key(spreadsheet_id)

    
    try:
        ws = sh.worksheet(worksheet_title)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_title, rows=1, cols=20)
        ws.append_row(
            ["Дата", "Имя", "Телефон", "Username", "Источник", "Услуга", "Комментарий"],
            value_input_option="USER_ENTERED",
        )

    ws.append_row(
        [
            when.strftime("%Y-%m-%d %H:%M"),
            name or "",
            phone or "",
            (f"@{username}" if username else ""),
            source or "Telegram",
            service or "",
            comment or "",
        ],
        value_input_option="USER_ENTERED",
    )
