from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MADARAMUSIC import app


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NOTE: ButtonStyle / icon_custom_emoji_id are NOT available
#  in pyrofork 2.3.69 — plain InlineKeyboardButton used here.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def help_pannel(_, START: Union[bool, int] = None):
    """Page 1 — core music & admin categories."""
    nav_p1 = [
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        InlineKeyboardButton(text=_["NEXT_PAGE"],    callback_data="help_page_2"),
    ]
    nav_inner = [
        InlineKeyboardButton(text=_["BACK_PAGE"],    callback_data="help_page_1"),
        InlineKeyboardButton(text=_["BACK_BUTTON"],  callback_data="settingsback_helper"),
        InlineKeyboardButton(text=_["NEXT_PAGE"],    callback_data="help_page_2"),
    ]
    mark = nav_inner if START else nav_p1

    def _btn(key, cb):
        return InlineKeyboardButton(text=_[key], callback_data=cb)

    return InlineKeyboardMarkup([
        [_btn("H_B_1","help_callback hb1"),  _btn("H_B_2","help_callback hb2"),  _btn("H_B_3","help_callback hb3")],
        [_btn("H_B_4","help_callback hb4"),  _btn("H_B_5","help_callback hb5"),  _btn("H_B_6","help_callback hb6")],
        [_btn("H_B_7","help_callback hb7"),  _btn("H_B_8","help_callback hb8"),  _btn("H_B_9","help_callback hb9")],
        [_btn("H_B_10","help_callback hb10"),_btn("H_B_11","help_callback hb11"),_btn("H_B_12","help_callback hb12")],
        [_btn("H_B_13","help_callback hb13"),_btn("H_B_14","help_callback hb14"),_btn("H_B_15","help_callback hb15")],
        mark,
    ])


def help_pannel_extra(_, page: int = 2):
    """Page 2 — extra tools."""
    def _btn(key, cb):
        return InlineKeyboardButton(text=_[key], callback_data=cb)

    nav = [
        InlineKeyboardButton(text=_["BACK_PAGE"],   callback_data="help_page_1"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"],callback_data="close"),
        InlineKeyboardButton(text=_["NEXT_PAGE"],   callback_data="help_page_3"),
    ]

    return InlineKeyboardMarkup([
        [_btn("H_B_16","help_callback hb16"),_btn("H_B_17","help_callback hb17"),_btn("H_B_18","help_callback hb18")],
        [_btn("H_B_19","help_callback hb19"),_btn("H_B_20","help_callback hb20"),_btn("H_B_21","help_callback hb21")],
        [_btn("H_B_22","help_callback hb22"),_btn("H_B_23","help_callback hb23"),_btn("H_B_24","help_callback hb24")],
        nav,
    ])


def help_pannel_premium(_):
    """Page 3 — ✨ Premium Features: ChatFight · GenString · GitHub · Games."""
    def _btn(key, cb):
        return InlineKeyboardButton(text=_[key], callback_data=cb)

    nav = [
        InlineKeyboardButton(text=_["BACK_PAGE"],   callback_data="help_page_2"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"],callback_data="close"),
    ]

    return InlineKeyboardMarkup([
        # Row 1: ChatFight · GenString · GitHub
        [_btn("H_B_37","help_callback hb37"), _btn("H_B_38","help_callback hb38"), _btn("H_B_40","help_callback hb40")],
        # Row 2: GameTop · GPT · Cricket
        [_btn("H_B_39","help_callback hb39"), _btn("H_B_25","help_callback hb25"), _btn("H_B_27","help_callback hb27")],
        # Row 3: MyInfo · WHOIS · Reverse
        [_btn("H_B_28","help_callback hb28"), _btn("H_B_29","help_callback hb29"), _btn("H_B_30","help_callback hb30")],
        # Row 4: Instagram · VC Tools · AutoPlay
        [_btn("H_B_31","help_callback hb31"), _btn("H_B_35","help_callback hb35"), _btn("H_B_36","help_callback hb36")],
        nav,
    ])


def help_back_markup(_):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper"),
    ]])


def private_help_panel(_):
    return [[
        InlineKeyboardButton(
            text=_["S_B_4"],
            url=f"https://t.me/{app.username}?start=help",
        ),
    ]]
