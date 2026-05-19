"""/start va ro'yxatdan o'tish (til -> ism -> telefon)."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import queries
from keyboards.reply import language_kb, phone_kb, remove_kb
from locales.translations import LANG_NAMES, t
from states.states import Register
from utils.helpers import is_valid_phone, normalize_phone

router = Router()


# Display nomdan til kodini topish
_NAME_TO_CODE = {v: k for k, v in LANG_NAMES.items()}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    user = await queries.get_user(message.from_user.id)
    if user:
        # Allaqachon ro'yxatdan o'tgan - to'g'ridan welcome
        await message.answer(t("welcome", user["language"]), reply_markup=remove_kb())
        return

    await message.answer(
        t("choose_language", "uz"),
        reply_markup=language_kb(),
    )
    await state.set_state(Register.language)


@router.message(Register.language, F.text)
async def reg_language(message: Message, state: FSMContext) -> None:
    code = _NAME_TO_CODE.get(message.text or "")
    if not code:
        await message.answer(t("choose_language", "uz"), reply_markup=language_kb())
        return

    await state.update_data(language=code)
    await message.answer(t("language_saved", code), reply_markup=remove_kb())
    await message.answer(t("ask_name", code))
    await state.set_state(Register.name)


@router.message(Register.name, F.text)
async def reg_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")

    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(t("name_too_short", lang))
        return

    await state.update_data(full_name=name)
    await message.answer(t("ask_phone", lang), reply_markup=phone_kb(lang))
    await state.set_state(Register.phone)


@router.message(Register.phone, F.contact)
async def reg_phone_contact(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")

    # Faqat o'z kontaktini yuborgan bo'lsa qabul qilamiz
    contact = message.contact
    if contact.user_id and contact.user_id != message.from_user.id:
        await message.answer(t("phone_invalid", lang))
        return

    phone = normalize_phone(contact.phone_number)
    if not is_valid_phone(phone):
        await message.answer(t("phone_invalid", lang), reply_markup=phone_kb(lang))
        return

    await _finish_registration(message, state, lang, phone)


@router.message(Register.phone, F.text)
async def reg_phone_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")

    phone = normalize_phone(message.text or "")
    if not is_valid_phone(phone):
        await message.answer(t("phone_invalid", lang), reply_markup=phone_kb(lang))
        return

    await _finish_registration(message, state, lang, phone)


async def _finish_registration(message: Message, state: FSMContext, lang: str, phone: str) -> None:
    data = await state.get_data()
    full_name = data.get("full_name", message.from_user.full_name or "Foydalanuvchi")

    await queries.upsert_user(
        tg_id=message.from_user.id,
        full_name=full_name,
        phone=phone,
        language=lang,
    )
    await state.clear()
    await message.answer(t("welcome", lang), reply_markup=remove_kb())
