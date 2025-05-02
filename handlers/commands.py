from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline_btns import subscribe_channel_btn, admin_command_btn
from keyboards.reply_btns import start_menu_btn
from utils.admin_filter import IsAdmin
from utils.is_subscribed import is_subscribed

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    await state.clear()
    btn = await start_menu_btn()
    full_name = message.from_user.full_name
    await message.answer(
        text=f"👋 Привет, {full_name}! 👋\n\n"
             "❓ Есть вопрос или предложение? Связаться с администрацией можно по соответствующей кнопке\n\n"
             "Проблемы с ботом? Пропишите /start для перезапуска или свяжитесь с администрацией",
        reply_markup=btn
    )


@router.message(IsAdmin(), Command('admin'))
async def admin_panel(message: Message, state: FSMContext):
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
        "Получение списка размеров: <code>/list_sizes</code>\n\n"

        "Число пользователей в боте: <code>/stat</code>\n"
        "Отправить рассылку: <code>/send</code>\n"
        "Список отложенных рассылок: <code>/scheduled</code>\n"
        "Экспортировать список товаров: <code>/export</code>"
    )
    btn = await admin_command_btn()
    await message.answer(
        text=f"Список команд:\n\n{commands}",
        reply_markup=btn
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


# check whether user subscribed to all channels or not
@router.callback_query(F.data == "check_subscribed")
async def check_subscribed(call: CallbackQuery):
    user_id = call.from_user.id
    channels = await is_subscribed(user_id)
    full_name = call.from_user.full_name

    if channels:
        await call.answer("Подпишитесь на наш канал 👇", show_alert=True)
        keyboard = await subscribe_channel_btn(channels)
        await call.message.delete()
        await call.message.answer(
            "Подпишитесь на наш канал 👇",
            reply_markup=keyboard
        )
    else:
        await call.answer("Благодарим вас за подписку на все необходимые каналы!")
        await call.message.delete()
        btn = await start_menu_btn()
        await call.message.answer(text=f"👋 Привет, {full_name}! 👋\n\n"
                                       "❓ Есть вопрос или предложение? Связаться с администрацией можно по соответствующей кнопке\n\n"
                                       "Проблемы с ботом? Пропишите /start для перезапуска или свяжитесь с администрацией",
                                  reply_markup=btn)
