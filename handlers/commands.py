from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINS
from database.crud import create_user_obj
from keyboards.reply_btns import start_menu_btn

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    btn = await start_menu_btn()
    await create_user_obj(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )
    full_name = message.from_user.full_name
    await message.answer(
        text=f"👋 Привет, {full_name}! 👋\n\n"
             "❓ Есть вопрос или предложение? Связаться с администрацией можно по соответствующей кнопке\n\n"
             "Проблемы с ботом? Пропишите /start для перезапуска или свяжитесь с администрацией",
        reply_markup=btn
    )


@router.message(Command('admin'))
async def admin_panel(message: Message, state: FSMContext):
    if message.from_user.id in ADMINS:

        commands = (
            "Добавление категории: <code>/add_category</code>\n"
            "Удаление категории: <code>/delete_category id_категории</code>\n"
            "Изменить замеры: <code>/update_zamer id_категории</code>\n"
            "Получение списка категорий: <code>/list_categories</code>\n\n"

            "Добавление продукта: <code>/add_product</code>\n"
            "Удаление продукта: <code>/delete_product id_продукта</code>\n"
            "Изменить видеообзор: <code>/update_videoobzor id_продукта</code>\n"
            "Получение списка продуктов: <code>/list_products</code>\n\n"

            "Добавление размера: <code>/add_size название_размера</code>\n"
            "Удаление размера: <code>/delete_size id_размера</code>\n"
            "Получение списка размеров: <code>/list_sizes</code>"
        )
        await message.answer(
            text=f"Список команд:\n\n{commands}"
        )


@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    btn = await start_menu_btn()
    await message.answer(text="❌ Процесс отменен", reply_markup=btn)


@router.message(F.text == "🔙 Главное меню")
async def main_menu_handler(message: Message, state: FSMContext):
    await state.clear()
    btn = await start_menu_btn()
    await message.answer(text="Вы вернулись в главное меню", reply_markup=btn)