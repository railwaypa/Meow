import asyncio

from pytgcalls import idle

from config import bot, call_py


async def main():
    print("STARTING Pyrogram CLIENT")

    try:
        await bot.start()
    except Exception as e:
        print(f"FAILED TO START PYROGRAM CLIENT: {e}")
        print(
            "Please check API_ID, API_HASH and SESSION in Heroku Config Vars."
        )
        return

    print("PYROGRAM CLIENT STARTED")

    try:
        print("STARTING PYTGCALLS CLIENT")
        await call_py.start()
        print("PYTGCALLS CLIENT STARTED")

        print(
            """
-------------------------------
 Meow Userbot + Music Activated!
-------------------------------
"""
        )

        await idle()

    except KeyboardInterrupt:
        print("STOPPING USERBOT")

    except Exception as e:
        print(f"RUNTIME ERROR: {e}")

    finally:
        print("STOPPING USERBOT")

        try:
            await call_py.stop()
        except Exception as e:
            print(f"PYTGCALLS STOP ERROR: {e}")

        try:
            await bot.stop()
        except Exception as e:
            print(f"PYROGRAM STOP ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(main())
