# main.py

import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, balloon, about, contacts, ski, booking, common

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start.router)
dp.include_router(balloon.router)
dp.include_router(about.router)
dp.include_router(contacts.router)
dp.include_router(ski.router)
dp.include_router(booking.router)
dp.include_router(common.router)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен вручную.")