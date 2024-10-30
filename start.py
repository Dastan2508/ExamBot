from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Добавить домашнее задание", callback_data="add_homework")
            ]
        ]
    )

    await message.answer(
        "Привет!",
        reply_markup=keyboard
    )