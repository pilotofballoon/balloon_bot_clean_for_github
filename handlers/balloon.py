# handlers/balloon.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputMediaPhoto, FSInputFile
from data.messages import BALLOON_MENU, PROGRAM_SOLO, PROGRAM_GROUP, PROGRAM_FAMILY, FAQ_TEXT

router = Router()

@router.callback_query(F.data == "balloon_menu")
async def balloon_menu(callback: CallbackQuery):
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
    media = InputMediaPhoto(media=FSInputFile("photos/balloon.jpg"), caption=BALLOON_MENU)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@router.callback_query(F.data.in_(["program_solo", "program_group", "program_family", "faq"]))
async def show_program(callback: CallbackQuery):
    data_map = {
        "program_solo": {"photo": "photos/solo.jpg", "caption": PROGRAM_SOLO},
        "program_group": {"photo": "photos/group.jpg", "caption": PROGRAM_GROUP},
        "program_family": {"photo": "photos/family.jpg", "caption": PROGRAM_FAMILY},
        "faq": {"photo": "photos/faq.jpg", "caption": FAQ_TEXT}
    }

    if callback.data in data_map:
        info = data_map[callback.data]
        media = InputMediaPhoto(media=FSInputFile(info["photo"]), caption=info["caption"])
        
        kb = []
        if callback.data != "faq":
            kb.append({"text": "📅 Забронировать", "callback_data": f"book_{callback.data.split('_')[1]}"})
        
        kb.append({"text": "⬅️ Назад", "callback_data": "balloon_menu"})
        
        builder = InlineKeyboardBuilder()
        for btn in kb:
            builder.button(**btn)
        builder.adjust(1)
        await callback.message.edit_media(media=media, reply_markup=builder.as_markup())