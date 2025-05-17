import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
from datetime import datetime, timedelta

# Проверка наличия credentials.json
def check_credentials_file():
    import os
    if not os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
        raise FileNotFoundError(f"Файл {config.GOOGLE_CREDENTIALS_FILE} не найден. Убедитесь, что он существует.")

# Добавление заявки в таблицу
def add_booking_to_sheet(data):
    # Проверяем наличие файла credentials.json
    check_credentials_file()

    scope = ['https://spreadsheets.google.com/feeds ', 'https://www.googleapis.com/auth/drive ']
    
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIALS_FILE, scope)
    except ValueError as e:
        raise ValueError("Ошибка загрузки учетных данных Google. Убедитесь, что credentials.json корректный.") from e

    try:
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(config.GOOGLE_SHEET_ID).sheet1
    except Exception as e:
        raise ConnectionError("Не удалось подключиться к Google Sheets API. Проверьте GOOGLE_SHEET_ID и доступы.") from e

    # Получаем дату полёта и вычисляем дату звонка
    try:
        flight_date = datetime.strptime(data["Дата полета"], "%d.%m.%Y")
        call_date = (flight_date - timedelta(days=2)).strftime("%d.%m.%y")
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательное поле: {e}")
    except ValueError as e:
        raise ValueError("Неверный формат даты. Используйте формат ДД.ММ.ГГГГ") from e

    # Формируем строку для добавления в таблицу
    row = [
        datetime.now().strftime("%d.%m.%Y"),         # Дата заполнения
        data.get("Имя", ""),                         # Имя клиента
        data.get("Телефон", ""),                     # Телефон
        data.get("Программа", ""),                   # Программа
        data.get("Кол-во", ""),                      # Кол-во человек
        data.get("Дата полета", ""),                 # Дата полета
        "Утро",                                      # Время полета (можно заменить логикой)
        data.get("Сумма", ""),                       # Сумма
        "",                                          # Сертификат (пусто)
        call_date,                                   # Дата звонка
        "",                                          # Вес (пусто)
        "",                                          # Примечание
        "",                                          # Пилот
        ""                                           # Аэростат
    ]

    try:
        sheet.append_row(row)
    except Exception as e:
        print("❌ Ошибка при добавлении строки:", e)
        raise