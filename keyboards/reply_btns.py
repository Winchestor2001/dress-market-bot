from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


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


async def admin_menu_btn():
    pass