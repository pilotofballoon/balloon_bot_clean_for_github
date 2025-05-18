# handlers/ski.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards import back_button
from data.messages import SKI_MESSAGE

router = Router()

@router.callback_query(F.data == "ski")
async def show_ski_info(callback: CallbackQuery):
    media = InputMediaPhoto(media=FSInputFile("photos/ski.jpg"), caption=SKI_MESSAGE)
    try:
        await callback.message.edit_media(media=media, reply_markup=back_button("back_to_main"))
    except Exception as e:
        print(f"Ошибка при редактировании медиа: {e}")
        await callback.message.answer_photo(
            photo=FSInputFile("photos/ski.jpg"),
            caption=SKI_MESSAGE,
            reply_markup=back_button("back_to_main")
        )
    await callback.answer()