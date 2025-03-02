from aiogram.filters.callback_data import CallbackData


class ProductCallback(CallbackData, prefix='product'):
    action: str
    item_id: int


class MailOptionCallback(CallbackData, prefix='mail_option'):
    schedule: bool