# contacts.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards import back_button_keyboard
from data.messages import CONTACTS_TEXT

router = Router()

@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/contacts.jpg"), caption=CONTACTS_TEXT)
    await callback.message.edit_media(media=media, reply_markup=back_button_keyboard("back_to_main"))