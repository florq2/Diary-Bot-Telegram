import io
import whisper
from pydub import AudioSegment
from aiogram.types import Message

from bot import bot

model = whisper.load_model("small")


async def audio_to_text(path: str) -> str:
    result = model.transcribe(path, language="ru", fp16=False)

    return result["text"]


async def save_as_mp3(message: Message) -> str:
    voice_file_info = await bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)

    voice_mp3_path = f"voice_files/voice-{message.voice.file_id}.mp3"
    AudioSegment.from_file(voice_ogg, "ogg").export(
        voice_mp3_path, format="mp3"
    )

    return voice_mp3_path
