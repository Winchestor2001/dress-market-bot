from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from keyboards.callback_data import ManagementCallback


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
        InlineKeyboardButton(text="🌟 Отзыв на VK", url="https://vk.com/wall442619801_625"),
        InlineKeyboardButton(text="🌟 Фотоотзыв на VK", url="https://vk.com/photo259231216_457359976")
    )
    btn.adjust(1)
    return btn.as_markup()


async def admin_categories_btn(categories):
    btn = InlineKeyboardBuilder()

    for category in categories:
        btn.add(InlineKeyboardButton(text=category.name, callback_data=f"select_category:{category.id}"))

    return btn.as_markup()
