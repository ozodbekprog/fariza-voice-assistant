# Fariza - Arxitektura va Ma'lumotlar Oqimi

Fariza bu Uzbek AI ovoz yordamchisi bo'lib, Telegram platformasi ustida Telethon user client orqali ishlaydi. Bu hujjat arxitekturaning asosiy tuzilishini, komponentlarini va ma'lumotlar oqimini tushuntiradi.

## Umumiy Ma'lumotlar Oqimi

```
┌─────────────────────────────────────────────────────────────────┐
│                       TELEGRAM FOYDALANUVCHI                     │
│                   (Xabar, Ovoz, Rasm jo'natish)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │   TELEGRAM CLIENT (Telethon)         │
        │  (Handler - xabarlarni qabul qilish) │
        └──────────────────────────────────────┘
                           │
                ┌──────────┼──────────┐
                │          │          │
                ▼          ▼          ▼
          ┌─────────┐ ┌─────────┐ ┌──────────┐
          │  OVOZ?  │ │  MATN?  │ │  RASM?   │
          └────┬────┘ └────┬────┘ └────┬─────┘
               │            │           │
       ┌───────▼──┐   ┌─────▼──┐  ┌────▼────┐
       │ UzbekVoice    │ GPT-4o │  │ GPT-4o  │
       │ STT (Speech-> │ (Matn  │  │ Vision  │
       │    Text)      │ Reply) │  │ Analysis│
       └───────┬──┘    └─────┬──┘  └────┬────┘
               │             │           │
               ▼             ▼           ▼
        ┌─────────────────────────────────────┐
        │     GPT-4o (Asosiy AI Moduli)       │
        │   (So'rov javobini yaratish)        │
        └─────────────────────────────────────┘
               │             │           │
               ▼             │           │
        ┌──────────────┐     │           │
        │ Aisha TTS    │     │           │
        │ (Text->Uzbek │     │           │
        │ Voice)       │     │           │
        └──────────┬───┘     │           │
                   │         │           │
                   └─────────┼───────────┘
                             │
                             ▼
        ┌──────────────────────────────────────┐
        │   RATE LIMITING (Har foydalanuvchi)  │
        │   MAX_TEXT=300, MAX_VOICE=20         │
        │   (Admin bypass mavjud)              │
        └──────────────────────────────────────┘
                             │
                             ▼
        ┌──────────────────────────────────────┐
        │  TELEGRAM CLIENT (Telethon)          │
        │  (Javobni jo'natish)                 │
        └──────────────────────────────────────┘
                             │
                             ▼
        ┌──────────────────────────────────────┐
        │       TELEGRAM FOYDALANUVCHISI       │
        │        (Ovoz yoki Matn Javob)        │
        └──────────────────────────────────────┘
```

## Asosiy Komponentlar

### 1. Telegram Client (Telethon)
- **Rol**: Telegram platforma bilan integratsiya
- **Vazifa**: Xabarlarni qabul qilish, ular turini aniqlash va javoblarni jo'natish
- **Konfiguratsiya**: `.env` faylidagi `API_ID` va `API_HASH` parametrlari orqali

### 2. GPT-4o Moduli (OpenAI)
- **Rol**: Asosiy AI intellekti
- **Vazifa**: Barcha savollarning javoblarini yaratish
- **Qo'llamish**: 
  - Matn xabarlarga javob berish
  - Ovoz xabarlarining transkriptsiyasiga javob berish
  - Rasm tahlil qilish va tavsif berish
- **Konfiguratsiya**: `.env` faylidagi `OPENAI_KEY`

### 3. UzbekVoice STT Moduli (Speech-to-Text)
- **Rol**: Ovoz xabarlarini tekstga o'girish
- **Vazifa**: Telegram'dan olingan audio fayllarini Uzbek tiliga transkribsiya qilish
- **Konfiguratsiya**: `.env` faylidagi `UZVOICE_KEY`
- **Foydalanish**: Faqat ovoz xabarlariga qo'llaniladi

### 4. Aisha TTS Moduli (Text-to-Speech)
- **Rol**: Javoblarni Uzbek tilida ovozga o'girish
- **Vazifa**: GPT-4o'ning matn javoblarini natural sounding Uzbek tilidagi ovoza aylantiramiz
- **Konfiguratsiya**: `.env` faylidagi `AISHA_KEY`
- **Foydalanish**: Ovoz xabarlariga javob berish uchun ishlatilinadi

### 5. Rate Limiting (Shumarish Mezoni)
- **Rol**: Misuse'ni oldini olish
- **Parametrlar**:
  - `MAX_TEXT`: Matn xabarlar uchun kunlik chegarasi (300)
  - `MAX_VOICE`: Ovoz xabarlar uchun kunlik chegarasi (20)
  - `ADMIN_ID`: Admin foydalanuvchi chegaralarni chetlab o'tishi mumkin
- **Implemented**: Har bir foydalanuvchi uchun alohida hisoblash

## Xabar Qayta Ishlash Mantiq

### Ovoz Xabari Oqimi
```
1. Telegram'dan ovoz fayli qabul qilish
2. Rate limit tekshirish (MAX_VOICE)
3. UzbekVoice STT: Ovozni Uzbek matniga o'girish
4. GPT-4o: Transkribsiya qilingan matnning javobini yaratish
5. Aisha TTS: Javobni Uzbek ovoziga o'girish
6. Telegram'ga audio fayl jo'natish
```

### Matn Xabari Oqimi
```
1. Telegram'dan matn xabari qabul qilish
2. Rate limit tekshirish (MAX_TEXT)
3. GPT-4o: Matnning javobini yaratish
4. Telegram'ga matn javob jo'natish
```

### Rasm Xabari Oqimi
```
1. Telegram'dan rasm qabul qilish
2. GPT-4o Vision: Rasmni tahlil qilish va tavsif berish
3. Telegram'ga tafsifi jo'natish (matn)
```

## Tashqi Xizmatlar va Ularning Rollari

| Xizmat | Rol | Konfiguratsiya |
|--------|------|----------------|
| **Telegram (Telethon)** | Messenger va xabar qabul qilish | `API_ID`, `API_HASH` |
| **OpenAI (GPT-4o)** | AI savollariga javob berish | `OPENAI_KEY` |
| **UzbekVoice** | Uzbek tilida speech-to-text | `UZVOICE_KEY` |
| **Aisha** | Uzbek tilida text-to-speech | `AISHA_KEY` |

## Konfiguratsiya (.env)

Quyidagi muhit o'zgaruvchilarini o'rnatish zarur:

```
API_ID=<Telegram API ID>
API_HASH=<Telegram API Hash>
OPENAI_KEY=<OpenAI API kaliti>
UZVOICE_KEY=<UzbekVoice API kaliti>
AISHA_KEY=<Aisha API kaliti>
ADMIN_ID=<Admin Telegram User ID>
```

**Eslatma**: Hech qachon haqiqiy kalit qiymatlarini versionlash tizimiga commit qilmang.

## Xatolikni Hal Qilish va Bezavta

### Asosiy Xatoliklar
- **Rate Limit Xatosi**: Foydalanuvchi kunlik chegarasidan oshib ketgan bo'lsa, xabar iloji bor emasligini bildiradi
- **API Xatosi**: Tashqi xizmatga ulanish muammolari bo'lsa, foydalanuvchiga xato xabari jo'natiladi
- **Tilga Loyihy Xatosi**: STT yoki TTS xatosi bo'lsa, texnik muammo bo'lishi haqida xabar beriladi

### Log Fayllari
Barcha operatsiyalar `logs` katalogida yozib qo'yiladi. Xatolikni hal qilishda bu fayllarni ko'rib chiqing.

## Texnik Qidmatlari

Bu loyihada quyidagi asosiy texnologiyalar ishlatilinadi:

- **Python**: Bosh dasturlash tili
- **Telethon**: Telegram API uchun async client
- **OpenAI SDK**: GPT-4o bilan integratsiya
- **aiohttp**: Asinxron HTTP so'rovlar uchun (tashqi API bilan aloqa)

## Keyingi O'qish

Batafsil ma'lumot uchun quyidagi fayllarni o'qing:
- `main.py`: Asosiy dastur va handler
- `config.py`: Konfiguratsiya va muhit o'zgaruvchilari
- `utils.py`: Yordamchi funksiyalar
- `handlers.py`: Xabar qayta ishlash mantiq
