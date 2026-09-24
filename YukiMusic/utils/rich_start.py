import re

from pyrogram import enums, types

import config
from YukiMusic import yuki
from YukiMusic.utils.rich_stream import caption_blocks


_BUTTON_STYLES = (
    enums.ButtonStyle.DEFAULT,
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER,
)


def _clean_html(text):
    """Keep only tags understood by rich_stream's caption parser."""
    if not text:
        return ""
    return re.sub(r"<(?!/?(?:b|a)(?:\s+href=[^>]+)?>)[^>]+>", "", text, flags=re.I)


def _caption_blocks(text):
    return caption_blocks(_clean_html(text))


def _button(text, style, callback_data=None, url=None):
    kwargs = {"text": text, "style": style}
    if url:
        kwargs["url"] = url
    else:
        kwargs["callback_data"] = callback_data
    return types.RichMessageButton(**kwargs)


def _photo(photo):
    return types.InputRichBlockPhoto(photo=types.InputMediaPhoto(photo))


def _start_buttons(_):
    # Keep the same five actions that the existing private start panel exposes.
    return [
        types.InputRichBlockButtons(
            buttons=[
                _button(
                    _["S_B_3"],
                    enums.ButtonStyle.PRIMARY,
                    url=f"https://t.me/{yuki.username}?startgroup=true",
                )
            ]
        ),
        types.InputRichBlockButtons(
            buttons=[
                _button(
                    _["S_B_4"],
                    enums.ButtonStyle.SUCCESS,
                    callback_data="settings_back_helper",
                )
            ]
        ),
        types.InputRichBlockButtons(
            buttons=[
                _button(
                    _["S_B_6"],
                    enums.ButtonStyle.DEFAULT,
                    url=config.SUPPORT_CHANNEL,
                ),
                _button(
                    _["S_B_2"],
                    enums.ButtonStyle.PRIMARY,
                    url=config.SUPPORT_CHAT,
                ),
            ]
        ),
        types.InputRichBlockButtons(
            buttons=[
                _button(
                    _["S_B_5"],
                    enums.ButtonStyle.DANGER,
                    url=f"tg://user?id={config.OWNER_ID}",
                )
            ]
        ),
    ]


def build_private_start_blocks(_, caption, photo=None):
    blocks = []
    if photo:
        blocks.append(_photo(photo))
    blocks.extend(_caption_blocks(caption))
    blocks.extend(_start_buttons(_))
    return blocks


def build_group_start_blocks(_, caption, photo=None):
    blocks = []
    if photo:
        blocks.append(_photo(photo))
    blocks.extend(_caption_blocks(caption))
    blocks.append(
        types.InputRichBlockButtons(
            buttons=[
                _button(
                    _["S_B_1"],
                    enums.ButtonStyle.PRIMARY,
                    url=f"https://t.me/{yuki.username}?startgroup=true",
                ),
                _button(
                    _["S_B_2"],
                    enums.ButtonStyle.SUCCESS,
                    url=config.SUPPORT_CHAT,
                ),
            ]
        )
    )
    return blocks


async def send_private_start(message, _, caption, photo=None):
    blocks = build_private_start_blocks(_, caption, photo or config.START_IMG_URL)
    return await yuki.send_rich_message(message.chat.id, rich_message=types.InputRichMessage(blocks=blocks))


async def send_group_start(message, _, caption, photo=None):
    blocks = build_group_start_blocks(_, caption, photo or config.START_IMG_URL)
    return await yuki.send_rich_message(message.chat.id, rich_message=types.InputRichMessage(blocks=blocks))
