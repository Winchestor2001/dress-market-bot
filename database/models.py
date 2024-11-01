from peewee import *
from playhouse.shortcuts import model_to_dict

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


class ProductSize(BaseModel):
    size = CharField(max_length=50)

    def __str__(self):
        return self.size


class Dimension(BaseModel):
    photo = CharField()
    description = TextField()

    def __str__(self):
        return f"[{self.id}] - {self.description[:30]}"


class VideoReview(BaseModel):
    video = CharField()  # Storing path of the video as CharField (adjust if needed)
    description = TextField()

    def __str__(self):
        return f"[{self.id}] - {self.description[:30]}"


class Product(BaseModel):
    name = CharField(max_length=150)
    description = TextField()
    size = ManyToManyField(ProductSize, backref='products')
    price = FloatField(default=0.0)
    photo = CharField()  # Storing path of the image as CharField (adjust if needed)
    dimension = ForeignKeyField(Dimension, null=True, backref='products', on_delete='SET NULL')
    video_review = ForeignKeyField(VideoReview, null=True, backref='products', on_delete='SET NULL')
    category = ForeignKeyField(Category, null=True, backref='products', on_delete='SET NULL')

    def __str__(self):
        return self.name


# Establish many-to-many relationship for Product and ProductSize
ProductSizeThrough = Product.size.get_through_model()

