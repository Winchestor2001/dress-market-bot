from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import ADMINS
from keyboards.reply_btns import start_menu_btn, admin_menu_btn

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    btn = await start_menu_btn()
    full_name = message.from_user.full_name
    await message.answer(
        text=f"👋 Привет, {full_name}! 👋\n\n"
             "❓ Есть вопрос или предложение? Связаться с администрацией можно по соответствующей кнопке\n\n"
             "Проблемы с ботом? Пропишите /start для перезапуска или свяжитесь с администрацией",
        reply_markup=btn
    )


@router.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id in ADMINS:
        btn = await admin_menu_btn()
        full_name = message.from_user.full_name
        await message.answer(
            text=f"👋 Привет, {full_name}! 👋\n\nВы в админ панеле",
            reply_markup=btn
        )

