import re
import json


async def format_content(content) -> dict:
    button_matches = re.findall(r"\[(.+?)\s*=\s*(https?://\S+)\]", content)

    buttons = [{"text": text.strip(), "link": link.strip()} for text, link in button_matches]

    message_text = re.sub(r"\[.+?\s*=\s*https?://\S+\]", "", content).strip()

    return {"buttons": buttons, "message_text": message_text}


async def parse_text(text):
    name_match = re.search(r'^(.*?)\n', text)
    size_match = re.search(r'Размер:\s*(\w+)', text)
    description_match = re.search(r'Состояние:\s*([\s\S]+?)\nЦена:', text)
    price_match = re.search(r'Цена:\s*[^\d]*([\d,.]+)', text)
    buy_match = re.search(r'Купить - (@\w+)', text)

    description = description_match.group(1).strip() if description_match else None
    if description:
        description = ' '.join(description.splitlines())

    size = size_match.group(1) if size_match else None
    if size:
        size = size.replace('М', 'M').upper()

    return {
        "name": name_match.group(1).strip() if name_match else None,
        "size": size,
        "description": description,
        "price": price_match.group(1).replace(',', '.') if price_match else None,
        "contact": buy_match.group(1) if buy_match else None
    }
