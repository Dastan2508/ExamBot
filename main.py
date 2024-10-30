import asyncio
import logging

from start import start_router
from home_work import homework_router
from aiogram import Bot

from bot_config import bot, dp, database


async def start_db():
    print("База данных созданнна")
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(homework_router)

    dp.startup.register(start_db)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())