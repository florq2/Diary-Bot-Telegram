from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Начать тренировку 🏆")],
                                               [KeyboardButton(text="История тренировок 🗓")]],
                                     resize_keyboard=True,
                                     input_field_placeholder="Жду указаний...")

finish_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить тренировку 🏁")],
                                                [KeyboardButton(text="Удалить запись ❌")]],
                                      resize_keyboard=True,
                                      input_field_placeholder="Расскажите о подходе.")

back_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Назад ❌")]],
                                    resize_keyboard=True,
                                    input_field_placeholder="Введите дату тренировки...")


async def dates_keyboard(dates):
    builder = InlineKeyboardBuilder()

    for date in dates:
        builder.button(text=date[0], callback_data=date[0])

    return builder.adjust(2).as_markup()
