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


async def select_category_btn(categories: list):
    btn = ReplyKeyboardBuilder()
    btn.add(
        *[KeyboardButton(text=f"{item.name}") for item in categories]
    )
    btn.row(
        KeyboardButton(text="🔙 Главное меню"),
    )

    return btn.as_markup(resize_keyboard=True)
