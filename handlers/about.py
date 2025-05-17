# handlers/about.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile  # ⬅️ Эти импорты были упущены
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.messages import ABOUT_CLUB
from keyboards import main_menu_keyboard

router = Router()

@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    kb = [{"text": "⬅️ Назад", "callback_data": "main_menu"}]
    builder = InlineKeyboardBuilder()
    for btn in kb:
        builder.button(**btn)
    builder.adjust(1)

    media = InputMediaPhoto(media=FSInputFile("photos/about.JPG"), caption=ABOUT_CLUB)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())