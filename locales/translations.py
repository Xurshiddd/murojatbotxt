"""Uchta til uchun matnlar: uz, ru, en."""
from __future__ import annotations

LANGUAGES = ("uz", "ru", "en")

LANG_NAMES: dict[str, str] = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

_TEXTS: dict[str, dict[str, str]] = {
    # ---------- Til tanlash ----------
    "choose_language": {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
        "en": "Choose your language:",
    },
    "language_saved": {
        "uz": "✅ Til saqlandi.",
        "ru": "✅ Язык сохранён.",
        "en": "✅ Language saved.",
    },

    # ---------- Ism ----------
    "ask_name": {
        "uz": "Ismingizni kiriting:",
        "ru": "Введите ваше имя:",
        "en": "Please enter your name:",
    },
    "name_too_short": {
        "uz": "❗️ Ism juda qisqa. Iltimos, to'liq ismingizni kiriting.",
        "ru": "❗️ Имя слишком короткое. Пожалуйста, введите полное имя.",
        "en": "❗️ Name is too short. Please enter your full name.",
    },

    # ---------- Telefon ----------
    "ask_phone": {
        "uz": "📞 Telefon raqamingizni yuboring.\n\nQuyidagi tugma orqali yuborishingiz yoki +998XXXXXXXXX ko'rinishida yozishingiz mumkin.",
        "ru": "📞 Отправьте ваш номер телефона.\n\nМожно через кнопку ниже или в формате +998XXXXXXXXX.",
        "en": "📞 Please send your phone number.\n\nUse the button below or type it in the format +998XXXXXXXXX.",
    },
    "share_phone_btn": {
        "uz": "📱 Raqamni yuborish",
        "ru": "📱 Отправить номер",
        "en": "📱 Share phone number",
    },
    "phone_invalid": {
        "uz": "❗️ Telefon raqam noto'g'ri. To'g'ri format: +998XXXXXXXXX",
        "ru": "❗️ Неверный формат номера. Правильный формат: +998XXXXXXXXX",
        "en": "❗️ Invalid phone number. Correct format: +998XXXXXXXXX",
    },

    # ---------- Asosiy ----------
    "welcome": {
        "uz": "Assalomu alaykum! Sizga qanday yordam bera olishimiz mumkin?\nMurojaatingiz bo'lsa marhamat, sizga yordam berishdan mamnunmiz 😊",
        "ru": "Здравствуйте! Чем мы можем вам помочь?\nЕсли у вас есть обращение — пожалуйста, напишите, мы рады помочь 😊",
        "en": "Hello! How can we help you?\nIf you have an inquiry, please send it — we are glad to help 😊",
    },
    "request_sent": {
        "uz": "✅ Murojaatingiz qabul qilindi. Tez orada javob beriladi.",
        "ru": "✅ Ваше обращение принято. Скоро мы ответим.",
        "en": "✅ Your request has been received. We will reply soon.",
    },
    "answer_received": {
        "uz": "📬 Sizning murojaatingizga javob keldi:",
        "ru": "📬 Получен ответ на ваше обращение:",
        "en": "📬 You have a reply to your request:",
    },

    # ---------- Settings ----------
    "settings_title": {
        "uz": "⚙️ Sozlamalar. Nimani o'zgartirmoqchisiz?",
        "ru": "⚙️ Настройки. Что хотите изменить?",
        "en": "⚙️ Settings. What would you like to change?",
    },
    "settings_language": {
        "uz": "🌐 Til",
        "ru": "🌐 Язык",
        "en": "🌐 Language",
    },
    "settings_name": {
        "uz": "👤 Ism",
        "ru": "👤 Имя",
        "en": "👤 Name",
    },
    "settings_phone": {
        "uz": "📞 Telefon",
        "ru": "📞 Телефон",
        "en": "📞 Phone",
    },
    "settings_cancel": {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
        "en": "❌ Cancel",
    },
    "cancelled": {
        "uz": "Bekor qilindi.",
        "ru": "Отменено.",
        "en": "Cancelled.",
    },
    "name_updated": {
        "uz": "✅ Ism yangilandi.",
        "ru": "✅ Имя обновлено.",
        "en": "✅ Name updated.",
    },
    "phone_updated": {
        "uz": "✅ Telefon yangilandi.",
        "ru": "✅ Телефон обновлён.",
        "en": "✅ Phone updated.",
    },

    # ---------- Admin ----------
    "new_request_header": {
        "uz": "📩 Yangi murojaat\n👤 Yuboruvchi: {name}\n🆔 #{rid}",
        "ru": "📩 Новое обращение\n👤 Отправитель: {name}\n🆔 #{rid}",
        "en": "📩 New request\n👤 From: {name}\n🆔 #{rid}",
    },
    "btn_answer": {
        "uz": "✍️ Javob berish",
        "ru": "✍️ Ответить",
        "en": "✍️ Reply",
    },
    "btn_show_phone": {
        "uz": "📞 Raqamni ko'rish",
        "ru": "📞 Показать номер",
        "en": "📞 Show phone",
    },
    "answered_by_other": {
        "uz": "⚠️ Bu murojaatga boshqa admin allaqachon javob bergan.",
        "ru": "⚠️ На это обращение уже ответил другой админ.",
        "en": "⚠️ This request has already been answered by another admin.",
    },
    "send_answer_prompt": {
        "uz": "✍️ #{rid} murojaatga javobingizni yuboring (matn, foto, video, hujjat va h.k.):",
        "ru": "✍️ Отправьте ваш ответ на обращение #{rid} (текст, фото, видео, документ и т.д.):",
        "en": "✍️ Send your reply to request #{rid} (text, photo, video, document, etc.):",
    },
    "answer_sent": {
        "uz": "✅ Javob foydalanuvchiga yuborildi.",
        "ru": "✅ Ответ отправлен пользователю.",
        "en": "✅ Reply sent to the user.",
    },
    "phone_label": {
        "uz": "📞 Foydalanuvchi raqami: {phone}",
        "ru": "📞 Номер пользователя: {phone}",
        "en": "📞 User phone: {phone}",
    },

    # ---------- Statistika ----------
    "stats_text": {
        "uz": "📊 Statistika\n\nJami murojaatlar: {total}\n✅ Javob berilgan: {answered}\n⏳ Javob berilmagan: {pending}",
        "ru": "📊 Статистика\n\nВсего обращений: {total}\n✅ Отвечено: {answered}\n⏳ Без ответа: {pending}",
        "en": "📊 Statistics\n\nTotal requests: {total}\n✅ Answered: {answered}\n⏳ Pending: {pending}",
    },
    "not_registered": {
        "uz": "Iltimos, /start buyrug'i orqali ro'yxatdan o'ting.",
        "ru": "Пожалуйста, зарегистрируйтесь через команду /start.",
        "en": "Please register first using /start.",
    },
    "not_admin": {
        "uz": "Bu buyruq faqat adminlar uchun.",
        "ru": "Эта команда только для администраторов.",
        "en": "This command is only for admins.",
    },
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Tarjima olish. Agar til topilmasa, uzbekcha qaytariladi."""
    if lang not in LANGUAGES:
        lang = "uz"
    template = _TEXTS.get(key, {}).get(lang) or _TEXTS.get(key, {}).get("uz") or key
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template
