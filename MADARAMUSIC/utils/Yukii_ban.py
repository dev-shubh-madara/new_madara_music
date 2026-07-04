from pyrogram import filters
from pyrogram.enums import ChatMemberStatus


async def _admin_check(_, client, message):
    if not message.chat:
        return False
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception:
        return False


admin_filter = filters.create(_admin_check)
