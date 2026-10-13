import logging

from pyrogram import Client, filters
from pyrogram.types import Message

LOGGER = logging.getLogger("Meow.Debug")


@Client.on_message(filters.all, group=-100)
async def meow_debug(client: Client, message: Message):

    text = message.text or message.caption or ""

    if not text:
        return

    LOGGER.warning(
        "MEOW DEBUG | chat=%s | user=%s | outgoing=%s | text=%r",
        message.chat.id,
        message.from_user.id if message.from_user else None,
        message.outgoing,
        text[:100],
    )

    if text.strip().lower() != ".testmeow":
        return

    me = await client.get_me()

    if not message.from_user or message.from_user.id != me.id:
        LOGGER.warning("TEST IGNORED: Sender is not session owner")
        return

    LOGGER.warning("MEOW TEST COMMAND DETECTED")

    try:
        await message.edit_text(
            "✅ MEOW DEBUG SUCCESS!\n\n"
            "Telegram updates and message editing are working."
        )

        LOGGER.warning("MEOW TEST COMMAND EXECUTED SUCCESSFULLY")

    except Exception:
        LOGGER.exception("MEOW TEST COMMAND FAILED")
