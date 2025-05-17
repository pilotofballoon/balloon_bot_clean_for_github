# main.py

import asyncio
from aiogram import Bot, Dispatcher

# Токен из .env
from config import BOT_TOKEN

# Создаем бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутеры
from handlers import start, balloon, contacts, booking, about, ski, common

dp.include_router(start.router)
dp.include_router(balloon.router)
dp.include_router(contacts.router)
dp.include_router(booking.router)
dp.include_router(about.router)
dp.include_router(ski.router)
dp.include_router(common.router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())