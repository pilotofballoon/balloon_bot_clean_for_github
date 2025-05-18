from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, Contact
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import BookingStates
from services.google_sheets import add_booking_to_sheet
from keyboards import main_menu_keyboard, balloon_menu_keyboard, back_button
from data.messages import FLIGHT_PROCEDURE_1, FLIGHT_PROCEDURE_2, FLIGHT_PROCEDURE_3

import re
from datetime import datetime, timedelta

router = Router()

# 💰 Таблица цен
PRICE_TABLE = {
    "solo": {1: 40000, 2: 40000, 3: 45000, 4: 55000},
    "group": {1: 22500, 2: 36000, 3: 45000},
    "family": {"2+1": 40000, "2+2": 45000, "2+3": 55000}
}

# 📱 Проверка даты
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
    program = callback.data.split("_")[1]
    await state.set_state(BookingStates.name)
    await state.update_data(program=program)

    first_name = callback.from_user.first_name or "Пользователь"
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Использовать моё имя", callback_data="use_default_name")
    kb.button(text="✍️ Ввести другое имя", callback_data="edit_name")
    kb.adjust(1)

    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=f"👋 Привет, {first_name}!\nХотите использовать это имя или указать другое?")
    await callback.message.edit_media(media=media, reply_markup=kb.as_markup())

# --- Шаг 1: Имя ---
@router.callback_query(BookingStates.name, F.data.in_(["use_default_name", "edit_name"]))
async def choose_name(callback: CallbackQuery, state: FSMContext):
    if callback.data == "use_default_name":
        name = callback.from_user.first_name
        await state.update_data(name=name)
        await state.set_state(BookingStates.contact)
        
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📞 Поделиться контактом", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption="📞 Поделитесь контактом:")
        await callback.message.edit_media(media=media, reply_markup=None)  # удаляем inline-клавиатуру
        await callback.message.answer("📞 Поделитесь контактом:", reply_markup=kb)
    else:
        await state.set_state(BookingStates.name)
        await callback.message.edit_text("Введите ваше имя:")

@router.message(BookingStates.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name.replace(" ", "").isalpha():
        await message.answer("❌ Имя должно содержать только буквы.")
        return

    await state.update_data(name=name)
    await state.set_state(BookingStates.contact)

    kb = InlineKeyboardBuilder()
    kb.button(text="📞 Поделиться контактом", request_contact=True)
    kb.button(text="⬅️ Назад", callback_data=f"book_{(await state.get_data())['program']}")
    kb.adjust(1)

    await message.answer("📞 Поделитесь контактом:", reply_markup=kb.as_markup())

# --- Шаг 2: Получение контакта ---
@router.message(BookingStates.contact, F.contact)
async def process_contact(message: Message, state: FSMContext):
    contact = message.contact
    phone = contact.phone_number
    name = contact.first_name

    await state.update_data(phone=phone, name=name)
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

    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.button(text="⬅️ Назад", callback_data=f"book_{program}")
    builder.adjust(1)
    await message.answer("👥 Сколько человек будет на полёте?", reply_markup=builder.as_markup())

# --- Шаг 3: Количество людей ---
@router.callback_query(BookingStates.people_count, F.data.startswith("people_"))
async def process_people(callback: CallbackQuery, state: FSMContext):
    people_count = callback.data.split("_")[1]
    data = await state.get_data()
    program = data["program"]

    # Проверки
    if program == "group" and "+" not in people_count:
        try:
            count = int(people_count)
            if not (1 <= count <= 3):
                await callback.answer("❌ Можно выбрать от 1 до 3 человек.")
                return
        except ValueError:
            await callback.answer("❌ Неверное значение.")
            return
    elif program == "family" and "+" not in people_count:
        await callback.answer("❌ Выберите формат '2+1', '2+2' и т.д.")
        return
    elif program == "solo" and "+" not in people_count:
        try:
            count = int(people_count)
            if not (1 <= count <= 4):
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
Нажмите \"✅ Отправить\", чтобы завершить.
"""

    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Отправить", callback_data="submit_booking")
    builder.button(text="❌ Отмена", callback_data="balloon_menu")
    builder.adjust(1)

    await message.answer(summary, reply_markup=builder.as_markup(), parse_mode="Markdown")

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

    total_price = PRICE_TABLE.get(program, {}).get(int(people_count) if "+" not in people_count else people_count, "Неизвестно")

    try:
        flight_date = datetime.strptime(date, "%d.%m.%Y")
        call_date = (flight_date - timedelta(days=2)).strftime("%d.%m.%y")
    except ValueError:
        await callback.message.answer("❌ Неверный формат даты.")
        return

    sheet_data = {
        "Имя": name,
        "Телефон": phone,
        "Программа": program.title(),
        "Кол-во": people_count,
        "Дата полета": date,
        "Сумма": str(total_price),
        "Дата звонка": call_date
    }

    try:
        add_booking_to_sheet(sheet_data)
    except Exception as e:
        await callback.message.answer("❌ Произошла ошибка при отправке заявки.")
        print("Ошибка записи в таблицу:", e)

    from config import ADMINS
    confirmation = f"""
✅ *Заявка принята!*
👤 Имя: {name}
📞 Телефон: {phone}
🎈 Программа: {program.title()}
👥 Кол-во: {people_count}
📅 Дата: {date}
💰 Сумма: {total_price}₽
⚠️ Полёт состоится при благоприятных погодных условиях.
"""

    builder = InlineKeyboardBuilder()
    builder.button(text="🧳 Посмотреть процедуру полёта", callback_data="show_flight_procedure")
    builder.button(text="⬅️ Назад", callback_data="balloon_menu")
    builder.adjust(1)

    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=confirmation)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

    for admin_id in ADMINS:
        try:
            await callback.bot.send_message(admin_id, confirmation, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка отправки админу {admin_id}: {e}")

    await state.clear()