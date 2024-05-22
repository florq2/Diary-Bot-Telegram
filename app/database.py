from aiogram import types
import sqlite3 as sq

from aiogram.types import user

from app.workout import get_user_exercises


async def create_tables():
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date_id INTEGER,
            user_id INTEGER,
            exercise TEXT,
            FOREIGN KEY (workout_date_id) REFERENCES workout_dates(id)
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

    db.commit()
    db.close()


async def add_new_user(message: types.Message):
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    user_id = int(message.from_user.id)
    user_name = str(message.from_user.username)

    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
                   (user_id, user_name))

    db.commit()
    db.close()


async def add_new_workout(message: types.Message):
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    user_id = int(message.from_user.id)
    date = str(message.date.date())

    exercise = await get_user_exercises(message)

    if exercise == "":
        return

    cursor.execute("SELECT id FROM workout_dates WHERE user_id = ? AND date = ?",
                   (user_id, date))
    row = cursor.fetchone()

    if row:
        workout_date_id = row[0]
    else:
        cursor.execute("INSERT OR IGNORE INTO workout_dates (user_id, date) VALUES (?, ?)",
                       (user_id, date))
        workout_date_id = cursor.lastrowid

    cursor.execute("INSERT INTO workout_entries (workout_date_id, user_id, exercise) VALUES (?, ?, ?)",
                   (workout_date_id, user_id, exercise))

    db.commit()
    db.close()


async def get_dates(message: types.Message):
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    user_id = int(message.from_user.id)

    cursor.execute("SELECT date FROM workout_dates WHERE user_id = ?", (user_id, ))
    dates = cursor.fetchall()

    db.close()

    return dates


async def get_date_id(user_id: int, date: str) -> int:
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    cursor.execute("SELECT id FROM workout_dates WHERE user_id = ? and date = ?", (user_id, date))
    date_id = cursor.fetchone()

    return date_id[0]


async def get_exercises(message: types.Message, date: str):
    db = sq.connect('data/workout_diary.db')
    cursor = db.cursor()

    user_id = int(message.from_user.id)
    date_id = await get_date_id(user_id, date)

    cursor.execute("SELECT exercise FROM workout_entries WHERE user_id = ? AND workout_date_id = ?",
                   (user_id, date_id))
    exercises = cursor.fetchall()

    return exercises
