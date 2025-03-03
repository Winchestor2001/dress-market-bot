import asyncio
import json
from datetime import datetime
import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    file_id = post.get("file_id")

    try:
        content = json.loads(post["content"]) if isinstance(post["content"], str) else post["content"]
    except json.JSONDecodeError:
        logger.info(f"❌ Ошибка JSON в `content` для поста {post['id']}")
        return

    message_text = content.get("message_text", "Без текста")
    buttons = content.get("buttons", None)

    if buttons:
        buttons = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=btn['text'], url=btn['link'])] for btn in buttons]
        )
    else:
        buttons = None

    if post_type == "text":
        await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=buttons)
        return

    media_methods = {
        "photo": bot.send_photo,
        "video": bot.send_video,
        "animation": bot.send_animation,
    }
    if post_type in media_methods and file_id:
        try:
            if post_type == "photo":
                await media_methods[post_type](chat_id=chat_id, photo=file_id, caption=message_text, reply_markup=buttons)
            elif post_type == "video":
                await media_methods[post_type](chat_id=chat_id, video=file_id, caption=message_text, reply_markup=buttons)
            elif post_type == "animation":
                await media_methods[post_type](chat_id=chat_id, animation=file_id, caption=message_text, reply_markup=buttons)
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.info(f"❌ Ошибка при отправке {post_type} пользователю {chat_id}: {e}")


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
