import asyncio
import logging

from aiogram import types
from handlers import routers_list
from loader import bot, dp


async def set_bot_menu():
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="♻️ Запустить бота")
        ]
    )


async def main():
    await set_bot_menu()
    dp.include_routers(*routers_list)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
