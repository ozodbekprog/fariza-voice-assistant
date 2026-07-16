from telethon import TelegramClient, events
from telethon.events import StopPropagation
from openai import AsyncOpenAI
import asyncio
import os
from datetime import datetime
from pydub import AudioSegment
import requests
import base64
from mimetypes import guess_type
import os
from pathlib import Path
from pydub import AudioSegment
import imageio_ffmpeg
from dotenv import load_dotenv
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

# .env faylidan maxfiy kalitlarni yuklaymiz
load_dotenv()


STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage"))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


# 🔐 API kalitlar — barchasi .env faylidan o'qiladi (kodga hech qachon yozilmaydi!)
api_id      = int(os.environ["API_ID"])
api_hash    = os.environ["API_HASH"]
openai_key  = os.environ["OPENAI_KEY"]
uzvoice_key = os.environ["UZVOICE_KEY"]
aisha_key   = os.environ["AISHA_KEY"]
admin_id    = int(os.environ["ADMIN_ID"])

client = TelegramClient("fariza_user", api_id, api_hash)
gpt = AsyncOpenAI(api_key=openai_key)
chat_histories = {}
user_limits = {}
user_notified = set()

MAX_TEXT = 300
MAX_VOICE = 20

system_prompt = (
    "Siz Fariza – Ozodbek Hoshimov tomonidan yaratilgan, uning eng yaqin do‘sti va yordamchisisiz. "
    "Siz do‘stona, samimiy ohangda javob berasiz. Har doim hushmuomala va e’tiborli bo‘ling."
)

def log_user_message(user, text):
    os.makedirs("arxiv", exist_ok=True)
    filename = f"arxiv/{user.id}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"🧑‍💻 ID: {user.id}\n")
        f.write(f"👤 Username: {user.username}\n")
        f.write(f"📞 Phone: {getattr(user, 'phone', 'Noma’lum')}\n")
        f.write(f"⏰ {datetime.now()}\n")
        f.write(f"📩 {text}\n")
        f.write("="*40 + "\n")

async def ask_gpt(chat_id, user_input):
    history = chat_histories.setdefault(chat_id, [{"role": "system", "content": system_prompt}])
    history.append({"role": "user", "content": user_input})
    try:
        response = await gpt.chat.completions.create(
            model="gpt-4o",
            messages=history,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"⚠️ Xatolik yuz berdi: {e}"

def uzbekvoice_stt(api_key, file_path):
    url = 'https://uzbekvoice.ai/api/v1/stt'
    headers = {"Authorization": api_key}
    files = {"file": ("audio.mp3", open(file_path, "rb"))}
    data = {
        "return_offsets": "true",
        "run_diarization": "false",
        "language": "uz",
        "blocking": "true",
    }
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            print("📡 UzbekVoice javobi:", result)
            return result.get("result", {}).get("text", "[matn topilmadi]")
        else:
            return f"[❌ UzbekVoice xato]: {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "[❌ So‘rov vaqtida muammo]"

def aisha_tts(api_key, text, lang="uz", model="gulnoza", mood="happy", file_path="aisha_response.mp3"):
    url = "https://back.aisha.group/api/v1/tts/post/"
    headers = {
        "x-api-key": api_key,
        "X-Channels": "mono",
        "X-Quality": "128k",
        "X-Rate": "24000",
        "X-Format": "mp3"
    }
    data = {
        "transcript": text,
        "language": lang,
        "model": model,
        "mood": mood
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        print("🔁 TTS status:", response.status_code)
        if response.status_code in [200, 201]:
            result = response.json()
            audio_url = result.get("audio_path")
            if audio_url:
                audio_data = requests.get(audio_url)
                with open(file_path, "wb") as f:
                    f.write(audio_data.content)
                print(f"✅ Audio yuklandi: {file_path}")
                return file_path
            else:
                print("❌ audio_path topilmadi")
                return None
        else:
            print("❌ TTS javobi:", response.status_code, response.text)
            return None
    except Exception as e:
        print("❌ TTS istisno:", e)
        return None

async def voice_to_text(file_path: str) -> str:
    mp3_path = file_path.replace(".ogg", ".mp3")
    try:
        audio = AudioSegment.from_file(file_path)
        audio.export(mp3_path, format="mp3")
        return uzbekvoice_stt(uzvoice_key, mp3_path)
    except Exception as e:
        return f"[🎧 Xatolik: {e}]"
    finally:
        if os.path.exists(file_path): os.remove(file_path)
        if os.path.exists(mp3_path): os.remove(mp3_path)

photo_commands = {}

@client.on(events.NewMessage(incoming=True, func=lambda e: e.photo))
async def handle_photo(event):
    sender = await event.get_sender()
    if sender.is_self:
        return

    try:
        file_path = await event.download_media(file="photo.jpg")
        print(f"📥 Rasm yuklandi: {file_path}")
        await event.respond("📥 Rasm qabul qilindi! Endi menga qanday topshiriq berishni xohlaysiz?")
        photo_commands[sender.id] = file_path
    except Exception as e:
        await event.respond("❌ Rasmni yuklashda xatolik yuz berdi.")
        print("❌ Yuklash xatosi:", e)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.text))
async def handle_text_or_command(event):
    sender = await event.get_sender()
    if sender.is_self:
        return

    user_id = sender.id
    text = event.text.strip()

    if user_id in photo_commands:
        file_path = photo_commands.pop(user_id)
        await event.respond("🧠 Fariza rasmni tahlil qilmoqda...")
        try:
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode("utf-8")

            mime_type, _ = guess_type(file_path)
            if not mime_type:
                mime_type = "image/jpeg"

            response = await gpt.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Siz foydalanuvchiga rasm asosida topshiriqqa javob berasiz."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                        ]
                    }
                ],
                temperature=0.6
            )

            javob = response.choices[0].message.content.strip()
            await event.respond(f"📊 Natija:\n{javob}")
            os.remove(file_path)
        except Exception as e:
            await event.respond("❌ Rasmni ko‘rsatilgan topshiriqqa ko‘ra tahlil qilishda xatolik yuz berdi.")
            print("❌ Tahlil xatosi:", e)
    else:
        if user_id != admin_id:
            usage = user_limits.get(user_id, {"text": 0, "voice": 0})
            if usage["text"] >= MAX_TEXT:
                if user_id not in user_notified:
                    await event.respond("🚫 Sizning matnli so‘rovlar limitingiz tugagan.")
                    user_notified.add(user_id)
                return
            usage["text"] += 1
            user_limits[user_id] = usage

        log_user_message(sender, text)
        javob = await ask_gpt(user_id, text)
        await event.respond(javob)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.voice))
async def handle_voice(event):
    sender = await event.get_sender()
    if sender.is_self:
        return

    user_id = sender.id
    file_path = await event.download_media(file="voice.ogg")
    matn = await voice_to_text(file_path)

    if user_id != admin_id:
        usage = user_limits.get(user_id, {"text": 0, "voice": 0})
        if usage["voice"] >= MAX_VOICE:
            if user_id not in user_notified:
                await event.respond("🚫 Sizning ovozli so‘rovlar limitingiz tugagan.")
                user_notified.add(user_id)
            return
        usage["voice"] += 1
        user_limits[user_id] = usage

    log_user_message(sender, matn)
    javob = await ask_gpt(user_id, matn)
    audio_path = aisha_tts(aisha_key, javob)
    if audio_path and os.path.exists(audio_path):
        await client.send_file(event.chat_id, audio_path, voice_note=True)
        os.remove(audio_path)
    else:
        await event.respond(javob)

print("🚀 Fariza user-mode ishga tushdi...")
client.start()
client.run_until_disconnected()
