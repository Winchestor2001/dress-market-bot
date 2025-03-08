from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from keyboards.callback_data import ProductCallback, MailOptionCallback, ProductAddOptionCallback


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


async def product_btn(product_id: int, contact: str):
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
        InlineKeyboardButton(
            text="💸 Купить",
            url=contact
        ),
    )
    btn.adjust(2)
    return btn.as_markup()


async def add_product_type_btn():
    btn = InlineKeyboardBuilder()
    btn.add(
        InlineKeyboardButton(
            text="Ручной",
            callback_data=ProductAddOptionCallback(import_product=False).pack()
        ),
        InlineKeyboardButton(
            text="Импортировать",
            callback_data=ProductAddOptionCallback(import_product=True).pack()
        ),
    )
    btn.adjust(1)
    return btn.as_markup()


async def mail_options_btn():
    btn = InlineKeyboardBuilder()
    btn.add(
        InlineKeyboardButton(text="📝 Простая отправка", callback_data=MailOptionCallback(schedule=False).pack()),
        InlineKeyboardButton(text="🕔 Отложенная отправка", callback_data=MailOptionCallback(schedule=True).pack()),
    )
    btn.adjust(1)
    return btn.as_markup()

async def mail_btn(buttons: list):
    btn = InlineKeyboardBuilder()
    btn.add(
        *[InlineKeyboardButton(text=item['text'], url=item['link']) for item in buttons]
    )
    btn.adjust(1)
    return btn.as_markup()
