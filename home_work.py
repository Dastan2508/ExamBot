# homework_handler.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from database import create_db, save_homework  # Импортируем функции работы с БД

homework_router = Router()

# Список групп
GROUPS = ["Python 46-01", "Python 46-02", "Python 46-03"]

# Состояния диалога
class HomeworkStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_group = State()
    waiting_for_homework_number = State()
    waiting_for_github_link = State()

# Создаем базу данных при старте
create_db()

# Начинаем диалог по команде /homework
@homework_router.message(Command(commands=["homework"]))
async def start_homework(message: Message, state: FSMContext):
    await message.answer("Введите, пожалуйста, своё имя.")
    await state.set_state(HomeworkStates.waiting_for_name)

# Шаг 1: Получаем имя пользователя
@homework_router.message(HomeworkStates.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    # Отправляем список групп
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=group) for group in GROUPS]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Выберите вашу группу:", reply_markup=keyboard)
    await state.set_state(HomeworkStates.waiting_for_group)

# Шаг 2: Получаем выбранную группу
@homework_router.message(HomeworkStates.waiting_for_group, F.text.in_(GROUPS))
async def get_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)

    # Запрашиваем номер домашнего задания
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=str(i)) for i in range(1, 9)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Введите номер домашнего задания (от 1 до 8):", reply_markup=keyboard)
    await state.set_state(HomeworkStates.waiting_for_homework_number)

# Шаг 3: Получаем номер домашнего задания
@homework_router.message(HomeworkStates.waiting_for_homework_number, F.text.isdigit())
async def get_homework_number(message: Message, state: FSMContext):
    if 1 <= int(message.text) <= 8:
        await state.update_data(homework_number=int(message.text))
        await message.answer("Отправьте ссылку на GitHub репозиторий.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[],  # Пустой список клавиш, если не нужно ничего показывать
            resize_keyboard=True,
            one_time_keyboard=True
        ))
        await state.set_state(HomeworkStates.waiting_for_github_link)
    else:
        await message.answer("Введите корректный номер домашнего задания (от 1 до 8).")

# Шаг 4: Получаем ссылку на GitHub
@homework_router.message(HomeworkStates.waiting_for_github_link, F.text.startswith("https://"))
async def get_github_link(message: Message, state: FSMContext):
    await state.update_data(github_link=message.text)
    user_data = await state.get_data()

    # Сохраняем данные в базу данных
    save_homework(user_data['name'], user_data['group'], user_data['homework_number'], user_data['github_link'])

    # Формируем и отправляем итоговое сообщение
    result_message = (
        f"Домашнее задание успешно отправлено!\n\n"
        f"Имя: {user_data['name']}\n"
        f"Группа: {user_data['group']}\n"
        f"Номер домашнего задания: {user_data['homework_number']}\n"
        f"Ссылка на GitHub: {user_data['github_link']}"
    )
    await message.answer(result_message)
    await state.clear()  # Завершаем состояние

# Обработка неверного выбора на шаге с выбором группы
@homework_router.message(HomeworkStates.waiting_for_group)
async def invalid_group(message: Message):
    await message.answer("Пожалуйста, выберите группу из предложенного списка.")

# Обработка неверной ссылки
@homework_router.message(HomeworkStates.waiting_for_github_link)
async def invalid_github_link(message: Message):
    await message.answer("Пожалуйста, отправьте корректную ссылку на GitHub, начинающуюся с https://")
