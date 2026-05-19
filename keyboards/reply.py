"""Reply klaviaturalar."""
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from locales.translations import LANG_NAMES, t


def language_kb() -> ReplyKeyboardMarkup:
    """Til tanlash - uz/ru/en tugmalari."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=LANG_NAMES["uz"])],
            [KeyboardButton(text=LANG_NAMES["ru"])],
            [KeyboardButton(text=LANG_NAMES["en"])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("share_phone_btn", lang), request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def settings_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("settings_language", lang))],
            [KeyboardButton(text=t("settings_name", lang))],
            [KeyboardButton(text=t("settings_phone", lang))],
            [KeyboardButton(text=t("settings_cancel", lang))],
        ],
        resize_keyboard=True,
    )


def remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
