import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.crud import create_category_obj, get_all_categories_obj, delete_category_obj, get_all_products, \
    delete_product_by_id, get_all_categories_for_btn_obj, create_product_obj, create_size_obj, get_all_sizes_obj, \
    delete_size_obj, get_all_sizes_for_btn_obj, get_single_category_obj, update_category_dimension_obj, \
    update_product_video_review_obj, get_single_product_obj, get_all_users_obj
from keyboards.inline_btns import admin_categories_btn, admin_sizes_btn, mail_btn
from keyboards.reply_btns import remove_btn
from loader import bot
from states.management_states import ProductState, CategoryState, MailState
from utils.content_formatter import format_content

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('add_category'))
async def add_category_command(message: Message, state: FSMContext):
    await message.answer(text="Введите название категории:")
    await state.set_state(CategoryState.name)


@router.message(CategoryState.name)
async def category_name_state(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Отправьте фото для замеры:")
    await state.set_state(CategoryState.dimension_photo)


@router.message(CategoryState.dimension_photo, F.content_type.in_({'photo', 'text'}))
async def category_dimension_photo_state(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text and message.text == '.':
        dimension_photo = None
    else:
        dimension_photo = message.photo[-1].file_id
    if data.get("category_name", False):
        result = await update_category_dimension_obj(category_name=data['category_name'],
                                                     dimension_photo=dimension_photo)
    else:
        result = await create_category_obj(name=data['category'], dimension_photo=dimension_photo)
    await message.answer(text=result)
    await state.clear()


@router.message(Command('list_categories'))
async def category_list_command(message: Message):
    categories = await get_all_categories_obj()
    await message.answer(text=categories)


@router.message(Command('delete_category'))
async def delete_category_command(message: Message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer(text="Не указано ID категории для удаления.")
        return

    try:
        category_id = int(command_parts[1])
        result = await delete_category_obj(category_id)
        await message.answer(text=result)
    except ValueError:
        await message.answer(text="❌ Некорректный ID категории. Пожалуйста, введите числовое значение.")


@router.message(Command('update_zamer'))
async def update_zamer_command(message: Message, state: FSMContext):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer(text="Не указано ID категории для изменение замеры.")
        return

    try:
        category_id = int(command_parts[1])
        category = await get_single_category_obj(category_id)
        await state.set_data({"category_name": category.name})
        await message.answer("Отправьте фото для замеры:")
        await state.set_state(CategoryState.dimension_photo)
    except ValueError:
        await message.answer(text="❌ Некорректный ID категории. Пожалуйста, введите числовое значение.")


@router.message(Command('update_videoobzor'))
async def update_videoobzor_command(message: Message, state: FSMContext):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer(text="Не указано ID продукта для изменение видеообзор.")
        return

    try:
        product_id = int(command_parts[1])
        product = await get_single_product_obj(product_id)
        await state.set_data({"product_id": product.id})
        await message.answer("Отправьте видео для видеообзора:")
        await state.set_state(ProductState.waiting_for_video_review)
    except ValueError:
        await message.answer(text="❌ Некорректный ID продукт. Пожалуйста, введите числовое значение.")


@router.message(Command('list_products'))
async def list_products_command(message: Message):
    products = await get_all_products()
    await message.answer(text=products)


@router.message(Command('delete_product'))
async def delete_product_command(message: Message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer(text="Не указано ID продукта.")
        return

    product_ids = [item.strip() for item in command_parts[1].split(',')]
    result = await delete_product_by_id(product_ids)
    await message.answer(text=result)


@router.message(Command('add_product'))
async def add_product_command(message: Message, state: FSMContext):
    await message.answer("Введите название продукта:", reply_markup=remove_btn)
    await state.set_state(ProductState.waiting_for_name)


@router.message(ProductState.waiting_for_name)
async def process_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание продукта:")
    await state.set_state(ProductState.waiting_for_description)


@router.message(ProductState.waiting_for_description)
async def process_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите цену продукта:")
    await state.set_state(ProductState.waiting_for_price)


@router.message(ProductState.waiting_for_price, F.text)
async def process_product_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    categories = await get_all_categories_for_btn_obj()
    btn = await admin_categories_btn(categories)

    await message.answer(text="Выберите категорию:", reply_markup=btn)
    await state.set_state(ProductState.waiting_for_category)


@router.callback_query(F.data.startswith('select_category:'))
async def product_category_state(c: CallbackQuery, state: FSMContext):
    category_id = c.data.split(":")[1]
    await state.update_data(category_id=category_id)
    await c.answer(f"Вы выбрали категорию с ID {category_id}.", show_alert=True)

    sizes = await get_all_sizes_for_btn_obj()
    btn = await admin_sizes_btn(sizes)
    await c.message.edit_text(text="Выберите размер", reply_markup=btn)
    await state.set_state(ProductState.waiting_for_size)


@router.callback_query(ProductState.waiting_for_size, F.data.startswith('select_size:'))
async def product_size_state(c: CallbackQuery, state: FSMContext):
    size_id = c.data.split(":")[1]
    await state.update_data(size_id=size_id)
    await c.answer(f"Вы выбрали размер с ID {size_id}.", show_alert=True)

    await c.message.edit_text("Отправьте видеообзор:")
    await state.set_state(ProductState.waiting_for_video_review)


@router.message(ProductState.waiting_for_video_review, F.content_type.in_({'video', 'text'}))
async def product_video_review_state(message: Message, state: FSMContext):
    if message.text and message.text == '.':
        video_review_id = None
    else:
        video_review_id = message.video.file_id
    data = await state.get_data()
    if data.get("product_id", False):
        await state.update_data(video_review_id=video_review_id)
        result = await update_product_video_review_obj(data['product_id'], video_review_id)
        await message.answer(text=result)
        await state.clear()
        return
    else:
        await state.update_data(video_review_id=video_review_id)
    await message.answer("Отправьте фото продукта:")
    await state.set_state(ProductState.waiting_for_photo)


@router.message(ProductState.waiting_for_photo, F.content_type.in_({'photo'}))
async def product_photo_state(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer("Отправьте текст для замеры:")
    await state.set_state(ProductState.waiting_for_dimension)


@router.message(ProductState.waiting_for_dimension)
async def product_dimension_state(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')
    size_id = data.get('size_id')
    photo_id = data.get('photo_id')
    video_review_id = data.get('video_review_id')
    dimension = message.text

    await create_product_obj(name, description, price, category_id, size_id, video_review_id, photo_id, dimension)
    await message.answer("✅ Продукт успешно добавлен!")
    await state.clear()


@router.message(Command('add_size'))
async def add_size_command(message: Message, state: FSMContext):
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        await message.answer(text="Не указали размер")
        return

    size_name = command_parts[1]
    result = await create_size_obj(size_name)
    await message.answer(text=result)


@router.message(Command('list_sizes'))
async def size_list_command(message: Message):
    sizes = await get_all_sizes_obj()
    await message.answer(text=sizes)


@router.message(Command('delete_size'))
async def delete_size_command(message: Message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        await message.answer(text="Не указано ID размера для удаления.")
        return

    try:
        size_id = int(command_parts[1])
        result = await delete_size_obj(size_id)
        await message.answer(text=result)
    except ValueError:
        await message.answer(text="❌ Некорректный ID размера. Пожалуйста, введите числовое значение.")


@router.message(Command('send'))
async def mail_command(message: Message, state: FSMContext):
    context = "Отправьте пост. (для отмены /start)"
    await message.answer(text=context)
    await state.set_state(MailState.mail_message)


@router.message(MailState.mail_message)
async def mail_message_state(message: Message, state: FSMContext):
    post_type = message.content_type
    if post_type not in ('text', 'photo', 'video', 'animation'):
        return await message.answer("Неверный пост")

    content = message.html_text
    content = await format_content(content=content)
    btn = await mail_btn(content['buttons'])

    media_data = {
        'text': {'method': bot.send_message, 'params': {'text': content['message_text'], 'reply_markup': btn}},
        'photo': {
            'method': bot.send_photo,
            'params': {'photo': message.photo[-1].file_id if message.photo else None,
                       'caption': content['message_text'], 'reply_markup': btn}
        },
        'video': {
            'method': bot.send_video,
            'params': {'video': message.video.file_id if message.video else None,
                       'caption': content['message_text'], 'reply_markup': btn}
        },
        'animation': {
            'method': bot.send_animation,
            'params': {'animation': message.animation.file_id if message.animation else None,
                       'caption': content['message_text'], 'reply_markup': btn}
        }
    }

    send_method = media_data[post_type]['method']
    send_params = media_data[post_type]['params']

    users = await get_all_users_obj()
    total_users = len(users)
    sent_count = 0
    failed_count = 0
    failed_users = []

    for user in users:
        try:
            await send_method(chat_id=user['telegram_id'], **send_params)
            sent_count += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            failed_count += 1
            failed_users.append(f"{user['username']} ({user['telegram_id']})")
            logger.error(f"Ошибка при отправке пользователю {user['telegram_id']} - {user['username']}: {e}")
            continue

    report_message = (
        f"📢 Рассылка завершена!\n\n"
        f"👥 Всего пользователей: {total_users}\n"
        f"✅ Успешно отправлено: {sent_count}\n"
        f"❌ Ошибок: {failed_count}\n"
    )

    if failed_users:
        failed_list = "\n".join(failed_users[:10])
        report_message += f"\n❗ Ошибки у следующих пользователей:\n{failed_list}"

    await message.answer(text=report_message)
    await state.clear()
