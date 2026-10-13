# Meow modern PyTgCalls migration (test build)

- Migrated removed `input_stream`, `StreamType`, and stream-end APIs to the modern PyTgCalls interfaces.
- Replaced old join/change/leave/pause/resume calls through `Modules/helpers/modern_calls.py`.
- Uses maintained Pyrogram-compatible `pyrogrammod` dependency.
- Audio/video inputs are now passed to the current `play` media autodetection; legacy video quality settings are not enforced by this adapter.
- Requires Python >=3.10, ffmpeg, and real Telegram voice-chat tests.
- This is a migration candidate, NOT a claim of verified live playback. Report traceback and command used if an error occurs.
- Never commit `.env` or Telegram session strings.
