# main.py
from aiogram import Bot, Dispatcher
from handlers import start, balloon, contacts, booking, about, ski, common  # ⬅️ common должен быть здесь
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(start.router)
dp.include_router(balloon.router)
dp.include_router(contacts.router)
dp.include_router(booking.router)
dp.include_router(about.router)
dp.include_router(ski.router)
dp.include_router(common.router)  # ⬅️ Должен быть подключен

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))