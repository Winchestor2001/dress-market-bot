from .models import db, Category, Product
from peewee import fn
from playhouse.shortcuts import model_to_dict


async def create_category_obj(name: str):
    category = Category.create(name=name)
    return (f"✅ Категория '{category.name}' успешно добавлена с ID {category.id}!\n\n"
            f"Чтобы посмотреть список категории напишите команду /list_categories")


async def get_all_categories_obj():
    categories = Category.select().order_by(Category.name)
    if categories.exists():
        category_list = "\n".join([f"🔹 {category.name} = ID <code>{category.id}</code>" for category in categories])
        return f"📋 Список категорий:\n\n{category_list}"
    else:
        return "❌ Категории пока не добавлены."


async def get_all_categories_for_btn_obj():
    categories = Category.select().order_by(Category.name)
    if categories.exists():
        return categories
    else:
        return []


async def is_category_name_exists(category_name: str) -> bool:
    category_exists = Category.select().where(fn.LOWER(Category.name) == category_name.lower()).exists()
    return category_exists


async def delete_category_obj(category_id: int):
    category = Category.get_or_none(Category.id == category_id)  # Находим категорию по ID
    if category:
        category.delete_instance()  # Удаляем категорию
        return f"✅ Категория '{category.name}' успешно удалена!"
    else:
        return "❌ Категория с таким ID не найдена."


async def get_all_products():
    products = Product.select().order_by(Product.name)
    if products.exists():
        product_list = "\n".join([
            f"🔹 {product.name} = ID <code>{product.id}</code> = {product.price} RUB"
            for product in products
        ])
        return f"📋 Список продуктов:\n\n{product_list}"
    else:
        return "❌ Продукты пока не добавлены."


async def delete_product_by_id(product_id: str):
    try:
        product = Product.get(Product.id == product_id)
        product.delete_instance()
        return f"✅ Продукт с ID <code>{product_id}</code> успешно удален!"
    except Product.DoesNotExist:
        return f"❌ Продукт с ID <code>{product_id}</code> не найден."


async def create_product_obj(name: str, description: str, price: float, category_id: str, size_id: str,
                             video_review_id: str, photo_id: str, dimension: str):
    product = Product.create(
        name=name,
        description=description,
        price=price,
        category=category_id,
        sizes=size_id,
        video_review=video_review_id,
        photo=photo_id,
        dimension=dimension
    )
    return product
