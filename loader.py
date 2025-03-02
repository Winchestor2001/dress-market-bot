import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.models import db, TelegramUser, Category, VideoReview, Product, ProductSize, ScheduledPost

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db.create_tables([TelegramUser, Category,VideoReview, Product, ProductSize, ScheduledPost])
MOSCOW_TZ = pytz.timezone("Europe/Moscow")