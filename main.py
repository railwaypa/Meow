
import asyncio
import logging
import traceback
import importlib.metadata

import pyrogram

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
            LOGGER.info("%s Version: %s", package, version)

        except importlib.metadata.PackageNotFoundError:
            LOGGER.warning("%s is not installed", package)

    LOGGER.info("=" * 45)


# ==========================================
# MAIN FUNCTION
# ==========================================

async def main():

    bot_started = False
    calls_started = False

    check_versions()

    try:
        # ==================================
        # START PYROGRAM CLIENT
        # ==================================

        LOGGER.info("STARTING PYROGRAM CLIENT...")

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

        LOGGER.info("STARTING PYTGCALLS CLIENT...")

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
            "=======================================\n"
        )

        # ==================================
        # KEEP BOT RUNNING
        # ==================================

        LOGGER.info("WAITING FOR TELEGRAM UPDATES...")

        await idle()

    except KeyboardInterrupt:
        LOGGER.info("KEYBOARD INTERRUPT RECEIVED")

    except asyncio.CancelledError:
        LOGGER.warning("MAIN TASK CANCELLED")
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

        # Stop PyTgCalls first
        if calls_started:
            try:
                LOGGER.info("STOPPING PYTGCALLS...")

                await call_py.stop()

                LOGGER.info(
                    "PYTGCALLS STOPPED SUCCESSFULLY"
                )

            except Exception:
                LOGGER.error(
                    "PYTGCALLS STOP ERROR",
                    exc_info=True
                )

        # Stop Pyrogram
        if bot_started:
            try:
                LOGGER.info("STOPPING PYROGRAM...")

                await bot.stop()

                LOGGER.info(
                    "PYROGRAM STOPPED SUCCESSFULLY"
                )

            except Exception:
                LOGGER.error(
                    "PYROGRAM STOP ERROR",
                    exc_info=True
                )

        LOGGER.info("MEOW USERBOT SHUTDOWN COMPLETE")


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        LOGGER.info("PROCESS INTERRUPTED")

    except Exception:
        LOGGER.critical(
            "MEOW PROCESS TERMINATED DUE TO ERROR",
            exc_info=True
        )
        raise SystemExit(1)
