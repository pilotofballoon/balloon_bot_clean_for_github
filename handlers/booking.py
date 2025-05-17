from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, InputMediaPhoto
from states import BookingStates
from services.google_sheets import add_booking_to_sheet
import re
from datetime import datetime, timedelta

router = Router()

# 💰 Таблица цен
PRICE_TABLE = {
    "solo": {1: 40000, 2: 45000, 3: 55000, 4: 60000},
    "group": {1: 22500, 2: 36000, 3: 45000},
    "family": {"2+1": 54000, "2+2": 63000, "2+3": 72000}
}

# 📱 Проверка телефона
def is_valid_phone(phone: str) -> bool:
    return re.fullmatch(r"(\+7|8)[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}", phone) is not None

# 📅 Проверка даты
def is_valid_date(date_text: str) -> bool:
    try:
        flight_date = datetime.strptime(date_text, "%d.%m.%Y")
        today = datetime.now()
        if flight_date < today:
            return False
        return True
    except ValueError:
        return False

# --- Начало бронирования ---
@router.callback_query(F.data.startswith("book_"))
async def start_booking(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    if len(parts) < 2:
        await callback.message.answer("❌ Неверный запрос.")
        return

    program = parts[1]
    await state.set_state(BookingStates.name)
    await state.update_data(program=program)

    kb = [{"text": "⬅️ Назад", "callback_data": "balloon_menu"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)

    await callback.message.edit_caption(
        caption="Введите ваше имя для начала бронирования:",
        reply_markup=builder.as_markup()
    )

# --- Шаг 1: Имя ---
@router.message(BookingStates.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name.replace(" ", "").isalpha():
        await message.answer("❌ Имя должно содержать только буквы.")
        return

    await state.update_data(name=name)
    await state.set_state(BookingStates.phone)

    kb = [{"text": "⬅️ Назад", "callback_data": "balloon_menu"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)

    await message.answer("📞 Укажите ваш телефон:\nПример: +79001234567", reply_markup=builder.as_markup())

# --- Шаг 2: Телефон ---
@router.message(BookingStates.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not is_valid_phone(phone):
        await message.answer("❌ Введите корректный номер телефона.\nПример: +79001234567")
        return

    await state.update_data(phone=phone)
    await state.set_state(BookingStates.people_count)

    data = await state.get_data()
    program = data["program"]

    kb = []
    if program == "solo":
        kb = [
            {"text": "1 чел.", "callback_data": "people_1"},
            {"text": "2 чел.", "callback_data": "people_2"},
            {"text": "3 чел.", "callback_data": "people_3"},
            {"text": "4 чел.", "callback_data": "people_4"}
        ]
    elif program == "group":
        kb = [
            {"text": "1 чел. (мин. 3 на дату)", "callback_data": "people_1"},
            {"text": "2 чел. (мин. 3 на дату)", "callback_data": "people_2"},
            {"text": "3 чел. (гарантированный полёт)", "callback_data": "people_3"}
        ]
    elif program == "family":
        kb = [
            {"text": "2+1", "callback_data": "people_2+1"},
            {"text": "2+2", "callback_data": "people_2+2"},
            {"text": "2+3", "callback_data": "people_2+3"}
        ]

    kb.append({"text": "⬅️ Назад", "callback_data": "balloon_menu"})
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await message.answer("Сколько человек будет на полёте?", reply_markup=builder.as_markup())

# --- Шаг 3: Количество людей ---
@router.callback_query(F.data.startswith("people_"))
async def process_people(callback: CallbackQuery, state: FSMContext):
    people_count = callback.data.split("_")[1]
    data = await state.get_data()
    program = data["program"]

    if program == "group":
        try:
            people_count_int = int(people_count)
            if not (1 <= people_count_int <= 3):
                await callback.answer("❌ Можно выбрать от 1 до 3 человек.")
                return
        except ValueError:
            await callback.answer("❌ Неверное значение.")
            return
    elif program == "family" and "+" not in people_count:
        await callback.answer("❌ Выберите формат '2+1', '2+2' и т.д.")
        return
    elif program == "solo":
        try:
            people_count_int = int(people_count)
            if not (1 <= people_count_int <= 4):
                await callback.answer("❌ Можно выбрать от 1 до 4 человек.")
                return
        except ValueError:
            await callback.answer("❌ Неверное количество людей.")
            return

    await state.update_data(people_count=people_count)
    await state.set_state(BookingStates.date)
    await callback.message.edit_text("📅 Введите желаемую дату полёта:\nФормат: ДД.ММ.ГГГГ")

# --- Шаг 4: Дата ---
@router.message(BookingStates.date)
async def finalize_booking(message: Message, state: FSMContext):
    date = message.text.strip()
    if not is_valid_date(date):
        await message.answer("❌ Введите корректную дату (в будущем):\nФормат: ДД.ММ.ГГГГ")
        return

    await state.update_data(date=date)
    data = await state.get_data()

    summary = f"""
🧾 *Ваша заявка*
👤 Имя: {data['name']}
📞 Телефон: {data['phone']}
🎈 Программа: {data['program'].title()}
👥 Кол-во: {data['people_count']}
📅 Желаемая дата: {date}
Нажмите \"✅ Отправить\", чтобы завершить бронирование.
"""

    kb = [
        {"text": "✅ Отправить", "callback_data": "submit_booking"},
        {"text": "❌ Отмена", "callback_data": "cancel_booking"}
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await message.answer(summary, reply_markup=builder.as_markup())

# --- Шаг 5: Отправка заявки ---
@router.callback_query(F.data == "submit_booking")
async def submit_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    required_keys = ["name", "phone", "program", "people_count", "date"]
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        await callback.message.answer(f"❌ Не все данные собраны: {', '.join(missing_keys)}")
        return

    name = data["name"]
    phone = data["phone"]
    program = data["program"]
    people_count = data["people_count"]
    date = data["date"]

    # 💰 Расчёт стоимости
    total_price = PRICE_TABLE.get(program, {}).get(int(people_count) if "+" not in people_count else people_count, "Неизвестно")

    # 📅 Дата звонка
    try:
        flight_date = datetime.strptime(date, "%d.%m.%Y")
        call_date = (flight_date - timedelta(days=2)).strftime("%d.%m.%y")
    except ValueError:
        await callback.message.answer("❌ Неверный формат даты.")
        return

    # 📥 Формируем данные для Google Sheets
    sheet_data = {
        "Имя": name,
        "Телефон": phone,
        "Программа": program.title(),
        "Кол-во": people_count,
        "Дата полета": date,
        "Сумма": str(total_price),
        "Дата звонка": call_date
    }

    # 📄 Записываем в таблицу
    try:
        add_booking_to_sheet(sheet_data)
    except Exception as e:
        await callback.message.answer("❌ Произошла ошибка при отправке заявки.")
        print("Ошибка записи в таблицу:", e)

    # 📬 Уведомление админам
    from config import ADMINS
    for admin_id in ADMINS:
        try:
            await callback.bot.send_message(
                admin_id,
                f"🧾 *Новая заявка*\n"
                f"👤 Имя: {name}\n"
                f"📞 Телефон: {phone}\n"
                f"🎈 Программа: {program.title()}\n"
                f"👥 Кол-во: {people_count}\n"
                f"📅 Дата: {date}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")

    # 📨 Подтверждение пользователю
    confirmation = f"""
✅ *Заявка принята!*

👤 Имя: {name}
📞 Телефон: {phone}
🎈 Программа: {program.title()}
👥 Кол-во: {people_count}
📅 Дата: {date}
💰 Сумма: {total_price}₽

Мы свяжемся с вами заранее, чтобы уточнить детали полёта.

⚠️ Полёт состоится при благоприятных погодных условиях.
"""

    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=confirmation)
    kb = [{"text": "⬅️ Назад", "callback_data": "balloon_menu"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)

    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())
    await callback.message.answer(confirmation)

    # 🧹 Очищаем состояние
    await state.clear()

# --- Шаг 6: Отмена ---
@router.callback_query(F.data == "cancel_booking")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption="❌ Бронирование отменено")
    kb = [{"text": "⬅️ Назад", "callback_data": "balloon_menu"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())