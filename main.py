import asyncio
from aiogram import Bot, Dispatcher

# Импортируем роутеры
from handlers import start, balloon, contacts, booking, about, ski, common
import config

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем все роутеры
    dp.include_router(start.router)
    dp.include_router(balloon.router)
    dp.include_router(contacts.router)
    dp.include_router(booking.router)
    dp.include_router(about.router)
    dp.include_router(ski.router)
    dp.include_router(common.router)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())