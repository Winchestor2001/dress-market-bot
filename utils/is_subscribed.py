import logging

from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError
from loader import bot


async def is_subscribed(user_id):
    channels = [
        {
            "id": -1001928126577,
            "name": "TIME2BUY",
            "link": "https://t.me/time222buy"
        },
        {
            "id": -1001721323404,
            "name": "CASUAL STORE BY PEH",
            "link": "https://t.me/casualstorebypeh"
        }
    ]
    not_subscribed_channels = []
    for channel in channels:
        try:
            chat_member = await bot.get_chat_member(channel['id'], user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                not_subscribed_channels.append(channel)
        except TelegramForbiddenError as er:
            text = f"Ошибка при проверке подписки на канал {channel['name']}({channel['channel_url']}): {er}"
            logging.info(text)
            continue
        except TelegramAPIError as e:
            text = f"Ошибка при проверке подписки на канал {channel['name']}({channel['link']}): {e}"
            logging.info(text)

    return not_subscribed_channels
