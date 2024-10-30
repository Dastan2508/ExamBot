# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot_config import BOT_TOKEN
from start import start_router
from home_work import homework_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(homework_router)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())