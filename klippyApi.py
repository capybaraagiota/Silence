import aiohttp
import asyncio
import os
import random

async def get_random_gif(query):
    app_key = os.getenv("KLIPY_API_KEY")
    if not app_key:
        return None
    url = f"https://api.klipy.com/api/v1/{app_key}/gifs/search"
    params = {
        "page": 1,
        "per_page": 20,
        "q": query,
        "format_filter": "gif",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                gifs = data.get("data", {}).get("data", [])
                if not gifs:
                    return None
                chosen_gif = random.choice(gifs)
                return chosen_gif.get("file", {}).get("md", {}).get("gif", {}).get("url")
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None