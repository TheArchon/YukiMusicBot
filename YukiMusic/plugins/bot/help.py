import random
from typing import Union

from pyrogram import filters, types
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, Message

from YukiMusic import yuki
from YukiMusic.utils import help_pannel
from YukiMusic.utils.database import get_lang
from YukiMusic.utils.decorators.language import LanguageStart, languageCB
from YukiMusic.utils.inline.help import help_topic_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

MESSAGE_EFFECTS = [
    5107584321108051014,
    5159385139981059251,
    5104841245755180586,
    5046509860389126442,
]

# Only these six sections are used as Help Center pages.
HELP_TOPICS = {
    "hb1": helpers.HELP_1,
    "hb2": helpers.HELP_2,
    "hb6": helpers.HELP_6,
    "hb11": helpers.HELP_11,
    "hb14": helpers.HELP_14,
    "hb16": helpers.HELP_16,
}

HELP_PAGES = ["hb1", "hb2", "hb6", "hb11", "hb14", "hb16"]

# Display titles shown above each page, similar to the reference video.
HELP_TITLES = {
    "hb1": "⚡ Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs",
    "hb2": "🔐 Aᴜᴛʜ Cᴏᴍᴍᴀɴᴅs",
    "hb6": "🎵 C-Pʟᴀʏ Cᴏᴍᴍᴀɴᴅs",
    "hb11": "▶️ Pʟᴀʏ Cᴏᴍᴍᴀɴᴅs",
    "hb14": "🎶 Sᴏɴɢ Cᴏᴍᴍᴀɴᴅs",
    "hb16": "🔁 Aᴜᴛᴏᴘʟᴀʏ Cᴏᴍᴍᴀɴᴅs",
}


def _topic_page(cb):
    return HELP_PAGES.index(cb) + 1


def _topic_for_page(page):
    return HELP_PAGES[page - 1]


def _page_text(topic, page):
    return f"<b>🔒 Help Center {page}/{len(HELP_PAGES)}</b>\n\n<b>{HELP_TITLES[topic]}</b>\n\n{HELP_TOPICS[topic]}"


async def _show_help_home(CallbackQuery, _, START=False):
    # The Help button now opens page 1 directly, like the reference video.
    page = 1
    topic = _topic_for_page(page)
    keyboard = help_topic_markup(_, page, START)
    try:
        await CallbackQuery.edit_message_text(
            _page_text(topic, page), reply_markup=keyboard
        )
    except MessageNotModified:
        pass


async def _show_help_categories(CallbackQuery, _, START=False):
    keyboard = help_pannel(_, START, 1)
    try:
        await CallbackQuery.edit_message_text(
            _['help_1'].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    except MessageNotModified:
        pass


@yuki.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@yuki.on_callback_query(filters.regex(r"^settings_back_helper$") & ~BANNED_USERS)
async def helper_private(
    client: yuki, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except Exception:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        await _show_help_home(update, _, True)
    else:
        try:
            await update.delete()
        except Exception:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        page = 1
        topic = _topic_for_page(page)
        keyboard = help_topic_markup(_, page, False)
        await update.reply_text(
            _page_text(topic, page),
            reply_markup=keyboard,
        )


@yuki.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_['help_2'], reply_markup=InlineKeyboardMarkup(keyboard))


@yuki.on_callback_query(filters.regex(r"^help_page\s") & ~BANNED_USERS)
@languageCB
async def help_page_cb(client, CallbackQuery, _):
    parts = CallbackQuery.data.split()
    try:
        page = int(parts[1])
    except (IndexError, ValueError):
        return await CallbackQuery.answer()

    sf = parts[2] if len(parts) > 2 else "0"
    START = sf == "1"

    if page < 1 or page > len(HELP_PAGES):
        return await CallbackQuery.answer()

    topic = _topic_for_page(page)
    keyboard = help_topic_markup(_, page, START)
    try:
        await CallbackQuery.edit_message_text(
            _page_text(topic, page), reply_markup=keyboard
        )
    except MessageNotModified:
        pass
    finally:
        try:
            await CallbackQuery.answer()
        except Exception:
            pass


@yuki.on_callback_query(filters.regex(r"^help_callback\s") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    parts = CallbackQuery.data.strip().split()
    if len(parts) < 2:
        return await CallbackQuery.answer()

    cb = parts[1]
    sf = parts[2] if len(parts) > 2 else "0"
    START = sf == "1"

    if cb not in HELP_PAGES:
        return await CallbackQuery.answer("This help section is unavailable.", show_alert=True)

    page = _topic_page(cb)
    keyboard = help_topic_markup(_, page, START)
    try:
        await CallbackQuery.edit_message_text(
            _page_text(cb, page), reply_markup=keyboard
        )
    except MessageNotModified:
        pass
    finally:
        try:
            await CallbackQuery.answer()
        except Exception:
            pass


@yuki.on_callback_query(filters.regex(r"^help_home\s") & ~BANNED_USERS)
@languageCB
async def help_home_cb(client, CallbackQuery, _):
    parts = CallbackQuery.data.split()
    sf = parts[1] if len(parts) > 1 else "0"
    START = sf == "1"
    await _show_help_categories(CallbackQuery, _, START)
    try:
        await CallbackQuery.answer()
    except Exception:
        pass


@yuki.on_callback_query(filters.regex(r"^help_noop$") & ~BANNED_USERS)
async def help_noop_cb(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except Exception:
        pass
