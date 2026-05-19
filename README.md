# Murojaat Bot

Telegram bot foydalanuvchilardan murojaat qabul qiladi va belgilangan adminlarga yetkazadi. `aiogram 3` (async) + PostgreSQL (`asyncpg`).

## Imkoniyatlar

- `/start` -> 3 ta til tanlash (O'zbek / Русский / English) -> ism -> telefon (`+998XXXXXXXXX`)
- Telefon tugma orqali yoki matn ko'rinishida; noto'g'ri formatda qayta so'raladi
- Ro'yxatdan o'tgan foydalanuvchining har qanday xabari (matn, foto, video, hujjat, ovoz, video-note, sticker, animation, joylashuv, kontakt) murojaat sifatida qabul qilinadi
- Murojaat barcha adminlarga yuboriladi, ostida ikkita tugma:
  - **Javob berish** — bosgan admin javobini yuboradi, boshqa adminlardagi tugma avtomatik o'chadi
  - **Raqamni ko'rish** — hech qachon o'chmaydi, bosilganda foydalanuvchi raqami chiqadi
- Admin javobi (har qanday turdagi xabar) foydalanuvchiga yuboriladi
- **Fayllar serverda saqlanmaydi**: bazaga faqat matn/caption va meta-ma'lumot yoziladi. Xabarlar `copy_message` orqali Telegram serverlari ichida nusxalanadi
- `/settings` — til, ism va telefonni o'zgartirish
- `/statistika` (adminlar uchun) — umumiy, javob berilgan va javob berilmagan murojaatlar soni

## O'rnatish

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Kutubxonalar
pip install -r requirements.txt

# 3. PostgreSQL bazasini yaratish
createdb murojatbot
# yoki psql ichida:
#   CREATE DATABASE murojatbot;

# 4. .env faylini sozlash
cp .env.example .env
# .env ni tahrirlang: BOT_TOKEN, ADMIN_IDS, DB_*

# 5. Ishga tushirish
python bot.py
```

Jadval sxemasi bot birinchi ishga tushganda avtomatik yaratiladi.

## `.env` o'zgaruvchilari

| O'zgaruvchi | Tavsif |
|---|---|
| `BOT_TOKEN` | @BotFather'dan olingan token |
| `ADMIN_IDS` | Adminlar Telegram ID, vergul bilan: `123,456` |
| `DB_HOST` | PostgreSQL host (default: `localhost`) |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | Baza nomi (default: `murojatbot`) |
| `DB_USER` | Foydalanuvchi |
| `DB_PASSWORD` | Parol |

> Telegram ID ni bilish uchun [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring.

## Loyiha tuzilmasi

```
murojatbot/
├── bot.py                  # Kirish nuqtasi
├── config.py               # .env o'qish
├── requirements.txt
├── .env.example
├── database/
│   ├── db.py               # asyncpg pool + jadval sxemasi
│   └── queries.py          # CRUD funksiyalar
├── handlers/
│   ├── start.py            # /start + ro'yxatdan o'tish FSM
│   ├── user.py             # foydalanuvchi xabarlari -> adminlar
│   ├── admin.py            # javob va raqam tugmalari
│   ├── settings.py         # /settings FSM
│   └── commands.py         # /statistika
├── keyboards/
│   ├── reply.py            # Reply tugmalar (til, telefon, settings)
│   └── inline.py           # Inline tugmalar (admin uchun)
├── locales/translations.py # uz / ru / en matnlar
├── states/states.py        # FSM holatlari
└── utils/helpers.py        # telefon validatsiyasi va h.k.
```

## Buyruqlar

| Buyruq | Kim uchun | Vazifa |
|---|---|---|
| `/start` | Hamma | Botni boshlash / qayta ishga tushirish |
| `/settings` | Foydalanuvchi | Til, ism, telefonni o'zgartirish |
| `/statistika` | Admin | Murojaatlar statistikasi |

## Eslatmalar

- Bot foydalanuvchidan kelgan har qanday xabarni murojaat deb hisoblaydi (faqat ro'yxatdan o'tgan bo'lsa). Maxsus tugma yoki "murojaat yuborish" rejimi yo'q — shartlarda shunday ko'rsatilgan.
- `copy_message` Telegram tomonidagi metodga ishonadi: bot tomonida `file_id` saqlanmaydi va serverga fayl yuklanmaydi.
- "Javob berilgan/berilmagan" tekshiruvi bazada atomik `UPDATE ... WHERE answered=FALSE RETURNING id` orqali bajariladi — ikki admin bir vaqtda javob bera olmaydi.
