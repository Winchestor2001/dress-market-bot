from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline_btns import feedback_btn

router = Router()


@router.message(F.text == "💬 Отзывы")
async def feedback_handler(message: Message):
    context = ("💬 <b>Отзывы наших клиентов</b>\n\n"
               "Мы ценим ваше мнение и всегда рады обратной связи! Ознакомьтесь с реальными отзывами наших клиентов.")
    btn = await feedback_btn()
    await message.answer(text=context, reply_markup=btn)

