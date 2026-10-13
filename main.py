import asyncio
import logging
import traceback
import importlib.metadata

import pyrogram

from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pytgcalls import idle

from config import bot, call_py


# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

LOGGER = logging.getLogger("Meow")


# ==========================================
# DEPENDENCY VERSION CHECK
# ==========================================

def check_versions():
    LOGGER.info("=" * 45)
    LOGGER.info("MEOW DEPENDENCY VERSION CHECK")
    LOGGER.info("=" * 45)

    LOGGER.info(
        "Pyrogram Version: %s",
        getattr(pyrogram, "__version__", "Unknown")
    )

    for package in (
        "pyrofork",
        "py-tgcalls",
        "TgCrypto",
    ):
        try:
            version = importlib.metadata.version(package)

            LOGGER.info(
                "%s Version: %s",
                package,
                version
            )

        except importlib.metadata.PackageNotFoundError:
            LOGGER.warning(
                "%s is not installed",
                package
            )

    LOGGER.info("=" * 45)


# ==========================================
# DIRECT TELEGRAM UPDATE DEBUG
# ==========================================

async def direct_update_debug(client, message):
    """
    Diagnostic handler.

    Does not depend on:
    - filters.me
    - filters.command
    - HNDLR

    Used to check whether Telegram message
    updates are reaching the Pyrogram client.
    """

    try:
        text = message.text or message.caption or ""

        if not text:
            return

        sender_id = (
            message.from_user.id
            if message.from_user
            else None
        )

        LOGGER.warning(
            "[DIRECT UPDATE] chat_id=%s | "
            "from_user=%s | outgoing=%s | text=%r",
            message.chat.id,
            sender_id,
            message.outgoing,
            text[:100]
        )

        # ==================================
        # DIRECT TEST COMMAND
        # ==================================

        if text.strip().lower() != ".testmeow":
            return

        LOGGER.warning(
            "[DIRECT TEST] .testmeow detected"
        )

        me = await client.get_me()

        # Only session owner can execute test
        if sender_id != me.id:
            LOGGER.warning(
                "[DIRECT TEST] Ignored: sender is not session owner"
            )
            return

        LOGGER.warning(
            "[DIRECT TEST] Sender verified: %s",
            me.id
        )

        await message.edit_text(
            "✅ MEOW DIRECT UPDATE TEST SUCCESS!\n\n"
            "Telegram updates are being received.\n"
            "Message handler is executing correctly."
        )

        LOGGER.warning(
            "[DIRECT TEST] COMMAND EXECUTED SUCCESSFULLY"
        )

    except Exception:
        LOGGER.error(
            "[DIRECT UPDATE] HANDLER ERROR\n%s",
            traceback.format_exc()
        )


# ==========================================
# REGISTER DIRECT DEBUG HANDLER
# ==========================================

def register_debug_handler():
    """
    Register before bot.start() so the handler
    is available as soon as Pyrogram starts.
    """

    bot.add_handler(
        MessageHandler(
            direct_update_debug,
            filters.all
        ),
        group=-200
    )

    LOGGER.info(
        "[DEBUG] Direct update handler registered "
        "in group -200"
    )


# ==========================================
# MAIN FUNCTION
# ==========================================

async def main():

    bot_started = False
    calls_started = False

    check_versions()

    try:

        # ==================================
        # REGISTER DEBUG HANDLER
        # ==================================

        register_debug_handler()

        # ==================================
        # START PYROGRAM CLIENT
        # ==================================

        LOGGER.info(
            "STARTING PYROGRAM CLIENT..."
        )

        try:
            await bot.start()

            bot_started = True

            LOGGER.info(
                "PYROGRAM CLIENT STARTED SUCCESSFULLY"
            )

            me = await bot.get_me()

            LOGGER.info(
                "LOGGED IN USER ID: %s",
                me.id
            )

            LOGGER.info(
                "LOGGED IN USERNAME: @%s",
                me.username or "None"
            )

            LOGGER.info(
                "[DEBUG] Send .testmeow from this "
                "Telegram account to test updates"
            )

        except Exception:
            LOGGER.error(
                "FAILED TO START PYROGRAM CLIENT"
            )

            LOGGER.error(
                "FULL PYROGRAM TRACEBACK:\n%s",
                traceback.format_exc()
            )

            raise

        # ==================================
        # START PYTGCALLS CLIENT
        # ==================================

        LOGGER.info(
            "STARTING PYTGCALLS CLIENT..."
        )

        try:
            await call_py.start()

            calls_started = True

            LOGGER.info(
                "PYTGCALLS CLIENT STARTED SUCCESSFULLY"
            )

        except Exception:
            LOGGER.error(
                "FAILED TO START PYTGCALLS CLIENT"
            )

            LOGGER.error(
                "FULL PYTGCALLS TRACEBACK:\n%s",
                traceback.format_exc()
            )

            raise

        # ==================================
        # SUCCESS MESSAGE
        # ==================================

        LOGGER.info(
            "\n"
            "=======================================\n"
            "       MEOW USERBOT + MUSIC V2         \n"
            "=======================================\n"
            "  Pyrogram : STARTED                   \n"
            "  PyTgCalls: STARTED                   \n"
            "  Status   : RUNNING                   \n"
            "  Debug    : ENABLED                   \n"
            "=======================================\n"
        )

        # ==================================
        # KEEP BOT RUNNING
        # ==================================

        LOGGER.info(
            "WAITING FOR TELEGRAM UPDATES..."
        )

        await idle()

    except KeyboardInterrupt:
        LOGGER.info(
            "KEYBOARD INTERRUPT RECEIVED"
        )

    except asyncio.CancelledError:
        LOGGER.warning(
            "MAIN TASK CANCELLED"
        )
        raise

    except Exception:
        LOGGER.critical(
            "MEOW STARTUP / RUNTIME FAILURE",
            exc_info=True
        )
        raise

    finally:

        LOGGER.info("=" * 45)
        LOGGER.info("STOPPING MEOW USERBOT")
        LOGGER.info("=" * 45)

        # ==================================
        # STOP PYTGCALLS FIRST
        # ==================================

        if calls_started:
            try:
                LOGGER.info(
                    "STOPPING PYTGCALLS..."
                )

                await call_py.stop()

                LOGGER.info(
                    "PYTGCALLS STOPPED SUCCESSFULLY"
                )

            except Exception:
                LOGGER.error(
                    "PYTGCALLS STOP ERROR",
                    exc_info=True
                )

        # ==================================
        # STOP PYROGRAM
        # ==================================

        if bot_started:
            try:
                LOGGER.info(
                    "STOPPING PYROGRAM..."
                )

                await bot.stop()

                LOGGER.info(
                    "PYROGRAM STOPPED SUCCESSFULLY"
                )

            except Exception:
                LOGGER.error(
                    "PYROGRAM STOP ERROR",
                    exc_info=True
                )

        LOGGER.info(
            "MEOW USERBOT SHUTDOWN COMPLETE"
        )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        LOGGER.info(
            "PROCESS INTERRUPTED"
        )

    except Exception:
        LOGGER.critical(
            "MEOW PROCESS TERMINATED DUE TO ERROR",
            exc_info=True
        )

        raise SystemExit(1)
