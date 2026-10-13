import os
import time
import base64
import binascii

from dotenv import load_dotenv
from pyrogram import Client, filters
from modules.helpers.modern_calls import ModernCalls


__version__ = "v0.1"

load_dotenv()


# ============================================================
# ENV
# ============================================================

API_ID_RAW = os.getenv("API_ID", "").strip()
API_HASH = os.getenv("API_HASH", "").strip()
SESSION = os.getenv("SESSION", "").strip()

HNDLR = os.getenv("HNDLR", ".").strip()

ALIVE_PIC = os.getenv("ALIVE_PIC", "").strip()
ALIVE_MSG = os.getenv("ALIVE_MSG", os.getenv("AlIVE_MSG", "")).strip()
PING_MSG = os.getenv("PING_MSG", "").strip()
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL", "").strip()


# ============================================================
# API ID
# ============================================================

try:
    API_ID = int(API_ID_RAW)
except (TypeError, ValueError):
    raise ValueError("API_ID is invalid.")


if API_ID <= 0:
    raise ValueError("API_ID is missing or invalid.")


# ============================================================
# API HASH
# ============================================================

if not API_HASH:
    raise ValueError("API_HASH is missing.")


# ============================================================
# SESSION
# ============================================================

if not SESSION:
    raise ValueError("SESSION is missing.")


# ============================================================
# SESSION DEBUG
# ============================================================

print("========================================")
print("PYROGRAM SESSION CHECK")
print("========================================")

print(f"SESSION characters: {len(SESSION)}")

try:
    padded = SESSION + ("=" * (-len(SESSION) % 4))
    decoded = base64.urlsafe_b64decode(padded)

    print(f"SESSION decoded bytes: {len(decoded)}")

except (binascii.Error, ValueError, TypeError) as e:
    print(f"SESSION decode error: {e}")

print("========================================")


# ============================================================
# SUDO USERS
# ============================================================

SUDO_USERS = []

sudo_raw = os.getenv("SUDO_USERS", "").strip()

if sudo_raw:
    for user_id in sudo_raw.replace(",", " ").split():
        try:
            SUDO_USERS.append(int(user_id))
        except ValueError:
            pass


# ============================================================
# CONTACT FILTER
# ============================================================

contact_filter = filters.create(
    lambda _, __, message:
        (
            message.from_user
            and message.from_user.is_contact
        )
        or message.outgoing
)


# ============================================================
# PYROGRAM
# ============================================================

print("Initializing Pyrogram CLIENT...")

try:
    bot = Client(
    name="meow",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    plugins=dict(root="modules"),
)

except Exception as e:
    print(f"PYROGRAM CLIENT CONFIG ERROR: {e}")
    raise


# ============================================================
# PYTGCALLS
# ============================================================

call_py = ModernCalls(bot)


# ============================================================
# GLOBALS
# ============================================================

hl = HNDLR[0] if HNDLR else "."

start_time = time.time()

print("Pyrogram CLIENT configuration loaded.")
