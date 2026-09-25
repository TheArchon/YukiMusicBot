from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from YukiMusic import yuki

# Only the six Help Center categories selected by the user.
HELP_PAGES = ["hb1", "hb2", "hb6", "hb11", "hb14", "hb16"]


def _mark_button(_, START):
    # The main Help Center always has a way back to the previous/start panel.
    if START:
        return InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
            style=ButtonStyle.SUCCESS,
        )
    return InlineKeyboardButton(
        text=_["CLOSE_BUTTON"],
        callback_data="close",
        style=ButtonStyle.DANGER,
    )


def help_pannel(_, START: Union[bool, int] = None, page: int = 1):
    """Main Help Center: six category buttons on one page."""
    sf = "1" if START else "0"
    rows = []

    # 2 buttons per row gives the menu a cleaner card/grid appearance.
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


def help_topic_markup(_, page: int, START: Union[bool, int] = None):
    """Video-style topic navigation: Prev | page/6 | Next, then Home."""
    sf = "1" if START else "0"
    total = len(HELP_PAGES)
    page = max(1, min(page, total))

    prev_button = InlineKeyboardButton(
        text=_["PREV_BUTTON"],
        callback_data=f"help_page {page - 1} {sf}" if page > 1 else "help_noop",
        style=ButtonStyle.PRIMARY,
    )
    page_button = InlineKeyboardButton(
        text=f"{page}/{total}",
        callback_data="help_noop",
        style=ButtonStyle.DANGER,
    )
    next_button = InlineKeyboardButton(
        text=_["NEXT_BUTTON"],
        callback_data=f"help_page {page + 1} {sf}" if page < total else "help_noop",
        style=ButtonStyle.PRIMARY,
    )

    return InlineKeyboardMarkup(
        [
            [prev_button, page_button, next_button],
            [
                InlineKeyboardButton(
                    text="🏠 Home",
                    callback_data=f"help_home {sf}",
                    style=ButtonStyle.SUCCESS,
                )
            ],
        ]
    )


def help_back_markup(_, page: int = 1, START: Union[bool, int] = None):
    # Kept as a compatibility wrapper for any other imports.
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
