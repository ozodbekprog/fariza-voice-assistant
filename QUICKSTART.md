# Fariza Ovoz Assistent - Tez Boshlash

## Talab qilgan narsalar
- Python 3.8+
- pip
- bash

## Boshlash bo'yicha qadamlar

### 1. Paketni klonlash
```bash
git clone <repository-url>
cd fariza-voice-assistant
```

### 2. .env konfiguratsiyasini yaratish
```bash
cp .env.example .env
```

### 3. API kalitlarini qo'shish
`.env` faylini matn muharriri bilan oching va quyidagi qiymatlarni to'ldiring:

- **API_ID** — https://my.telegram.org saytidan oling
- **API_HASH** — https://my.telegram.org saytidan oling
- **OPENAI_KEY** — https://platform.openai.com saytidan oling
- **UZVOICE_KEY** — https://uzvoice.com saytidan oling
- **AISHA_KEY** — Aisha xizmatidan oling
- **ADMIN_ID** — Botdan `/getme` buyrug'ini ishlatib oling
- **STORAGE_DIR** — saqlash uchun direktoriysining yo'li (standart: `./storage`)

### 4. Skriptni ishga tushirish
```bash
chmod +x run.sh
./run.sh
```

Bu script quyidagilarni bajaradi:
- Python3 mavjudligini tekshiradi
- Virtual Environment yaratadi (agar mavjud bo'lmasa)
- Barcha kerakli paketlarni o'rnatadi
- .env konfiguratsiyasini tekshiradi
- Asosiy ilovani ishga tushiradi

## Muammolarni hal qilish

**Xato: "Python3 topilmadi"**
```bash
# Ubuntu/Debian:
sudo apt-get install python3 python3-venv

# macOS:
brew install python3
```

**Xato: ".env fayli topilmadi"**
- `.env` faylini yarating va API kalitlarini to'ldiring (yuqorida qarang)

**Xato: "Permission denied"**
```bash
chmod +x run.sh
```

## Qo'shimcha maqolalar
- [Telethon dokumentatsiyasi](https://docs.telethon.dev/)
- [OpenAI dokumentatsiyasi](https://platform.openai.com/docs)
- [Python dotenv](https://github.com/theskumar/python-dotenv)

