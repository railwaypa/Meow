import asyncio
import logging
import traceback
import importlib.metadata

import pyrogram

from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pytgcalls import idle

from config import bot, call_py, HNDLR


# ============================================================
# BUILD IDENTIFICATION
# ============================================================

BUILD_VERSION = "MEOW-CMD-FIX-V38"

print(
    f"\n[BUILD CHECK] {BUILD_VERSION} | NEW MAIN.PY LOADED\n",
    flush=True,
)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    force=True,
)

LOGGER = logging.getLogger("Meow")


# ============================================================
# DEPENDENCY VERSION CHECK
# ============================================================

def check_versions():

    LOGGER.info("=" * 45)
    LOGGER.info("MEOW DEPENDENCY VERSION CHECK")
    LOGGER.info("=" * 45)

    LOGGER.info(
        "Build Version: %s",
        BUILD_VERSION,
    )

    LOGGER.info(
        "Pyrogram Version: %s",
        getattr(pyrogram, "__version__", "Unknown"),
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
                version,
            )

        except importlib.metadata.PackageNotFoundError:
            LOGGER.warning(
                "%s is not installed",
                package,
            )

    LOGGER.info(
        "Configured Command Prefix: %r",
        HNDLR,
    )

    LOGGER.info("=" * 45)


# ============================================================
# DIRECT TELEGRAM UPDATE DEBUG
# ============================================================

async def direct_update_debug(client, message):

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
            "sender_id=%s | outgoing=%s | text=%r",
            message.chat.id,
            sender_id,
            message.outgoing,
            text[:100],
        )

        # ====================================================
        # DIRECT TEST COMMAND
        # ====================================================

        command = text.strip().lower()

        valid_commands = {
            ".testmeow",
            f"{HNDLR}testmeow".lower(),
        }

        if command not in valid_commands:
            return

        LOGGER.warning(
            "[DIRECT TEST] Test command detected"
        )

        me = await client.get_me()

        if sender_id != me.id:
            LOGGER.warning(
                "[DIRECT TEST] Ignored: sender is not session owner"
            )
            return

        LOGGER.warning(
            "[DIRECT TEST] Sender verified"
        )

        await message.edit_text(
            "✅ MEOW DIRECT TEST SUCCESS!\n\n"
            "Pyrogram is receiving Telegram updates.\n"
            "Direct message handler is working.\n\n"
            f"Build: {BUILD_VERSION}"
        )

        LOGGER.warning(
            "[DIRECT TEST] COMMAND EXECUTED SUCCESSFULLY"
        )

    except Exception:
        LOGGER.error(
            "[DIRECT UPDATE] HANDLER ERROR\n%s",
            traceback.format_exc(),
        )


# ============================================================
# REGISTER DIRECT DEBUG HANDLER
# ============================================================

def register_debug_handler():

    LOGGER.warning(
        "[DEBUG] Starting direct handler registration..."
    )

    bot.add_handler(
        MessageHandler(
            direct_update_debug,
            filters.all,
        ),
        group=-200,
    )

    LOGGER.warning(
        "[DEBUG] Direct update handler registered in group -200"
    )

    print(
        "[BUILD CHECK] DIRECT DEBUG HANDLER REGISTERED",
        flush=True,
    )


# ============================================================
# MAIN FUNCTION
# ============================================================

async def main():

    bot_started = False
    calls_started = False

    LOGGER.warning(
        "[BUILD CHECK] MAIN FUNCTION EXECUTED | %s",
        BUILD_VERSION,
    )

    check_versions()

    try:

        # ====================================================
        # REGISTER DEBUG HANDLER BEFORE STARTUP
        # ====================================================

        register_debug_handler()

        # ====================================================
        # START PYROGRAM CLIENT
        # ====================================================

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
                me.id,
            )

            LOGGER.info(
                "LOGGED IN USERNAME: @%s",
                me.username or "None",
            )

            LOGGER.warning(
                "[DEBUG] Telegram session owner verified"
            )

            LOGGER.warning(
                "[DEBUG] Send .testmeow from the logged-in account"
            )

        except Exception:
            LOGGER.error(
                "FAILED TO START PYROGRAM CLIENT"
            )

            LOGGER.error(
                "FULL PYROGRAM TRACEBACK:\n%s",
                traceback.format_exc(),
            )

            raise

        # ====================================================
        # START PYTGCALLS CLIENT
        # ====================================================

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
                traceback.format_exc(),
            )

            raise

        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

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

        LOGGER.warning(
            "[BUILD CHECK] %s FULLY STARTED",
            BUILD_VERSION,
        )

        # ====================================================
        # KEEP BOT RUNNING
        # ====================================================

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
            exc_info=True,
        )
        raise

    finally:

        LOGGER.info("=" * 45)
        LOGGER.info("STOPPING MEOW USERBOT")
        LOGGER.info("=" * 45)

        # ====================================================
        # STOP PYTGCALLS FIRST
        # ====================================================

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
                    exc_info=True,
                )

        # ====================================================
        # STOP PYROGRAM
        # ====================================================

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
                    exc_info=True,
                )

        LOGGER.info(
            "MEOW USERBOT SHUTDOWN COMPLETE"
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    print(
        f"[BUILD CHECK] EXECUTING MAIN ENTRY POINT: {BUILD_VERSION}",
        flush=True,
    )

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        LOGGER.info(
            "PROCESS INTERRUPTED"
        )

    except Exception:
        LOGGER.critical(
            "MEOW PROCESS TERMINATED DUE TO ERROR",
            exc_info=True,
        )

        raise SystemExit(1)
