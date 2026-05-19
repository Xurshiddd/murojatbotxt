"""Inline klaviaturalar (adminlar uchun)."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from locales.translations import t


def admin_request_kb(request_id: int, lang: str = "uz", show_answer: bool = True) -> InlineKeyboardMarkup:
    """Admin ko'radigan murojaat ostidagi tugmalar.

    show_answer=False bo'lsa, faqat 'Raqamni ko'rish' tugmasi qoldiriladi
    (boshqa admin javob bergach, javob tugmasi olib tashlanadi).
    """
    rows: list[list[InlineKeyboardButton]] = []
    if show_answer:
        rows.append([
            InlineKeyboardButton(
                text=t("btn_answer", lang),
                callback_data=f"ans:{request_id}",
            ),
        ])
    rows.append([
        InlineKeyboardButton(
            text=t("btn_show_phone", lang),
            callback_data=f"phone:{request_id}",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)
