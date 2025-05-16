# handlers/common.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputMediaPhoto, FSInputFile
from data.messages import START_MESSAGE, BALLOON_MENU

router = Router()

# Маппинг целей "назад"
BACK_MAP = {
    "back_to_balloon_menu": {"photo": "photos/balloon.jpg", "caption": BALLOON_MENU, "keyboard": "balloon_menu"},
    "back_to_main": {"photo": "photos/start.jpg", "caption": START_MESSAGE, "keyboard": "main_menu"},
}

def main_menu_keyboard():
    kb = [
        {"text": "О Нас", "callback_data": "about"},
        {"text": "Воздушный шар", "callback_data": "balloon_menu"},
        {"text": "Горные лыжи", "callback_data": "ski"},
        {"text": "Контакты", "callback_data": "contacts"}
    ]
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    return builder.as_markup()

def balloon_menu_keyboard():
    kb = [
        {"text": "🌟 Соло-программа", "callback_data": "program_solo"},
        {"text": "👥 Групповой полет", "callback_data": "program_group"},
        {"text": "👨‍👩‍👧‍👦 Семейный полет", "callback_data": "program_family"},
        {"text": "📋 FAQ и условия", "callback_data": "faq"},
        {"text": "⬅️ Назад", "callback_data": "back_to_main"}
    ]
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    return builder.as_markup()

@router.callback_query(F.data.in_(BACK_MAP.keys()))
async def universal_back_handler(callback: CallbackQuery):
    target = BACK_MAP[callback.data]
    photo_path = target["photo"]
    caption = target.get("caption")
    keyboard_type = target.get("keyboard")

    if keyboard_type == "main_menu":
        keyboard = main_menu_keyboard()
    elif keyboard_type == "balloon_menu":
        keyboard = balloon_menu_keyboard()
    else:
        await callback.answer("Неизвестная цель")
        return

    media = InputMediaPhoto(media=FSInputFile(photo_path), caption=caption)
    await callback.message.edit_media(media=media, reply_markup=keyboard)