
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, SUDO_USERS

LOGGER = logging.getLogger("Meow.CommandDebug")


@Client.on_message(filters.all, group=-100)
async def debug_all_messages(client: Client, message: Message):
    text = message.text or message.caption or ""

    if not text:
        return

    LOGGER.warning(
        "MESSAGE DEBUG | chat_id=%s | from_user=%s | outgoing=%s | text=%r | prefix=%r",
        message.chat.id,
        message.from_user.id if message.from_user else None,
        message.outgoing,
        text[:100],
        HNDLR,
    )


@Client.on_message(
    filters.me & filters.command("testmeow", prefixes=HNDLR),
    group=-99,
)
async def test_meow(client: Client, message: Message):
    LOGGER.warning("TESTMEOW COMMAND MATCHED")

    await message.edit_text(
        "✅ Meow Userbot command handler is working!"
    )
