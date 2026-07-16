# Fariza - Uzbek AI Voice Assistant

> An open-source Uzbek-language AI voice assistant running on Telegram with speech-to-text, GPT-4o chat, and text-to-speech capabilities.

---

## O'zbekcha | Uzbek

### Fariza – O'zbekcha AI Ovoz Yordamchisi

**Fariza** – Telegramma'da ishlaidigan, o'zbekcha ishchi hisobiga (Telethon) qurilgan, ochiq manbalik AI ovoz yordamchisidir. U OpenAI GPT-4o bilan matnli va tasvir tahlili, UzbekVoice.ai orqali ovozni matniga o'girish (STT), va Aisha orqali matnni o'zbekcha ovozga o'girish (TTS) imkoniyatlarini taqdim etadi.

#### Xususiyatlari

- **Matnli chat**: GPT-4o bilan real-vaqt suhbat
- **Ovoz xabarlari**: Ovozni matniga o'girish, javobni o'zbekcha ovozga o'girish
- **Tasvir tahlili**: Rasmni tahlil qilish va tasvir haqida suq berilgan savolga javob berish
- **Foydalanuvchi limitlari**: Har bir foydalanuvchiga matn va ovoz so'rovlari uchun chegaralar
- **Arxiv**: Barcha foydalanuvchi xabarlari saqlanadi
- **Admin huquqlari**: Mastarali foydalanuvchi chegaralarni chugatlamaydi

#### O'rnatish

**Talab qilinadigan narsalar:**
- Python 3.8+
- Telegramma hisobvarisiga ega bo'lish
- OpenAI API kaliti
- UzbekVoice.ai API kaliti
- Aisha (aisha.group) API kaliti

**O'rnatish bosqichlari:**

1. **Repozitoriyani klonlash:**
   ```bash
   git clone https://github.com/yourusername/fariza-voice-assistant.git
   cd fariza-voice-assistant
   ```

2. **Virtual muhit yaratish:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac uchun
   # yoki
   venv\Scripts\activate  # Windows uchun
   ```

3. **Bog'liqliklarni o'rnatish:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Telegram API kalitlarini olish:**
   - [my.telegram.org](https://my.telegram.org) ga o'ting
   - Ro'yxatdan o'ting va tizimga kiring
   - "API development tools" bo'limiga o'ting
   - `API_ID` va `API_HASH` ni nusxalang

5. **.env faylini konfiguratsiya qilish:**
   ```bash
   cp .env.example .env
   ```
   `.env` faylida quyidagi ma'lumotlarni to'ldiring:
   ```
   API_ID=YOUR_API_ID
   API_HASH=YOUR_API_HASH
   OPENAI_KEY=YOUR_OPENAI_API_KEY
   UZVOICE_KEY=YOUR_UZBEKVOICE_API_KEY
   AISHA_KEY=YOUR_AISHA_API_KEY
   ADMIN_ID=YOUR_TELEGRAM_USER_ID
   STORAGE_DIR=storage
   ```

6. **Faollashtirish:**
   ```bash
   python main.py
   ```
   Birinchi marta ishga tushirganda, Telegramma raqamingizni kiritishingiz talab qilinadi.

#### Konfiguratsiya Jadvali

| O'zgaruvchi | Tavsifi | Misol |
|---|---|---|
| `API_ID` | Telegram API IDsi (my.telegram.org dan) | `123456789` |
| `API_HASH` | Telegram API hash (my.telegram.org dan) | `abcdef1234567890` |
| `OPENAI_KEY` | OpenAI API kaliti | `sk-...` |
| `UZVOICE_KEY` | UzbekVoice.ai API kaliti | `api_key_...` |
| `AISHA_KEY` | Aisha.group API kaliti | `aisha_key_...` |
| `ADMIN_ID` | Administrator Telegram ID raqami | `987654321` |
| `STORAGE_DIR` | Saqlash katalogi | `storage` |

#### Foydalanish

1. **Matnli xabar yuborish:**
   - Forizaga oddiy xabar yuboring
   - Fariza GPT-4o orqali javob beradi

2. **Ovoz xabarini yuborish:**
   - Ovoz xabarini Forizaga yuboring
   - Ovoz matniga o'giriladi, GPT-4o javob beradi, javob o'zbekcha ovozga o'giriladi

3. **Rasmni tahlil qilish:**
   - Rasmni Forizaga yuboring
   - Xabar yuboring (topshiriq/savol)
   - Fariza GPT-4o orqali rasimni tahlil qilib javob beradi

#### Xavfsizlik

- **.env faylini hech qachon commit qilmang!** Unda maxfiy kalitlar saqlanadi
- `.env` faylini `.gitignore` ga qo'shing
- Kalitlaringizni hech kimbaga bermang
- Agar kalitingiz ushshirilsa, uni darhol yangilab qo'ying

#### Bog'liqliklar

- **telethon** - Telegram API bilan ishlash
- **openai** - GPT-4o bilan integratsiya
- **pydub** - Audio qayta ishlash
- **requests** - HTTP so'rovlar
- **python-dotenv** - .env faylini o'qish
- **imageio-ffmpeg** - Audio konvertatsiya

#### Fariza haqida

**Fariza** - bu **Ozodbek Hoshimov** tomonidan yaratilgan, uning eng yaqin do'sti va yordamchisiga bag'ishlanishi kerak bo'lgan o'zbekcha AI yordamchisidir. Fariza do'stona va samimiy ohangda javob berib, foydalanuvchilarning savollariga yordamchi bo'ladi.

---

## English

### Fariza – Uzbek AI Voice Assistant

**Fariza** is an open-source Uzbek-language AI voice assistant built to run on Telegram as a Telethon user client. It leverages OpenAI's GPT-4o for chat and image analysis, UzbekVoice.ai for speech-to-text (Uzbek), and Aisha for text-to-speech (Uzbek voice).

#### Features

- **Text Chat**: Real-time conversation with GPT-4o
- **Voice Messages**: Converts speech to text, processes with GPT-4o, and responds with Uzbek speech synthesis
- **Image Analysis**: Analyzes images and answers user queries about them
- **Per-User Rate Limits**: Configurable limits for text and voice requests per user
- **Message Archive**: Logs all user interactions for reference
- **Admin Privileges**: Administrator bypasses rate limits

#### Requirements

- Python 3.8+
- Telegram account (personal user account)
- OpenAI API key
- UzbekVoice.ai API key
- Aisha.group API key

#### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/fariza-voice-assistant.git
   cd fariza-voice-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain Telegram API credentials:**
   - Visit [my.telegram.org](https://my.telegram.org)
   - Sign up or log in
   - Navigate to "API development tools"
   - Copy your `API_ID` and `API_HASH`

5. **Configure .env file:**
   ```bash
   cp .env.example .env
   ```
   Fill in the `.env` file with your credentials:
   ```
   API_ID=YOUR_API_ID
   API_HASH=YOUR_API_HASH
   OPENAI_KEY=YOUR_OPENAI_API_KEY
   UZVOICE_KEY=YOUR_UZBEKVOICE_API_KEY
   AISHA_KEY=YOUR_AISHA_API_KEY
   ADMIN_ID=YOUR_TELEGRAM_USER_ID
   STORAGE_DIR=storage
   ```

6. **Start the assistant:**
   ```bash
   python main.py
   ```
   On first run, you will be prompted to enter your Telegram phone number for authentication.

#### Configuration

| Variable | Description | Example |
|---|---|---|
| `API_ID` | Telegram API ID (from my.telegram.org) | `123456789` |
| `API_HASH` | Telegram API hash (from my.telegram.org) | `abcdef1234567890` |
| `OPENAI_KEY` | OpenAI API key | `sk-...` |
| `UZVOICE_KEY` | UzbekVoice.ai API key | `api_key_...` |
| `AISHA_KEY` | Aisha.group API key | `aisha_key_...` |
| `ADMIN_ID` | Administrator's Telegram user ID | `987654321` |
| `STORAGE_DIR` | Directory for storing message logs | `storage` |

#### Usage

1. **Send a text message:**
   - Send any text message to Fariza
   - Receive a GPT-4o response

2. **Send a voice message:**
   - Record and send a voice message
   - Speech is transcribed, processed by GPT-4o, and responded to with Uzbek voice synthesis

3. **Analyze an image:**
   - Send an image to Fariza
   - Follow with a text message containing your query or instruction
   - Fariza analyzes the image using GPT-4o and responds

#### Security

- **Never commit the `.env` file!** It contains sensitive API keys
- Add `.env` to `.gitignore`
- Do not share your API keys with anyone
- Rotate keys immediately if they are compromised

#### Dependencies

- **telethon** - Telegram client library
- **openai** - Integration with GPT-4o
- **pydub** - Audio processing
- **requests** - HTTP requests
- **python-dotenv** - Environment variable management
- **imageio-ffmpeg** - Audio format conversion

#### About Fariza

**Fariza** is dedicated as a tribute to **Ozodbek Khoshimov**, as their closest friend and assistant. The assistant responds with a friendly and sincere tone, providing helpful answers to user queries in the Uzbek language.

---

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

For questions or issues, please open an issue on the GitHub repository.
