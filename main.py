import asyncio
import logging
from aiogram import Dispatcher

from bot import bot
from app.handlers import router
from app.database import create_tables


async def run():
    await create_tables()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Disabled")
