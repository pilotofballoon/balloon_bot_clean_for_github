# handlers/balloon.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import back_button
from data.messages import (
    BALLOON_MENU, PROGRAM_SOLO, PROGRAM_GROUP, PROGRAM_FAMILY,
    FAQ_TEXT_1, FAQ_TEXT_2, FAQ_TEXT_3, FAQ_TEXT_4, FAQ_TEXT_5,
    FLIGHT_PROCEDURE_1, FLIGHT_PROCEDURE_2, FLIGHT_PROCEDURE_3
)

router = Router()

@router.callback_query(F.data == "balloon_menu")
async def balloon_menu(callback: CallbackQuery):
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
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=BALLOON_MENU)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@router.callback_query(F.data.in_(["program_solo", "program_group", "program_family", "faq"]))
async def show_program(callback: CallbackQuery):
    data_map = {
        "program_solo": {"photo": "photos/solo.jpg", "caption": PROGRAM_SOLO},
        "program_group": {"photo": "photos/group.jpg", "caption": PROGRAM_GROUP},
        "program_family": {"photo": "photos/family.jpg", "caption": PROGRAM_FAMILY},
        "faq": {"photo": "photos/faq.jpg", "caption": FAQ_TEXT_1}
    }
    info = data_map[callback.data]
    media = InputMediaPhoto(media=FSInputFile(info["photo"]), caption=info["caption"])
    
    kb = []
    if callback.data != "faq":
        kb.append({"text": "📅 Забронировать", "callback_data": f"book_{callback.data.split('_')[1]}"})
    
    # Если FAQ, добавляем кнопку "Далее"
    if callback.data == "faq":
        kb.append({"text": "➡️ Далее", "callback_data": "faq_part_2"})
    
    kb.append({"text": "⬅️ Назад", "callback_data": "balloon_menu"})
    
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- Часть 2 FAQ ---
@router.callback_query(F.data == "faq_part_2")
async def show_faq_part2(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/faq.jpg"), caption=FAQ_TEXT_2)
    kb = [
        {"text": "➡️ Далее", "callback_data": "faq_part_3"},
        {"text": "⬅️ Назад", "callback_data": "faq"}
            ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- Часть 3 FAQ ---
@router.callback_query(F.data == "faq_part_3")
async def show_faq_part3(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/faq.jpg"), caption=FAQ_TEXT_3)
    kb = [
        {"text": "➡️ Далее", "callback_data": "faq_part_4"},
        {"text": "⬅️ Назад", "callback_data": "faq_part_2"}
            ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- Часть 4 FAQ ---
@router.callback_query(F.data == "faq_part_4")
async def show_faq_part4(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/faq.jpg"), caption=FAQ_TEXT_4)
    kb = [
        {"text": "➡️ Далее", "callback_data": "faq_part_5"},
        {"text": "⬅️ Назад", "callback_data": "faq_part_3"}
            ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- Часть 5 FAQ ---
@router.callback_query(F.data == "faq_part_5")
async def show_faq_part5(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/faq.jpg"), caption=FAQ_TEXT_5)
    kb = [
        {"text": "⬅️ Назад", "callback_data": "faq_part_4"},
        {"text": "🏠 В меню", "callback_data": "balloon_menu"}
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())
    
@router.callback_query(F.data == "show_flight_procedure")
async def show_flight_procedure(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=FLIGHT_PROCEDURE_1)
    kb = [{"text": "➡️ Далее", "callback_data": "flight_page_2"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())
    
@router.callback_query(F.data == "flight_page_2")
async def show_flight_procedure_page2(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=FLIGHT_PROCEDURE_2)
    kb = [
        {"text": "➡️ Далее", "callback_data": "flight_page_3"},
        {"text": "⬅️ Назад", "callback_data": "flight_page_1"}
        
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@router.callback_query(F.data == "flight_page_3")
async def show_flight_procedure_page3(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=FLIGHT_PROCEDURE_3)
    kb = [
        {"text": "⬅️ Назад", "callback_data": "flight_page_2"},
        {"text": "🏠 В меню", "callback_data": "balloon_menu"}
    ]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())