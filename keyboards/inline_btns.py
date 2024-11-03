from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from keyboards.callback_data import ProductCallback


async def support_btn():
    btn = InlineKeyboardBuilder()
    btn.add(
        InlineKeyboardButton(text="👤 steroidik", url="https://t.me/steroidik"),
        InlineKeyboardButton(text="👤 pppeeexxx", url="https://t.me/pppeeexxx"),
    )
    btn.adjust(1)
    return btn.as_markup()


async def feedback_btn():
    btn = InlineKeyboardBuilder()
    btn.add(
        InlineKeyboardButton(text="🌟 Отзывы в VK #1", url="https://vk.com/wall442619801_625"),
        InlineKeyboardButton(text="🌟 Отзывы в VK #2", url="https://vk.com/photo259231216_457359976")
    )
    btn.adjust(1)
    return btn.as_markup()


async def admin_categories_btn(categories):
    btn = InlineKeyboardBuilder()

    for category in categories:
        btn.add(InlineKeyboardButton(text=category.name, callback_data=f"select_category:{category.id}"))

    return btn.as_markup()


async def admin_sizes_btn(sizes):
    btn = InlineKeyboardBuilder()

    for size in sizes:
        btn.add(InlineKeyboardButton(text=size.name, callback_data=f"select_size:{size.id}"))

    return btn.as_markup()


async def product_btn(product_id: int):
    btn = InlineKeyboardBuilder()
    btn.add(
        InlineKeyboardButton(
            text="🎥 Видеообзор",
            callback_data=ProductCallback(action="video", item_id=product_id).pack()
        ),
        InlineKeyboardButton(
            text="📏 Замеры",
            callback_data=ProductCallback(action="dimension", item_id=product_id).pack()
        ),
    )
    btn.adjust(2)
    return btn.as_markup()

