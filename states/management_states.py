from . import *


class ProductState(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_category = State()
    waiting_for_size = State()
    waiting_for_video_review = State()
    waiting_for_photo = State()
    waiting_for_dimension = State()