---
name: ButtonStyle removal
description: pyrofork 2.3.69 does not have ButtonStyle or icon_custom_emoji_id; all InlineKeyboardButton calls must use only text= and callback_data=/url=
---

**Rule:** Never import `ButtonStyle` from `pyrogram.enums` and never pass `style=` or `icon_custom_emoji_id=` to `InlineKeyboardButton` when using pyrofork 2.3.69.

**Why:** The installed pyrofork version is 2.3.69. `ButtonStyle` does not exist in `pyrogram.enums` in this version, causing `ImportError` at startup. This broke the pre-existing inline/ layer and all new plugins.

**How to apply:** When writing any InlineKeyboardButton, use only:
```python
InlineKeyboardButton(text="...", callback_data="...")
InlineKeyboardButton(text="...", url="...")
```
If ButtonStyle is needed in future, upgrade pyrofork first and verify the import works.
