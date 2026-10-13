"""Modern PyTgCalls adapter for the legacy Meow command handlers.

The upstream API uses play/leave_call/pause/resume and on_update.
This adapter preserves existing call sites without importing removed input_stream APIs.
"""
from dataclasses import dataclass
from pytgcalls import PyTgCalls

@dataclass(frozen=True)
class AudioPiped:
    source: str

@dataclass(frozen=True)
class AudioVideoPiped:
    source: str
    audio_quality: object = None
    video_quality: object = None

class HighQualityAudio: pass
class HighQualityVideo: pass
class MediumQualityVideo: pass
class LowQualityVideo: pass

class StreamType:
    pulse_stream = None  # Old stream mode no longer exists in the current API.

class ModernCalls(PyTgCalls):
    @staticmethod
    def _source(stream):
        return stream.source if isinstance(stream, (AudioPiped, AudioVideoPiped)) else stream

    async def join_group_call(self, chat_id, stream, **kwargs):
        return await self.play(chat_id, self._source(stream))

    async def change_stream(self, chat_id, stream):
        return await self.play(chat_id, self._source(stream))

    async def leave_group_call(self, chat_id):
        return await self.leave_call(chat_id)

    async def pause_stream(self, chat_id):
        return await self.pause(chat_id)

    async def resume_stream(self, chat_id):
        return await self.resume(chat_id)
