import ssl

import aiohttp
from aiohttp import web
import json

from config import BOT_TOKEN

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


@web.middleware
async def cors_middleware(request, handler):
    if request.method == "OPTIONS":
        return web.Response(headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600"
        })

    response = await handler(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


async def get_photo_url(file_id: str) -> str:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            data = await resp.json()
            file_path = data.get("result", {}).get("file_path")
            if file_path:
                return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            return ""


async def handle_get_products(request):
    from database.crud import get_all_products_for_webapp

    products = await get_all_products_for_webapp()
    return web.Response(text=json.dumps(products), content_type="application/json")
