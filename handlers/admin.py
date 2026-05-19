"""Admin tomonidan murojaatga javob berish va telefon raqamni ko'rish."""
from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import Config
from database import queries
from keyboards.inline import admin_request_kb
from locales.translations import t
from states.states import AdminAnswer
from utils.helpers import message_content_pair

router = Router()
log = logging.getLogger(__name__)


def _admin_only(callback: CallbackQuery, config: Config) -> bool:
    return callback.from_user.id in config.admin_ids


# ---------- "Javob berish" tugmasi ----------

@router.callback_query(F.data.startswith("ans:"))
async def cb_answer(callback: CallbackQuery, state: FSMContext, config: Config) -> None:
    if not _admin_only(callback, config):
        await callback.answer(t("not_admin", "uz"), show_alert=True)
        return

    try:
        request_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer()
        return

    req = await queries.get_request(request_id)
    if not req:
        await callback.answer()
        return

    if req["answered"]:
        await callback.answer(t("answered_by_other", "uz"), show_alert=True)
        # Bu admin'dagi tugmani ham yangilab qo'yamiz
        try:
            await callback.message.edit_reply_markup(
                reply_markup=admin_request_kb(request_id, show_answer=False)
            )
        except TelegramBadRequest:
            pass
        return

    await state.set_state(AdminAnswer.waiting_answer)
    await state.update_data(request_id=request_id)
    await callback.message.answer(t("send_answer_prompt", "uz", rid=request_id))
    await callback.answer()


# ---------- "Raqamni ko'rish" tugmasi (hech qachon o'chmaydi) ----------

@router.callback_query(F.data.startswith("phone:"))
async def cb_show_phone(callback: CallbackQuery, config: Config) -> None:
    if not _admin_only(callback, config):
        await callback.answer(t("not_admin", "uz"), show_alert=True)
        return

    try:
        request_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer()
        return

    req = await queries.get_request(request_id)
    if not req:
        await callback.answer()
        return

    phone = await queries.get_phone(req["user_id"])
    if not phone:
        await callback.answer("—", show_alert=True)
        return

    await callback.answer(phone, show_alert=True)
    await callback.message.answer(t("phone_label", "uz", phone=phone))


# ---------- Admin javob xabarini qabul qilish ----------

@router.message(AdminAnswer.waiting_answer)
async def admin_send_answer(message: Message, state: FSMContext, bot: Bot, config: Config) -> None:
    if message.from_user.id not in config.admin_ids:
        return

    data = await state.get_data()
    request_id = data.get("request_id")
    if not request_id:
        await state.clear()
        return

    req = await queries.get_request(int(request_id))
    if not req:
        await state.clear()
        return

    # Atomik: faqat hali javob berilmagan bo'lsa belgilash
    claimed = await queries.mark_request_answered(int(request_id), message.from_user.id)
    if not claimed:
        await message.answer(t("answered_by_other", "uz"))
        await state.clear()
        return

    # Boshqa adminlardagi "Javob berish" tugmasini olib tashlash
    admin_msgs = await queries.get_admin_messages(int(request_id))
    for am in admin_msgs:
        try:
            await bot.edit_message_reply_markup(
                chat_id=am["chat_id"],
                message_id=am["message_id"],
                reply_markup=admin_request_kb(int(request_id), show_answer=False),
            )
        except TelegramBadRequest:
            pass
        except Exception as exc:
            log.warning("edit_reply_markup error: %s", exc)

    # Foydalanuvchining tilini olib, sarlavha yuboramiz
    user = await queries.get_user(req["user_id"])
    user_lang = (user or {}).get("language", "uz")

    try:
        await bot.send_message(req["user_id"], t("answer_received", user_lang))
        await bot.copy_message(
            chat_id=req["user_id"],
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
    except Exception as exc:
        log.warning("Javobni yuborib bo'lmadi: %s", exc)

    # Bazaga javob matnini (agar bor bo'lsa) yozish - fayl saqlanmaydi
    content, content_type = message_content_pair(message)
    await queries.save_answer(
        request_id=int(request_id),
        admin_id=message.from_user.id,
        content=content,
        content_type=content_type,
    )

    await message.answer(t("answer_sent", "uz"))
    await state.clear()
