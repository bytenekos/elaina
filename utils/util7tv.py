import aiohttp
import aiofiles
import asyncio
import re
import os


async def get7tvEmoteList(link: str):
    link = f"https://7tv.io/v3/emote-sets/{link}"
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(link) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return None


async def parseGuildEmotes(guildEmotes: f""):
    animated_emotes = []
    non_animated_emotes = []
    pattern = r"name='(.*?)'\s+animated=(.*?)\s"
    matches = re.findall(pattern, guildEmotes)
    for name, animated_str in matches:
        animated = animated_str.strip() == "True"
        if animated:
            animated_emotes.append(name)
        else:
            non_animated_emotes.append(name)

    return len(animated_emotes), len(non_animated_emotes)


async def download7tvEmote(emoteid: str, emotename: str):
    url = f"https://cdn.7tv.app/emote/{emoteid}/4x.webp"
    file_name = f"{emotename}.webp"
    folder_path = "temp"

    os.makedirs(folder_path, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                file_path = os.path.join(folder_path, file_name)
                async with aiofiles.open(file_path, mode="wb") as f:
                    await f.write(await resp.read())
                    print(f"Downloaded {url} to {file_path}")
            else:
                print(f"Failed to download {url}, status code: {resp.status}")
