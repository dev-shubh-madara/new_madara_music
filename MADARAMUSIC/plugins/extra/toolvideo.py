import os
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from MADARAMUSIC import app
from config import BANNED_USERS


def convert_video_to_text(video_path):
    try:
        from pydub import AudioSegment
        import speech_recognition as sr
    except ImportError:
        raise RuntimeError("pydub and SpeechRecognition are required for this command.")

    audio = AudioSegment.from_file(video_path)
    audio.export("audio.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data)
    return text


@app.on_message(filters.command("vtxt") & filters.reply & ~BANNED_USERS)
async def convert_video_to_text_cmd(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.video:
        return await message.reply_text("❌ Reply to a video message to convert it to text.")

    m = await message.reply_text("⏳ <b>Downloading and processing video...</b>")
    video_path = await message.reply_to_message.download()
    try:
        text_result = convert_video_to_text(video_path)
    except RuntimeError as e:
        await m.edit_text(f"❌ {e}")
        return
    except Exception as e:
        await m.edit_text(f"❌ <b>Failed to extract text:</b> <code>{e}</code>")
        return
    finally:
        try:
            os.remove(video_path)
        except Exception:
            pass

    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(text_result)

    await m.delete()
    await message.reply_document("file.txt", caption="📝 Extracted text from video.")
    try:
        os.remove("file.txt")
    except Exception:
        pass


@app.on_message(filters.command("remove", prefixes="/") & filters.reply & ~BANNED_USERS)
async def remove_media(client, message: Message):
    replied = message.reply_to_message
    if not replied or not replied.video:
        return await message.reply_text("❌ Reply to a video message.")

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Specify what to remove: <code>/remove audio</code> or <code>/remove video</code>"
        )

    command = message.command[1].lower()
    m = await message.reply_text("⏳ <b>Processing...</b>")
    file_path = await replied.download()

    try:
        if command == "audio":
            os.system(f'ffmpeg -y -i "{file_path}" -c:v copy -an output_novid.mp4 -loglevel quiet')
            await message.reply_video("output_novid.mp4", caption="🎬 Video with audio removed.")
            os.remove("output_novid.mp4")
        elif command == "video":
            os.system(f'ffmpeg -y -i "{file_path}" -vn -c:a copy output_noaud.mp3 -loglevel quiet')
            await message.reply_audio("output_noaud.mp3", caption="🎵 Audio extracted from video.")
            os.remove("output_noaud.mp3")
        else:
            await m.edit_text("❌ Invalid option. Use <code>/remove audio</code> or <code>/remove video</code>.")
            return
    except Exception as ex:
        await m.edit_text(f"❌ <b>Error:</b> <code>{ex}</code>")
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass

    await m.delete()
