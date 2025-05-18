# handlers/about.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards import back_button
from data.messages import ABOUT_CLUB

router = Router()

@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/about.JPG"), caption=ABOUT_CLUB)
    await callback.message.edit_media(media=media, reply_markup=back_button("back_to_main"))