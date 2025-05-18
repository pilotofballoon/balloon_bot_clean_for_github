# keyboards.py

from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard():
    kb = [
        {"text": "ℹ️ О нас", "callback_data": "about"},
        {"text": "🎈 Воздушный шар", "callback_data": "balloon_menu"},
        {"text": "⛷ Горные лыжи", "callback_data": "ski"},
        {"text": "📞 Контакты", "callback_data": "contacts"}
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    return builder.as_markup()

def balloon_menu_keyboard():
    kb = [
        {"text": "🌟 Соло-программа", "callback_data": "program_solo"},
        {"text": "👥 Групповой полёт", "callback_data": "program_group"},
        {"text": "👨‍👩‍👧‍👦 Семейный полёт", "callback_data": "program_family"},
        {"text": "📋 FAQ и условия", "callback_data": "faq"},
        {"text": "⬅️ Назад", "callback_data": "back_to_main"}
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    return builder.as_markup()

def back_button(target="back_to_balloon_menu"):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data=target)
    return builder.as_markup()