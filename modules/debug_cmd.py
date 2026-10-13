import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR

LOGGER = logging.getLogger("Meow.Debug")


@Client.on_message(filters.me, group=-100)
async def debug_messages(client: Client, message: Message):
    text = message.text or message.caption or ""

    LOGGER.warning(
        "DEBUG MESSAGE RECEIVED | chat=%s | outgoing=%s | text=%r | HNDLR=%r",
        message.chat.id,
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
        "✅ Meow command handler is working!"
    )
