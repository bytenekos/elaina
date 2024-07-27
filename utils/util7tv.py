import aiohttp
import aiofiles
import asyncio
import re
import os
import io
from PIL import Image


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


async def download7tvEmoteNonAnimated(emoteid: str, emotename: str):
    url = f"https://cdn.7tv.app/emote/{emoteid}/4x.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                emote_data = await resp.read()

                # imagesaved = Image.open(io.BytesIO(emote_data))

                with io.BytesIO(emote_data) as output:
                    output.seek(0)
                    emote_bytes = output.read()

                return emote_bytes

            else:
                print(f"Failed to download {url}, status code: {resp.status}")


async def download7tvEmoteAnimated(emoteid: str, emotename: str):
    url = f"https://cdn.7tv.app/emote/{emoteid}/4x.gif"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                emote_data = await resp.read()

                # imagesaved = Image.open(io.BytesIO(emote_data))

                with io.BytesIO(emote_data) as output:
                    output.seek(0)
                    emote_bytes = output.read()

                return emote_bytes

            else:
                print(f"Failed to download {url}, status code: {resp.status}")