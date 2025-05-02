import asyncio
import logging

from aiogram import types
from handlers import routers_list
from loader import bot, dp
from middleware.auth import AuthMiddleware
from middleware.subscription import SubscriptionMiddleware
from utils.schedule_module import check_scheduled_posts


async def set_bot_menu():
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="♻️ Запустить бота")
        ]
    )


async def main():
    await set_bot_menu()
    dp.message.middleware.register(AuthMiddleware())
    dp.message.middleware.register(SubscriptionMiddleware())
    dp.include_routers(*routers_list)
    asyncio.ensure_future(check_scheduled_posts())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную")
