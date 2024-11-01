from peewee import *

db = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class TelegramUser(BaseModel):
    telegram_id = BigIntegerField()
    username = CharField(max_length=100, null=True)

    def __str__(self):
        return f"[{self.telegram_id}] - {self.username}"


class Category(BaseModel):
    name = CharField(max_length=150)

    def __str__(self):
        return self.name


class VideoReview(BaseModel):
    video = CharField()
    description = TextField()

    def __str__(self):
        return f"[{self.id}] - {self.description[:30]}"


class Product(BaseModel):
    name = CharField(max_length=150)
    description = TextField()
    price = FloatField(default=0.0)
    photo = CharField()
    sizes = CharField()
    dimension = CharField()
    video_review = CharField()
    category = ForeignKeyField(Category, null=True, backref='products', on_delete='SET NULL')

    def __str__(self):
        return self.name
