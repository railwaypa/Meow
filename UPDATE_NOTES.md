# Meow maintenance update

This is a conservative compatibility/bug-fix release, **not** a verified migration to the latest PyTgCalls API. The old 0.8.x stream API is retained because the player is written against it. Do not blindly upgrade `py-tgcalls` without porting all stream handlers.

Fixes: explicit session-string client initialization; consistent ALIVE_MSG variable (legacy alias supported); compose SESSION mismatch; duplicate yt-dlp helper overriding audio format; invalid quality condition; stream-end notification indexing when queue empties; extraction timeout and exit-code handling; sample environment and ignored secrets; playlist count initialization.

Run: copy `.env.example` to `.env`, fill credentials privately, `docker compose up --build -d`. Alternatively install `requirements.txt` with Python 3.10 and run `python main.py`. Telegram authorization, live VC and YouTube availability require real credentials and network access and were not tested here.
