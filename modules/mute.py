from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, Message
from pyrogram.errors import RPCError

from config import HNDLR, SUDO_USERS


# ==========================================
# MUTE PERMISSIONS - PYROFORK 2.3.69
# ==========================================

mute_permission = ChatPermissions(
    can_send_messages=False,
)


# ==========================================
# MUTE COMMAND
# ==========================================

@Client.on_message(
    filters.user(SUDO_USERS)
    & filters.command(["mute"], prefixes=HNDLR)
)
@Client.on_message(
    filters.me
    & filters.command(["mute"], prefixes=HNDLR)
)
async def mute(client: Client, message: Message):

    # Allow only groups and supergroups
    if message.chat.type not in (
        enums.ChatType.GROUP,
        enums.ChatType.SUPERGROUP,
    ):
        await message.delete()
        return

    # ======================================
    # CHECK ADMIN PERMISSIONS
    # ======================================

    try:
        me = await client.get_me()

        member = await client.get_chat_member(
            message.chat.id,
            me.id,
        )

        if member.status not in (
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        ):
            await message.edit_text(
                "❌ You must be an admin to mute users."
            )
            return

        if (
            member.status == enums.ChatMemberStatus.ADMINISTRATOR
            and not member.privileges.can_restrict_members
        ):
            await message.edit_text(
                "❌ You don't have permission to restrict members."
            )
            return

    except Exception as e:
        await message.edit_text(
            f"❌ Permission check failed:\n`{e}`"
        )
        return

    # ======================================
    # GET TARGET USER
    # ======================================

    try:
        if (
            message.reply_to_message
            and message.reply_to_message.from_user
        ):
            user_id = message.reply_to_message.from_user.id

        elif len(message.command) > 1:
            user = await client.get_users(
                message.command[1]
            )
            user_id = user.id

        else:
            await message.edit_text(
                "❌ Reply to a user or provide a username.\n\n"
                "**Usage:** `.mute @username`"
            )
            return

    except Exception as e:
        await message.edit_text(
            f"❌ Unable to find user:\n`{e}`"
        )
        return

    # ======================================
    # PREVENT SELF-MUTE
    # ======================================

    if user_id == me.id:
        await message.edit_text(
            "❌ I cannot mute myself."
        )
        return

    # ======================================
    # MUTE USER
    # ======================================

    try:
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=mute_permission,
        )

        await message.delete()

    except RPCError as e:
        await message.edit_text(
            f"❌ **Mute Failed!**\n\n"
            f"**Error:** `{e}`"
        )

    except Exception as e:
        await message.edit_text(
            f"❌ **Unexpected Error!**\n\n"
            f"**Log:** `{e}`"
        )
