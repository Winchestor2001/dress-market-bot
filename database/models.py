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
    dimension_photo = CharField(null=True)

    def __str__(self):
        return self.name


class ProductSize(BaseModel):
    name = CharField(max_length=50)

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
    price = CharField()
    photo = CharField()
    size_id = CharField()
    contact = CharField()
    dimension = CharField()
    video_review = CharField(null=True)
    category = ForeignKeyField(Category, null=True, backref='products', on_delete='SET NULL')

    def __str__(self):
        return self.name


class ScheduledPost(BaseModel):
    post_type = CharField()
    content = TextField()
    file_id = TextField(null=True)
    schedule_time = DateTimeField()
    buttons = TextField(null=True)
