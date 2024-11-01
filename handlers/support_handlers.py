from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline_btns import support_btn

router = Router()


@router.message(F.text == "👤 Администрация")
async def support_handler(message: Message):
    context = "По всем вопросам и предложениям пишите 👇"
    btn = await support_btn()
    await message.answer(text=context, reply_markup=btn)

