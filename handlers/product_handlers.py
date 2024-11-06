from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from unicodedata import category

from database.crud import get_all_categories_for_btn_obj, is_category_name_exists, get_all_sizes_for_btn_obj, \
    is_size_name_exists, get_filtered_products, get_product_video_review, get_product_dimension
from keyboards.callback_data import ProductCallback
from keyboards.inline_btns import product_btn
from keyboards.reply_btns import select_items_list_btn
from states.user_states import UserMarketState

router = Router()


@router.message(F.text == "📦 Каталог товаров")
async def category_handler(message: Message, state: FSMContext):
    categories = await get_all_categories_for_btn_obj()
    context = "Выберите категорию 👇"
    btn = await select_items_list_btn(categories)
    await message.answer(text=context, reply_markup=btn)
    await state.set_state(UserMarketState.category)


@router.message(UserMarketState.category)
async def category_handler(message: Message, state: FSMContext):
    category = message.text
    if await is_category_name_exists(category):
        await state.update_data(category=category)
        sizes = await get_all_sizes_for_btn_obj()
        context = "Выберите размер 👇"
        btn = await select_items_list_btn(sizes)
        await message.answer(text=context, reply_markup=btn)
        await state.set_state(UserMarketState.size)
    else:
        await message.answer(text="Категория не найдена")


@router.message(UserMarketState.size)
async def size_handler(message: Message, state: FSMContext):
    size = message.text
    if await is_size_name_exists(size):
        data = await state.get_data()
        result = await get_filtered_products(category_name=data['category'], size_name=size)

        if isinstance(result, str):
            await message.answer(result)
            return

        for item in result:
            product_text = (
                f"📦 <b>Название:</b> {item['name']}\n"
                f"📝 <b>Описание:</b> {item['description']}\n"
                f"💰 <b>Цена:</b> {item['price']} руб\n"
                f"📏 <b>Размер:</b> {item['size_id']}\n"
                f"📂 <b>Категория:</b> {item['category']}\n"
            )
            btn = await product_btn(item['id'])
            await message.answer_photo(
                photo=item['photo'],
                caption=product_text,
                reply_markup=btn
            )


@router.callback_query(ProductCallback.filter())
async def product_callback(c: CallbackQuery, state: FSMContext):
    cd, action, item_id = c.data.split(":")
    if action == "video":
        video = await get_product_video_review(product_id=int(item_id))
        if video:
            await c.answer()
            await c.message.reply_video(video=video)
        else:
            await c.answer("Еще нет видеообзора", show_alert=True)
    else:
        await c.answer()
        dimension, dimension_photo = await get_product_dimension(product_id=int(item_id))
        if dimension_photo:
            await c.message.reply_photo(photo=dimension_photo, caption=dimension)
        else:
            await c.message.reply_text(text=dimension)


