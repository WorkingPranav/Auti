from typing import Union
from pyrogram.types.user_and_chats import user
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types.user_and_chats.user import User
from ..database.user_db import UserDB
from PIL import Image
import os
import asyncio
import logging
import time
import random
from ..database.user_db import UserDB
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

# Setup a logger
renamelog = logging.getLogger(__name__)

# Function to adjust and save the image
async def adjust_image(path: str) -> Union[str, None]:
    try:
        im = Image.open(path)
        im = im.convert("RGB")
        im.thumbnail((320, 320))
        im.save(path, "JPEG")
        return path
    except Exception as e:
        renamelog.error(f"Error adjusting image: {str(e)}")
        return None

# Function to handle setting a thumbnail
@Client.on_message(filters.command("setthumb"))
async def handle_set_thumb(client, message: Message):
    if message.reply_to_message and message.reply_to_message.photo:
        path = await message.reply_to_message.download()
        path = await adjust_image(path)
        if path:
            with open(path, "rb") as file_handle:
                data = file_handle.read()
                UserDB().set_thumbnail(data, message.from_user.id)
            os.remove(path)
            await message.reply_text("Thumbnail set successfully.", quote=True)
        else:
            await message.reply_text("Error adjusting the image. Please try again.", quote=True)
    else:
        await message.reply_text("Reply to an image to set it as a thumbnail.", quote=True)

# Function to handle getting the thumbnail
@Client.on_message(filters.command("getthumb"))
async def handle_get_thumb(client, message: Message):
    user_thumb = UserDB().get_thumbnail(message.from_user.id)
    if user_thumb:
        await message.reply_photo(user_thumb, quote=True)
    else:
        await message.reply("No Thumbnail Found.", quote=True)

# Function to generate a screenshot
async def gen_ss(filepath, ts, opfilepath=None):
    source = filepath
    destination = os.path.dirname(source)
    ss_name = f"{os.path.basename(source)}_{int(time.time())}.jpg"
    ss_path = os.path.join(destination, ss_name)

    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(ts), "-i", str(source), "-vframes", "1", "-q:v", "2", str(ss_path)]

    try:
        subpr = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        spipe, epipe = await subpr.communicate()
        epipe = epipe.decode().strip()
        spipe = spipe.decode().strip()
        renamelog.info(f"Stdout Pipe: {spipe}")
        renamelog.info(f"Error Pipe: {epipe}")

        return ss_path
    except Exception as e:
        renamelog.error(f"Error generating screenshot: {str(e)}")
        return None

# Function to resize an image
async def resize_img(path, width=None, height=None):
    img = Image.open(path)
    wei, hei = img.size

    wei = width if width is not None else wei
    hei = height if height is not None else hei

    img.thumbnail((wei, hei))
    
    img.save(path, "JPEG")
    return path

# Function to handle clearing the thumbnail
@Client.on_message(filters.command("clrthumb"))
async def handle_clr_thumb(client, message: Message):
    UserDB().set_thumbnail(None, message.from_user.id)
    await message.reply_text("Thumbnail Cleared.", quote=True)
