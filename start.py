from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command(commands=["start"]))
async def send_welcome(message: Message):
    await message.answer("Привет! Я ваш бот. Чем могу помочь?")
