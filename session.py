import asyncio
import os

from pyrogram import Client


# ==============================
# Pyrogram 2.0.106 Session Generator
# ==============================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


async def main():
    if not API_ID or not API_HASH:
        print("❌ ERROR: API_ID or API_HASH is missing.")
        print()
        print("Set these environment variables first:")
        print("  API_ID=123456")
        print("  API_HASH=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return

    try:
        api_id = int(API_ID)
    except ValueError:
        print("❌ ERROR: API_ID must be a number.")
        return

    print("=" * 55)
    print("       MEOW USERBOT SESSION GENERATOR")
    print("       Pyrogram 2.0.106")
    print("=" * 55)
    print()
    print("Starting Telegram authentication...")
    print("Enter your phone number with country code.")
    print("Example: +919876543210")
    print()

    # IMPORTANT:
    # in_memory=True is the correct Pyrogram 2.x way
    # to create a temporary session and export it.
    app = Client(
        name="meow_session",
        api_id=api_id,
        api_hash=API_HASH,
        in_memory=True,
    )

    try:
        await app.start()

        me = await app.get_me()

        print()
        print("✅ Telegram authentication successful!")
        print()
        print(f"👤 Name : {me.first_name or ''}")
        print(f"🆔 ID   : {me.id}")
        print(f"🔗 User : @{me.username}" if me.username else "🔗 User : No username")
        print()

        session_string = await app.export_session_string()

        print("=" * 55)
        print("               SESSION STRING")
        print("=" * 55)
        print()
        print(session_string)
        print()
        print("=" * 55)
        print("⚠️  KEEP THIS SESSION PRIVATE!")
        print("⚠️  Anyone with this string may access")
        print("    your Telegram account.")
        print("=" * 55)

    except Exception as e:
        print()
        print(f"❌ SESSION GENERATION FAILED: {type(e).__name__}: {e}")

    finally:
        try:
            await app.stop()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
