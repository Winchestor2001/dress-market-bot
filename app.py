import asyncio
import logging

from aiogram import types
from aiohttp import web

from handlers import routers_list
from loader import bot, dp
from middleware.auth import AuthMiddleware
from middleware.subscription import SubscriptionMiddleware
from utils.schedule_module import check_scheduled_posts
from webapp.web_server import handle_get_products, cors_middleware


async def set_bot_menu():
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="♻️ Запустить бота")
        ]
    )


async def start_web_server():
    app = web.Application(middlewares=[cors_middleware])
    app.add_routes([web.get('/get-products', handle_get_products)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    logging.info("🌐 AIOHTTP сервер запущен на http://0.0.0.0:8000")


async def main():
    await set_bot_menu()
    dp.message.middleware.register(AuthMiddleware())
    dp.message.middleware.register(SubscriptionMiddleware())
    dp.include_routers(*routers_list)
    asyncio.ensure_future(check_scheduled_posts())
    await start_web_server()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную")
