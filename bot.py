from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database import *
from utils import generate_hash, create_temporary_invite
import os

bot = Client("temp_invite_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    add_user(message.from_user.id)
    args = message.command[1] if len(message.command) > 1 else None
    if args:
        for channel in get_channels():
            link = await create_temporary_invite(client, channel["_id"])
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=link)]]
            )
            await message.reply_photo(
                photo="start_data/start_image.jpg",
                caption=open("start_data/start_text.txt").read().replace("{link}", link),
                reply_markup=keyboard
            )
            return
    else:
        await message.reply("Welcome! Use /request <anime> or type anime name.")

@bot.on_message(filters.command("setchannel") & filters.user(OWNER_ID))
async def set_channel(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a channel message to register it.")
    chat = message.reply_to_message.sender_chat
    if not chat:
        return await message.reply("Message must be from a channel.")
    await client.join_chat(chat.id)
    register_channel(chat.id, chat.title)
    await message.reply(f"Channel {chat.title} added.")

@bot.on_message(filters.command("removechannel") & filters.user(OWNER_ID))
async def remove_channel_cmd(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /removechannel <chat_id>")
    remove_channel(int(message.command[1]))
    await message.reply("Channel removed.")

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    for user in users.find():
        try:
            await message.reply_to_message.copy(user["_id"])
        except:
            pass
    await message.reply("Broadcast complete.")

@bot.on_message(filters.command("request"))
async def anime_request(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /request <anime name>")
    anime = " ".join(message.command[1:])
    save_request(message.from_user.id, anime)
    await client.send_message(REQUEST_LOG_CHANNEL, f"#REQUEST\nUser: {message.from_user.mention()}\nAnime: {anime}")
    await message.reply("Your request has been sent!")

@bot.on_message(filters.text & ~filters.command(["start"]))
async def handle_anime_search(client, message: Message):
    text = message.text.strip().lower()
    for channel in get_channels():
        if text in channel["title"].lower():
            link = await create_temporary_invite(client, channel["_id"])
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=link)]]
            )
            await message.reply_photo(
                photo="start_data/start_image.jpg",
                caption=open("start_data/start_text.txt").read().replace("{link}", link),
                reply_markup=keyboard
            )
            return
    save_request(message.from_user.id, text)
    await client.send_message(REQUEST_LOG_CHANNEL, f"#UNKNOWN\nUser: {message.from_user.mention()}\nAnime: {text}")
    await message.reply("Anime not found. Request sent to admins.")

bot.run()
