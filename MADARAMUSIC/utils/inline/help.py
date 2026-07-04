from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MADARAMUSIC import app
from MADARAMUSIC.utils.emojis import (
    E_SPARK, E_CROWN, E_DIAMOND, E_THUNDER, E_MUSIC, E_GLOBE,
    E_GEAR, E_LOCK, E_HEART, E_STAR, E_FIRE, E_MIC,
)

# ── Premium emoji helper ─────────────────────────────────────────
def _e(eid, fb):
    return f'<emoji id={eid}>{fb}</emoji>'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NOTE: ButtonStyle / icon_custom_emoji_id are NOT available
#  in pyrofork 2.3.69 — plain InlineKeyboardButton only.
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
    """Page 3 — ✨ Premium Features."""
    def _btn(label, cb):
        return InlineKeyboardButton(text=label, callback_data=cb)

    nav = [
        InlineKeyboardButton(text=_["BACK_PAGE"],   callback_data="help_page_2"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"],callback_data="close"),
    ]

    return InlineKeyboardMarkup([
        # Row 1: ChatFight · GenString · GitHub
        [
            _btn(f'{_e(E_FIRE,"🔥")} ᴄʜᴀᴛꜰɪɢʜᴛ',   "help_callback hb37"),
            _btn(f'{_e(E_LOCK,"🔒")} ɢᴇɴsᴛʀɪɴɢ',   "help_callback hb38"),
            _btn(f'{_e(E_GLOBE,"🌐")} ɢɪᴛʜᴜʙ',     "help_callback hb40"),
        ],
        # Row 2: UPI Pay · Crypto · GameTop
        [
            _btn(f'{_e(E_DIAMOND,"💎")} ᴜᴩɪ ᴩᴀʏ',   "help_callback hb41"),
            _btn(f'{_e(E_THUNDER,"⚡")} ᴄʀʏᴩᴛᴏ',    "help_callback hb42"),
            _btn(f'{_e(E_CROWN,"👑")} ɢᴀᴍᴇᴛᴏᴩ',    "help_callback hb39"),
        ],
        # Row 3: GPT · Cricket · MyInfo
        [
            _btn(f'{_e(E_SPARK,"✨")} ɢᴘᴛ',         "help_callback hb25"),
            _btn(f'{_e(E_FIRE,"🏏")} ᴄʀɪᴄᴋᴇᴛ',     "help_callback hb27"),
            _btn(f'{_e(E_STAR,"⭐")} ᴍʏɪɴꜰᴏ',       "help_callback hb28"),
        ],
        # Row 4: WHOIS · Reverse · Instagram
        [
            _btn(f'{_e(E_GEAR,"⚙️")} ᴡʜᴏɪs',        "help_callback hb29"),
            _btn(f'{_e(E_MUSIC,"🔄")} ʀᴇᴠᴇʀsᴇ',     "help_callback hb30"),
            _btn(f'{_e(E_HEART,"❤️")} ɪɴsᴛᴀ',       "help_callback hb31"),
        ],
        # Row 5: VC Tools · AutoPlay
        [
            _btn(f'{_e(E_MIC,"🎤")} ᴠᴄ ᴛᴏᴏʟs',     "help_callback hb35"),
            _btn(f'{_e(E_MUSIC,"🎵")} ᴀᴜᴛᴏᴩʟᴀʏ',   "help_callback hb36"),
        ],
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
