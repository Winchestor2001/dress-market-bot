from typing import Any, Dict, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from database.crud import create_user_obj

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        await create_user_obj(
            telegram_id=event.from_user.id,
            username=event.from_user.username,
        )
        return await handler(event, data)
