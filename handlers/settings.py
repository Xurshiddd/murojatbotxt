"""/settings - til, ism, telefonni o'zgartirish."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import queries
from keyboards.reply import language_kb, phone_kb, remove_kb, settings_menu_kb
from locales.translations import LANG_NAMES, t
from states.states import Settings
from utils.helpers import is_valid_phone, normalize_phone

router = Router()

_NAME_TO_CODE = {v: k for k, v in LANG_NAMES.items()}


@router.message(Command("settings", "sozlamalar"))
async def cmd_settings(message: Message, state: FSMContext) -> None:
    user = await queries.get_user(message.from_user.id)
    if not user:
        await message.answer(t("not_registered", "uz"))
        return

    lang = user["language"]
    await state.set_state(Settings.menu)
    await message.answer(t("settings_title", lang), reply_markup=settings_menu_kb(lang))


# ---------- Menu tanlovlari ----------

@router.message(Settings.menu, F.text)
async def settings_menu_choice(message: Message, state: FSMContext) -> None:
    user = await queries.get_user(message.from_user.id)
    if not user:
        await state.clear()
        return
    lang = user["language"]
    text = (message.text or "").strip()

    if text == t("settings_language", lang):
        await state.set_state(Settings.waiting_language)
        await message.answer(t("choose_language", lang), reply_markup=language_kb())
        return

    if text == t("settings_name", lang):
        await state.set_state(Settings.waiting_name)
        await message.answer(t("ask_name", lang), reply_markup=remove_kb())
        return

    if text == t("settings_phone", lang):
        await state.set_state(Settings.waiting_phone)
        await message.answer(t("ask_phone", lang), reply_markup=phone_kb(lang))
        return

    if text == t("settings_cancel", lang):
        await state.clear()
        await message.answer(t("cancelled", lang), reply_markup=remove_kb())
        return

    # Tushunilmagan tanlov - menyuni qayta ko'rsatish
    await message.answer(t("settings_title", lang), reply_markup=settings_menu_kb(lang))


# ---------- Til yangilash ----------

@router.message(Settings.waiting_language, F.text)
async def settings_set_language(message: Message, state: FSMContext) -> None:
    code = _NAME_TO_CODE.get(message.text or "")
    if not code:
        await message.answer(t("choose_language", "uz"), reply_markup=language_kb())
        return

    await queries.update_user_field(message.from_user.id, "language", code)
    await state.clear()
    await message.answer(t("language_saved", code), reply_markup=remove_kb())
    await message.answer(t("welcome", code))


# ---------- Ism yangilash ----------

@router.message(Settings.waiting_name, F.text)
async def settings_set_name(message: Message, state: FSMContext) -> None:
    user = await queries.get_user(message.from_user.id)
    lang = (user or {}).get("language", "uz")
    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(t("name_too_short", lang))
        return

    await queries.update_user_field(message.from_user.id, "full_name", name)
    await state.clear()
    await message.answer(t("name_updated", lang), reply_markup=remove_kb())


# ---------- Telefon yangilash ----------

@router.message(Settings.waiting_phone, F.contact)
async def settings_set_phone_contact(message: Message, state: FSMContext) -> None:
    user = await queries.get_user(message.from_user.id)
    lang = (user or {}).get("language", "uz")
    contact = message.contact

    if contact.user_id and contact.user_id != message.from_user.id:
        await message.answer(t("phone_invalid", lang))
        return

    phone = normalize_phone(contact.phone_number)
    if not is_valid_phone(phone):
        await message.answer(t("phone_invalid", lang), reply_markup=phone_kb(lang))
        return

    await queries.update_user_field(message.from_user.id, "phone", phone)
    await state.clear()
    await message.answer(t("phone_updated", lang), reply_markup=remove_kb())


@router.message(Settings.waiting_phone, F.text)
async def settings_set_phone_text(message: Message, state: FSMContext) -> None:
    user = await queries.get_user(message.from_user.id)
    lang = (user or {}).get("language", "uz")
    phone = normalize_phone(message.text or "")
    if not is_valid_phone(phone):
        await message.answer(t("phone_invalid", lang), reply_markup=phone_kb(lang))
        return

    await queries.update_user_field(message.from_user.id, "phone", phone)
    await state.clear()
    await message.answer(t("phone_updated", lang), reply_markup=remove_kb())
