from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from YukiMusic import yuki

# Only these six sections are shown in the Help Center category menu.
HELP_PAGES = ["hb1", "hb2", "hb6", "hb11", "hb14", "hb16"]


def _mark_button(_, START):
    if START:
        # Used when Help is opened from the bot's Start page.
        # Pressing Back returns to the Start page.
        return InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settings_back_helper",
            style=ButtonStyle.SUCCESS,
        )
    return InlineKeyboardButton(
        text=_["CLOSE_BUTTON"],
        callback_data="close",
        style=ButtonStyle.DANGER,
    )


def help_pannel(_, START: Union[bool, int] = None, page: int = 1):
    """Six-category Help Center menu.

    /help opens this menu directly. When opened from Start, START=True
    makes the bottom button return to the Start page.
    """
    sf = "1" if START else "0"
    rows = []

    for i in range(0, len(HELP_PAGES), 2):
        row = []
        for key in HELP_PAGES[i : i + 2]:
            row.append(
                InlineKeyboardButton(
                    text=_[f"H_B_{key[2:]}"],
                    callback_data=f"help_callback {key} {sf}",
                    style=ButtonStyle.PRIMARY,
                )
            )
        rows.append(row)

    rows.append([_mark_button(_, START)])
    return InlineKeyboardMarkup(rows)


def help_topic_markup(_, page: int = 1, START: Union[bool, int] = None):
    """Video-style command page navigation: Prev | page/6 | Next + Home."""
    sf = "1" if START else "0"
    total = len(HELP_PAGES)
    page = max(1, min(page, total))

    prev_button = InlineKeyboardButton(
        text=_["PREV_BUTTON"],
        callback_data=f"help_page {page - 1} {sf}" if page > 1 else "help_noop",
        style=ButtonStyle.PRIMARY,
    )
    page_button = InlineKeyboardButton(
        text=f"🔒 {page}/{total}",
        callback_data="help_noop",
        style=ButtonStyle.DANGER,
    )
    next_button = InlineKeyboardButton(
        text=_["NEXT_BUTTON"],
        callback_data=f"help_page {page + 1} {sf}" if page < total else "help_noop",
        style=ButtonStyle.PRIMARY,
    )

    navigation_row = [prev_button, page_button]
    if page < total:
        navigation_row.append(next_button)

    return InlineKeyboardMarkup(
        [
            navigation_row,
            [
                InlineKeyboardButton(
                    text="👋 Home",
                    callback_data=f"help_home {sf}",
                    style=ButtonStyle.SUCCESS,
                )
            ],
        ]
    )


def help_back_markup(_, page: int = 1, START: Union[bool, int] = None):
    return help_topic_markup(_, page, START)


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{yuki.username}?start=help",
            ),
        ],
    ]
    return buttons
