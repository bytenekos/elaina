import aiohttp


async def get7tvEmoteList(link: str):
    link = f"https://7tv.io/v3/emote-sets/{link}"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(link) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return None
