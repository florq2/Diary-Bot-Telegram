from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot import bot
from app.recognizers import audio_to_text, save_as_mp3
from app.chatgpt_request import get_response
from app.keyboards import start_keyboard, finish_keyboard, back_keyboard, dates_keyboard
from app.workout import (save_user_exercise, get_user_exercises, clear_user_exercises, add_new_user,
                         change_last_msg_id, get_last_msg_id, delete_last_msg_id)
import app.database as db

router = Router()


class Workout(StatesGroup):
    workout = State()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать!\n"
                         "Я помогу Вам вести дневник тренировок.\n"
                         "Расскажите мне о выполненном подходе в обычном или голосовом сообщении.",
                         reply_markup=start_keyboard)
    await add_new_user(message)
    await db.add_new_user(message)


@router.message(F.text == "Начать тренировку 🏆")
async def start_workout(message: types.Message, state: FSMContext):
    await state.set_state(Workout.workout)
    await message.answer("Вы начали новую тренировку!\n"
                         "Расскажите о выполненном подходе.",
                         reply_markup=finish_keyboard)


@router.message(F.text == "Закончить тренировку 🏁")
async def start_workout(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы закончили очередную тренировку!\n"
                         "Продолжайте в том же духе!",
                         reply_markup=start_keyboard)
    await db.add_new_workout(message)
    await clear_user_exercises(message)
    await delete_last_msg_id(message)


@router.message(F.text == "Удалить запись ❌")
async def delete_exercise(message: types, state: FSMContext):
    await state.clear()
    await message.answer("Запись была удалена!",
                         reply_markup=start_keyboard)
    await clear_user_exercises(message)
    await delete_last_msg_id(message)


@router.message(F.text == "История тренировок 🗓")
async def start_workout(message: types.Message, state: FSMContext):
    dates = await db.get_dates(message)
    keyboard = await dates_keyboard(dates)
    await message.answer("Выберите дату тренировки:",
                         reply_markup=keyboard)


@router.message(Workout.workout)
async def voice_msg(message: types.Message):
    if message.voice:
        voice_path = await save_as_mp3(message)
        transcript_voice = await audio_to_text(voice_path)

        text = await get_response(transcript_voice)
    elif message.text:
        text = await get_response(str(message.text))
    else:
        text = "Ошибка"

    if "Ошибка" in text:
        await message.answer("Возникла ошибка. Пожалуйста, отправьте сообщение еще раз.")
    else:
        await save_user_exercise(message, text)

        msg = await get_user_exercises(message)

        if await get_last_msg_id(message) is not None:
            await bot.delete_message(message.chat.id, await get_last_msg_id(message))

        last_msg = await message.answer(msg)
        await change_last_msg_id(message, last_msg.message_id)


@router.callback_query()
async def callback_query(callback: CallbackQuery):
    exercises = await db.get_exercises(callback, callback.data)

    text = exercises[0][0]

    if len(exercises) > 1:
        text = ""
        num = 1
        for exercise in exercises:
            text += f"Тренировка №{num}:\n"
            text += exercise[0] + "\n"
            num += 1

    dates = await db.get_dates(callback)
    keyboard = await dates_keyboard(dates)

    await callback.answer(f"Ваша тренировка за {callback.data}")
    await callback.message.edit_text(f"Ваша тренировка за {callback.data}:\n\n" + text, reply_markup=keyboard)
