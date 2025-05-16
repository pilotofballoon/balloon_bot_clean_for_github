# keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard():
    kb = [
        {"text": "О Нас", "callback_data": "about"},
        {"text": "Воздушный шар", "callback_data": "balloon_menu"},
        {"text": "Горные лыжи", "callback_data": "ski"},
        {"text": "Контакты", "callback_data": "contacts"}
    ]
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
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    return builder.as_markup()

def back_button_keyboard(callback_data="back_to_balloon_menu"):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=callback_data)
    return builder.as_markup()