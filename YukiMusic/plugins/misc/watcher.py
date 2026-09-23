from pyrogram import filters
from pyrogram.types import Message

from YukiMusic import yuki
from YukiMusic.core.call import Shruti

welcome = 20
close = 30


@yuki.on_message(filters.video_chat_started, group=welcome)
@yuki.on_message(filters.video_chat_ended, group=close)
async def welcome(_, message: Message):
    await Shruti.stop_stream_force(message.chat.id)
