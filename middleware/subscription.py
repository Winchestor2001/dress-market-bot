from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types
from aiogram.enums import ChatType

from keyboards.inline_btns import subscribe_channel_btn
from utils.is_subscribed import is_subscribed


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message) and event.chat.type == ChatType.PRIVATE:
            user_id = event.from_user.id
            channels = await is_subscribed(user_id)

            if channels:
                keyboard = await subscribe_channel_btn(channels)

                await event.answer(
                    "Подпишитесь на наш канал 👇",
                    reply_markup=keyboard
                )
                return  # Stop processing further handlers if not subscribed

        return await handler(event, data)
