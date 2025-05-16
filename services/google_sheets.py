# services/google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
from datetime import datetime, timedelta

def add_booking_to_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds ", "https://www.googleapis.com/auth/drive "]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIALS_FILE, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(config.GOOGLE_SHEET_ID).sheet1

    flight_date = datetime.strptime(data["date"], "%d.%m.%Y")
    call_date = (flight_date - timedelta(days=2)).strftime("%d.%m.%y")

    row = [
        datetime.now().strftime("%d.%m.%Y"),
        data.get("name", ""),
        data.get("phone", ""),
        data.get("program", ""),
        data.get("people_count", ""),
        data.get("date", ""),
        "Утро",
        data.get("sum", ""),
        "",  # Сертификат
        call_date,
        "",  # Вес
        "",  # Примечание
        "",  # Пилот
        ""   # Аэростат
    ]
    sheet.append_row(row)