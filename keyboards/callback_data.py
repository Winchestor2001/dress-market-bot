from aiogram.filters.callback_data import CallbackData


class ManagementCallback(CallbackData, prefix='management'):
    action: str
    entity: int
    item_id: int