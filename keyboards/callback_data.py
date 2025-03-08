from aiogram.filters.callback_data import CallbackData


class ProductCallback(CallbackData, prefix='product'):
    action: str
    item_id: int


class MailOptionCallback(CallbackData, prefix='mail_option'):
    schedule: bool


class ProductAddOptionCallback(CallbackData, prefix='product_add_option'):
    import_product: bool
