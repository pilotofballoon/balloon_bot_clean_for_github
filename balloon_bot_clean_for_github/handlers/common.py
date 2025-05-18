# handlers/common.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from keyboards import main_menu_keyboard, balloon_menu_keyboard
from data.messages import (
    START_MESSAGE, BALLOON_MENU, ABOUT_CLUB, 
    CONTACTS_TEXT, SKI_MESSAGE, 
    FLIGHT_PROCEDURE_1, FLIGHT_PROCEDURE_2, FLIGHT_PROCEDURE_3,
    FAQ_TEXT_1
)

router = Router()

BACK_TARGETS = {
    "back_to_main": {"photo": "photos/start.jpg", "caption": START_MESSAGE},
    "back_to_balloon_menu": {"photo": "photos/balloon.jpg", "caption": BALLOON_MENU},
    "about_back": {"photo": "photos/about.JPG", "caption": ABOUT_CLUB},
    "faq_back": {"photo": "photos/faq.jpg", "caption": FAQ_TEXT_1},
    "contacts_back": {"photo": "photos/contacts.jpg", "caption": CONTACTS_TEXT},
    "ski_back": {"photo": "photos/ski.jpg", "caption": SKI_MESSAGE},
    "flight_procedure_back": {"photo": "photos/balloon.jpg", "caption": FLIGHT_PROCEDURE_1}
}

@router.callback_query(F.data.in_(BACK_TARGETS.keys()))
async def universal_back_handler(callback: CallbackQuery):
    target = BACK_TARGETS.get(callback.data)
    if not target:
        await callback.answer("❌ Неизвестная цель")
        return

    media = InputMediaPhoto(media=FSInputFile(target["photo"]), caption=target["caption"])
    try:
        await callback.message.edit_media(media=media, reply_markup=main_menu_keyboard())
    except Exception as e:
        print(f"Ошибка редактирования медиа: {e}")
        await callback.message.answer_photo(
            photo=FSInputFile(target["photo"]),
            caption=target["caption"],
            reply_markup=main_menu_keyboard()
        )
    await callback.answer()