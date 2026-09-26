from pyrogram.types import InlineKeyboardMarkup

from YukiMusic.button_styles import (
    danger_button,
    primary_button,
    success_button,
)


def stats_buttons(_, status):
    if status:
        keyboard = [
            [
                success_button(
                    text=_[\"SA_B_2\"],
                    callback_data=\"bot_stats_sudo\",
                ),
                primary_button(
                    text=_[\"SA_B_3\"],
                    callback_data=\"TopOverall\",
                ),
            ],
            [
                danger_button(
                    text=_[\"CLOSE_BUTTON\"],
                    callback_data=\"close\",
                ),
            ],
        ]
    else:
        keyboard = [
            [
                primary_button(
                    text=_[\"SA_B_1\"],
                    callback_data=\"TopOverall\",
                ),
            ],
            [
                danger_button(
                    text=_[\"CLOSE_BUTTON\"],
                    callback_data=\"close\",
                ),
            ],
        ]

    return InlineKeyboardMarkup(keyboard)


def back_stats_buttons(_):
    return InlineKeyboardMarkup(
        [
            [
                primary_button(
                    text=_[\"BACK_BUTTON\"],
                    callback_data=\"stats_back\",
                ),
                danger_button(
                    text=_[\"CLOSE_BUTTON\"],
                    callback_data=\"close\",
                ),
            ],
        ]
    )
