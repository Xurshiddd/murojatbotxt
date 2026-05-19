"""Yordamchi funksiyalar."""
from __future__ import annotations

import re

from aiogram.types import Message


_PHONE_RE = re.compile(r"^\+998\d{9}$")


def normalize_phone(raw: str) -> str:
    """Telefon raqamni standart +998XXXXXXXXX formatga keltirish.

    Qabul qilinadi: '+998901234567', '998901234567', '901234567',
    '+998 90 123 45 67', '8(90)123-45-67' va h.k. - faqat raqamlar olinadi.
    """
    digits = re.sub(r"\D", "", raw or "")
    if not digits:
        return ""
    # 998 bilan boshlangan 12 ta raqam
    if digits.startswith("998") and len(digits) == 12:
        return "+" + digits
    # 9 ta raqam - kod tushib qolgan
    if len(digits) == 9:
        return "+998" + digits
    # Qolgan barcha holatlar - validatsiyada tushiriladi
    return "+" + digits


def is_valid_phone(phone: str) -> bool:
    """+998 va keyin 9 ta raqam."""
    return bool(_PHONE_RE.match(phone or ""))


def message_content_pair(message: Message) -> tuple[str | None, str]:
    """Xabardan (matn/caption, content_type) juftligini qaytaradi.

    Server'da fayl saqlanmaydi: faqat matn va caption bazaga yoziladi.
    Boshqa adminlarga yuborish copy_message orqali amalga oshiriladi,
    shunda hech qanday fayl bot tomonida saqlanmaydi.
    """
    if message.text is not None:
        return message.text, "text"
    caption = message.caption
    if message.photo:
        return caption, "photo"
    if message.video:
        return caption, "video"
    if message.document:
        return caption, "document"
    if message.voice:
        return caption, "voice"
    if message.audio:
        return caption, "audio"
    if message.video_note:
        return None, "video_note"
    if message.animation:
        return caption, "animation"
    if message.sticker:
        return None, "sticker"
    if message.location:
        return None, "location"
    if message.contact:
        return None, "contact"
    return caption, "other"
