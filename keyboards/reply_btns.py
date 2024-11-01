from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

remove_btn = ReplyKeyboardRemove()


async def start_menu_btn():
    btn = ReplyKeyboardBuilder()
    btn.row(
        KeyboardButton(text="📦 Каталог товаров")
    )
    btn.row(
        KeyboardButton(text="👤 Администрация"),
        KeyboardButton(text="💬 Отзывы"),
    )

    return btn.as_markup(resize_keyboard=True)


async def select_items_list_btn(list_data: list):
    btn = ReplyKeyboardBuilder()
    btn.add(
        *[KeyboardButton(text=f"{item.name}") for item in list_data]
    )
    btn.row(
        KeyboardButton(text="🔙 Главное меню"),
    )
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)
