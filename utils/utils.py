from typing import Optional
import aiohttp


async def request_to_url(url: str, method: str, json: Optional[dict] = None):
    async with aiohttp.ClientSession() as session:
        response = await session.request(method=method.upper(), json=json, url=url)
        return await response.json()
