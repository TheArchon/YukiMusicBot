from pyrogram import types
from pyrogram.enums import ButtonStyle

from YukiMusic import yuki
from YukiMusic.utils.rich_stream import caption_blocks
from strings import helpers


HELP_TOPICS = {
    "hb1": helpers.HELP_1,
    "hb2": helpers.HELP_2,
    "hb3": helpers.HELP_3,
    "hb4": helpers.HELP_4,
    "hb5": helpers.HELP_5,
    "hb6": helpers.HELP_6,
    "hb7": helpers.HELP_7,
    "hb8": helpers.HELP_8,
    "hb9": helpers.HELP_9,
    "hb10": helpers.HELP_10,
    "hb11": helpers.HELP_11,
    "hb12": helpers.HELP_12,
    "hb13": helpers.HELP_13,
    "hb14": helpers.HELP_14,
    "hb15": helpers.HELP_15,
    "hb16": helpers.HELP_16,
}

PAGE_ONE = [
    "hb1",
    "hb2",
    "hb3",
    "hb4",
    "hb5",
    "hb6",
    "hb7",
    "hb8",
    "hb9",
]

PAGE_TWO = [
    "hb10",
    "hb11",
    "hb12",
    "hb13",
    "hb14",
    "hb15",
    "hb16",
]


def _button(text, callback_data, style=ButtonStyle.DEFAULT):
    return types.RichMessageButton(
        text=text,
        style=style,
        callback_data=callback_data,
    )


def _row(*buttons):
    return types.InputRichBlockButtons(buttons=list(buttons))


def _label(_, key, fallback):
    value = _.get(key) if hasattr(_, "get") else None
    return value or fallback


def _topic_button(_, topic):
    labels = {
        "hb1": "Music",
        "hb2": "Admin",
        "hb3": "Auth",
        "hb4": "Broadcast",
        "hb5": "Filters",
        "hb6": "Global",
        "hb7": "Group",
        "hb8": "Extra",
        "hb9": "Misc",
        "hb10": "Owner",
        "hb11": "Play",
        "hb12": "Playlist",
        "hb13": "Settings",
        "hb14": "Tools",
        "hb15": "Video",
        "hb16": "More",
    }

    return _button(
        labels.get(topic, topic.upper()),
        f"help_callback {topic}",
        ButtonStyle.DEFAULT,
    )


def build_help_blocks(_, start=False, page=1):
    page = 2 if int(page) == 2 else 1
    topics = PAGE_TWO if page == 2 else PAGE_ONE

    blocks = caption_blocks(
        _label(
            _,
            "help_2",
            "<b>Help Center</b>\n\nSelect a category below.",
        )
    )

    buttons = [_topic_button(_, topic) for topic in topics]

    for index in range(0, len(buttons), 2):
        blocks.append(_row(*buttons[index:index + 2]))

    navigation = []

    if page == 2:
        navigation.append(
            _button(
                _label(_, "PREV_BUTTON", "‹ Back"),
                f"help_page 1 {'1' if start else '0'}",
                ButtonStyle.PRIMARY,
            )
        )

    if page == 1:
        navigation.append(
            _button(
                _label(_, "NEXT_BUTTON", "Next ›"),
                f"help_page 2 {'1' if start else '0'}",
                ButtonStyle.PRIMARY,
            )
        )

    if navigation:
        blocks.append(_row(*navigation))

    if start:
        blocks.append(
            _row(
                _button(
                    _label(_, "BACK_BUTTON", "Back"),
                    "settings_back_helper",
                    ButtonStyle.SUCCESS,
                ),
                _button(
                    _label(_, "CLOSE_BUTTON", "Close"),
                    "close",
                    ButtonStyle.DANGER,
                ),
            )
        )
    else:
        blocks.append(
            _row(
                _button(
                    _label(_, "CLOSE_BUTTON", "Close"),
                    "close",
                    ButtonStyle.DANGER,
                )
            )
        )

    return blocks


def build_help_topic_blocks(_, topic, page=1, start=False):
    text = HELP_TOPICS.get(topic)

    if text is None:
        text = "<b>Help topic not found.</b>"

    blocks = caption_blocks(text)

    blocks.append(
        _row(
            _button(
                _label(_, "BACK_BUTTON", "‹ Back"),
                f"help_page {page} {'1' if start else '0'}",
                ButtonStyle.PRIMARY,
            ),
            _button(
                _label(_, "CLOSE_BUTTON", "Close"),
                "close",
                ButtonStyle.DANGER,
            ),
        )
    )

    return blocks


async def send_help(client, chat_id, _, start=True, page=1, photo=None):
    blocks = []

    if photo:
        blocks.append(
            types.InputRichBlockPhoto(
                photo=types.InputMediaPhoto(photo)
            )
        )

    blocks.extend(
        build_help_blocks(
            _,
            start=start,
            page=page,
        )
    )

    return await client.send_rich_message(
        chat_id,
        rich_message=types.InputRichMessage(blocks=blocks),
    )
