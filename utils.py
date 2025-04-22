import random, string
from pyrogram.enums import ChatInviteLinkCreateOptions
from datetime import datetime, timedelta

def generate_hash(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def create_temporary_invite(bot, channel_id):
    expire_time = datetime.utcnow() + timedelta(minutes=5)
    invite = await bot.create_chat_invite_link(
        chat_id=channel_id,
        expire_date=expire_time,
        member_limit=1
    )
    return invite.invite_link
