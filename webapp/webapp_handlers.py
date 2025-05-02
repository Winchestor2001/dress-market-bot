import json
import logging

from aiogram import Router, F
from aiogram.types import Message

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "delete_product":
            product_id = data["id"]
            # await delete_product_from_db(product_id)
            await message.answer(f"Продукт с ID {product_id} успешно удалён ✅")
    except Exception as e:
        await message.answer(f"Ошибка при удалении: {str(e)}")