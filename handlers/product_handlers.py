from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.crud import get_all_categories_for_btn_obj, is_category_name_exists
from keyboards.reply_btns import select_category_btn
from states.user_states import UserMarketState

router = Router()


@router.message(F.text == "📦 Каталог товаров")
async def category_handler(message: Message, state: FSMContext):
    categories = await get_all_categories_for_btn_obj()
    context = "Выберите категорию 👇"
    btn = await select_category_btn(categories)
    await message.answer(text=context, reply_markup=btn)
    await state.set_state(UserMarketState.category)


@router.message(UserMarketState.category)
async def category_handler(message: Message, state: FSMContext):
    category = message.text
    if await is_category_name_exists(category):
        await state.update_data(category=category)
    else:
        await message.answer(text="Категория не найдена")