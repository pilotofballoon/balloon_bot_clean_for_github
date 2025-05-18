# services/google_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import os
import config

def check_credentials_file():
    """Проверяет наличие файла учетных данных Google."""
    if not os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
        raise FileNotFoundError(f"Файл {config.GOOGLE_CREDENTIALS_FILE} не найден.")

def add_booking_to_sheet(data):
    """
    Добавляет новую заявку в Google Таблицу.
    
    :param data: dict - словарь с данными бронирования
    """
    check_credentials_file()

    scope = [
        'https://spreadsheets.google.com/feeds ',
        'https://www.googleapis.com/auth/drive '
    ]

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            config.GOOGLE_CREDENTIALS_FILE,
            scope
        )
        client = gspread.authorize(credentials)
    except Exception as e:
        raise ConnectionError("Не удалось авторизоваться в Google Sheets API.") from e

    try:
        sheet = client.open_by_key(config.GOOGLE_SHEET_ID).sheet1
    except Exception as e:
        raise ConnectionError("Не удалось подключиться к таблице. Проверьте GOOGLE_SHEET_ID.") from e

    # Парсим дату полёта
    try:
        flight_date = datetime.strptime(data["Дата полета"], "%d.%m.%Y")
        call_date = (flight_date - timedelta(days=2)).strftime("%d.%m.%y")
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательное поле: {e}")
    except ValueError as e:
        raise ValueError("Неверный формат даты. Используйте формат ДД.ММ.ГГГГ") from e

    # Формируем строку для добавления
    row = [
        datetime.now().strftime("%d.%m.%Y"),     # Дата заполнения
        data.get("Имя", ""),                     # Имя клиента
        data.get("Телефон", ""),                 # Телефон
        data.get("Программа", ""),               # Программа
        data.get("Кол-во", ""),                  # Кол-во человек
        data.get("Дата полета", ""),             # Дата полета
        "Утро",                                  # Время полета (можно расширить логику)
        str(data.get("Сумма", "")),             # Сумма
        "",                                      # Сертификат
        call_date,                               # Дата звонка
        "",                                      # Вес
        "",                                      # Примечание
        "",                                      # Пилот
        "",                                      # Аэростат
    ]

    try:
        sheet.append_row(row)
    except Exception as e:
        print("❌ Ошибка при добавлении строки:", e)
        raise