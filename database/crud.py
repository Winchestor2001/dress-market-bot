from .models import db, Category, Product, ProductSize, TelegramUser
from peewee import fn
from playhouse.shortcuts import model_to_dict


async def create_user_obj(telegram_id: int, username: str = None):
    user = TelegramUser.get_or_none(telegram_id=telegram_id)
    if not user:
        TelegramUser.create(telegram_id=telegram_id, username=username)


async def get_all_users_obj():
    users = TelegramUser.select()
    return [model_to_dict(user) for user in users]


async def create_category_obj(name: str, dimension_photo: str):
    category = Category.create(name=name, dimension_photo=dimension_photo)
    return (f"✅ Категория '{category.name}' успешно добавлена с ID {category.id}!\n\n"
            f"Чтобы посмотреть список категории напишите команду /list_categories")


async def create_size_obj(name: str):
    size = ProductSize.create(name=name)
    return (f"✅ Размер '{size.name}' успешно добавлена с ID {size.id}!\n\n"
            f"Чтобы посмотреть список категории напишите команду /list_sizes")


async def get_all_categories_obj():
    categories = Category.select().order_by(Category.name)
    if categories.exists():
        category_list = "\n".join([
            f"🔹 {category.name} = ID <code>{category.id}</code> = Замеры: {'Есть' if category.dimension_photo else 'Нет'}"
            for category in categories])
        return f"📋 Список категорий:\n\n{category_list}"
    else:
        return "❌ Категории пока не добавлены."


async def get_all_sizes_obj():
    sizes = ProductSize.select().order_by(ProductSize.name)
    if sizes.exists():
        size_list = "\n".join([f"🔹 {size.name} = ID <code>{size.id}</code>" for size in sizes])
        return f"📋 Список размеров:\n\n{size_list}"
    else:
        return "❌ Размеров пока не добавлены."


async def delete_size_obj(size_id: int):
    size = ProductSize.get_or_none(ProductSize.id == size_id)
    if size:
        size.delete_instance()  # Удаляем категорию
        return f"✅ Размер '{size.size}' успешно удалена!"
    else:
        return "❌ Размер с таким ID не найдена."


async def get_all_categories_for_btn_obj():
    categories = Category.select().order_by(Category.name)
    if categories.exists():
        return categories
    else:
        return []


async def get_all_sizes_for_btn_obj():
    sizes = ProductSize.select().order_by(ProductSize.name)
    if sizes.exists():
        sizes = ProductSize.select().order_by(ProductSize.name)

        # Define the desired order for sizes
        size_order = {
            'S/M': 0,
            'L': 1,
            'XL': 2,
            'XXL+': 3,
        }

        # Sort sizes using the defined order
        sorted_sizes = sorted(sizes, key=lambda size: size_order.get(size.name, len(size_order)))

        return sorted_sizes
    else:
        return []


async def is_category_name_exists(category_name: str) -> bool:
    category_exists = Category.select().where(Category.name ** category_name).exists()
    return category_exists


async def is_size_name_exists(size_name: str) -> bool:
    size_exists = ProductSize.select().where(ProductSize.name ** size_name).exists()
    return size_exists


async def delete_category_obj(category_id: int):
    category = Category.get_or_none(Category.id == category_id)  # Находим категорию по ID
    if category:
        category.delete_instance()  # Удаляем категорию
        return f"✅ Категория '{category.name}' успешно удалена!"
    else:
        return "❌ Категория с таким ID не найдена."


async def get_single_category_obj(category_id: int):
    category = Category.get_or_none(Category.id == category_id)
    return category


async def get_single_product_obj(product_id: int):
    product = Product.get_or_none(Product.id == product_id)
    return product


async def update_category_dimension_obj(category_name: str, dimension_photo):
    category = Category.get_or_none(Category.name == category_name)
    if category:
        category.dimension_photo = dimension_photo
        category.save()
        return f"✅ Фото замеры для категории '{category.name}' успешно обновлено!"
    else:
        return "❌ Категория с таким ID не найдена."


async def update_product_video_review_obj(product_id: int, video_review):
    product = Product.get_or_none(Product.id == product_id)
    if product:
        product.video_review = video_review
        product.save()
        return f"✅ Видеообзор для продукта '{product.name}' успешно обновлено!"
    else:
        return "❌ Продукт с таким ID не найдена."


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
    size = ProductSize.get(ProductSize.id == size_id)
    product = Product.create(
        name=name,
        description=description,
        price=price,
        category=category_id,
        size_id=size.name,
        video_review=video_review_id,
        photo=photo_id,
        dimension=dimension
    )
    return product


async def get_filtered_products(category_name: str, size_name: str):
    category = Category.get(Category.name == category_name)
    size = ProductSize.get(ProductSize.name == size_name)

    query = (
        Product
        .select()
        .where(
            (Product.category == category) &
            (Product.size_id == size.name)
        )
    )

    if query.exists():
        products = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "photo": product.photo,
                "category": product.category.name,
                "size_id": product.size_id
            }
            for product in query
        ]
        return products
    else:
        return "❌ Продукты с заданными категорией и размером не найдены."


async def get_product_video_review(product_id: int):
    product = Product.get_or_none(Product.id == product_id)
    if product and product.video_review:
        return product.video_review
    return None


async def get_product_dimension(product_id: int):
    product = Product.get_or_none(Product.id == product_id)
    if product and product.dimension and product.category.dimension_photo:
        return product.dimension, product.category.dimension_photo
    return None
