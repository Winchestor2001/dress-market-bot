import pandas as pd
from openpyxl import load_workbook
import io
import logging

from loader import bot

logger = logging.getLogger(__name__)


async def parse_products_from_excel(file_path: str):
    df = pd.read_excel(file_path, engine="openpyxl")
    wb = load_workbook(file_path)
    sheet = wb.active

    # Логируем заголовки
    logger.info(f"Заголовки колонок: {list(df.columns)}")

    # Проверяем наличие нужных колонок
    required_columns = ["Название", "Описание", "Цена", "Категория", "Размер", "Фото"]
    for col in required_columns:
        if col not in df.columns:
            raise logger.info(f"В файле нет колонки '{col}'!")

    # Получаем индексы столбцов
    columns = {col.strip(): i for i, col in enumerate(df.columns)}
    photo_col_index = columns["Фото"] + 1  # openpyxl использует 1-based индексацию

    # Проверяем, есть ли изображения в файле
    logger.info(f"Найдено изображений: {len(sheet._images)}")
    if not sheet._images:
        logger.info("❌ В файле нет изображений!")
        return []

    # Карта изображений {номер строки: байтовые данные изображения}
    image_mapping = {}
    for image in sheet._images:
        row = image.anchor._from.row  # Строка, где стоит картинка
        col = image.anchor._from.col  # Колонка, в которой картинка

        logger.info(f"🔍 Изображение найдено в строке {row}, колонке {col}")

        if col == photo_col_index:  # Проверяем, что картинка в нужном столбце
            img_data = io.BytesIO(image._data())
            image_mapping[row] = img_data.getvalue()

            # Сохраняем временное изображение для проверки
            temp_path = f"temp_image_{row}.png"
            with open(temp_path, "wb") as f:
                f.write(image_mapping[row])
            logger.info(f"✅ Сохранено изображение: {temp_path}")

    # Список продуктов
    products = []
    for index, row in df.iterrows():
        row_number = index + 2  # Excel использует 1-based индексацию (плюс заголовки)
        product = {
            "name": row["Название"],
            "description": row["Описание"],
            "price": row["Цена"],
            "category_id": row["Категория"],
            "size_id": row["Размер"],
            "photo": image_mapping.get(row_number),  # Привязка фото к строке
        }

        if product["photo"] is None:
            logger.info(f"⚠️ Нет фото для строки {row_number} ({product['name']})")

        products.append(product)

    return products


async def upload_photo_to_telegram(chat_id: int, photo_data: bytes) -> str:
    img_io = io.BytesIO(photo_data)
    img_io.name = "image.jpg"

    response = await bot.send_photo(chat_id=chat_id, photo=img_io)
    return response.photo[-1].file_id
