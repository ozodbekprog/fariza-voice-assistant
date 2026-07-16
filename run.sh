#!/bin/bash
set -e

# Fariza Ovoz Assistent - Startup Script

echo "=========================================="
echo "Fariza Ovoz Assistent"
echo "=========================================="
echo ""

# Python3 mavjudligini tekshirish
echo "Python3 mavjudligini tekshiryapman..."
if ! command -v python3 &> /dev/null; then
    echo "XATO: Python3 topilmadi!"
    echo "Ilmoiy o'rnatishni amalga oshiring: apt-get install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ $PYTHON_VERSION topildi"
echo ""

# Virtual Environment yaratish yoki aktivizatsiya qilish
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual Environment yaratilmoqda..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual Environment yaratildi"
else
    echo "✓ Virtual Environment allaqachon mavjud"
fi
echo ""

# Virtual Environmentni aktivizatsiya qilish
echo "Virtual Environmentni aktivizatsiya qilmoqda..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual Environment aktivizatsiya qilindi"
echo ""

# Kerakli paketlarni o'rnatish
echo "Paketlarni o'rnatmoqda (requirements.txt)..."
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q
echo "✓ Paketlar o'rnatildi"
echo ""

# .env faylni tekshirish
if [ ! -f ".env" ]; then
    echo "XATO: .env fayli topilmadi!"
    echo ""
    echo "Yechim:"
    echo "  1. .env.example faylini .env ga ko'chiring:"
    echo "     cp .env.example .env"
    echo ""
    echo "  2. .env faylida barcha API kalitlarini to'ldiring:"
    echo "     - API_ID: https://my.telegram.org"
    echo "     - API_HASH: https://my.telegram.org"
    echo "     - OPENAI_KEY: https://platform.openai.com"
    echo "     - UZVOICE_KEY: https://uzvoice.com"
    echo "     - AISHA_KEY: Aisha xizmatidan"
    echo "     - ADMIN_ID: Botdan /getme buyrug'ini ishlatib oling"
    echo ""
    exit 1
fi
echo "✓ .env fayli topildi"
echo ""

# Asosiy skriptni ishga tushirish
echo "=========================================="
echo "Ilovani ishga tushiryapman..."
echo "=========================================="
echo ""
python main.py

