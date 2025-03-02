import asyncio
import json
from datetime import datetime
import logging

from aiogram.types import InlineKeyboardMarkup

from database.crud import get_all_users_obj, get_scheduled_posts, delete_scheduled_post
from loader import bot, MOSCOW_TZ

logger = logging.getLogger(__name__)


async def send_post(chat_id: int, post: dict):
    """
    Отправляет сообщение пользователю в зависимости от типа контента.
    :param chat_id: Telegram ID пользователя
    :param post: Словарь с данными поста
    """
    post_type = post["post_type"]
    content = post["content"]
    buttons = post.get("buttons")

    if isinstance(buttons, str):
        try:
            buttons = InlineKeyboardMarkup(**json.loads(buttons))
        except json.JSONDecodeError:
            buttons = None

    media_data = {
        "text": {"method": bot.send_message, "params": {"text": content, "reply_markup": buttons}},
        "photo": {
            "method": bot.send_photo,
            "params": {"photo": content, "caption": content, "reply_markup": buttons},
        },
        "video": {
            "method": bot.send_video,
            "params": {"video": content, "caption": content, "reply_markup": buttons},
        },
        "animation": {
            "method": bot.send_animation,
            "params": {"animation": content, "caption": content, "reply_markup": buttons},
        },
    }

    send_method = media_data[post_type]["method"]
    send_params = media_data[post_type]["params"]

    try:
        await send_method(chat_id=chat_id, **send_params)
        await asyncio.sleep(0.5)  # Защита от спама Telegram API
    except Exception as e:
        print(f"❌ Ошибка при отправке пользователю {chat_id}: {e}")


async def check_scheduled_posts():
    logger.info("Schedule запушен")
    while True:
        try:
            now = datetime.now(MOSCOW_TZ)
            scheduled_posts = await get_scheduled_posts(now)

            for post in scheduled_posts:
                users = await get_all_users_obj()
                for user in users:
                    try:
                        await send_post(user['telegram_id'], post)
                    except Exception as e:
                        logger.error(f"❌ Ошибка при отправке пользователю {user['telegram_id']}: {e}")

                await delete_scheduled_post(post['id'])

        except Exception as e:
            logger.error(f"❌ Ошибка в `check_scheduled_posts()`: {e}")

        await asyncio.sleep(10)
