# about.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards import back_button_keyboard

router = Router()

@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    about_text = """
ℹ️ *О Нас*
Мы занимаемся полетами на воздушных шарах в Сочи и обучением катанию на горных лыжах.
"""
    media = InputMediaPhoto(media=FSInputFile("photos/about.jpg"), caption=about_text)
    await callback.message.edit_media(media=media, reply_markup=back_button_keyboard("back_to_main"))