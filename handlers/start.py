# start.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards import main_menu_keyboard
from data.messages import START_MESSAGE

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile("photos/start.jpg"),
        caption=START_MESSAGE,
        reply_markup=main_menu_keyboard()
    )