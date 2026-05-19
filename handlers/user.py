"""Foydalanuvchi murojaatlarini qabul qilish va adminlarga yuborish."""
from __future__ import annotations

import logging

from aiogram import Bot, Router
from aiogram.types import Message

from config import Config
from database import queries
from keyboards.inline import admin_request_kb
from locales.translations import t
from utils.helpers import message_content_pair

router = Router()
log = logging.getLogger(__name__)


@router.message()
async def handle_user_message(message: Message, bot: Bot, config: Config) -> None:
    """Catch-all: ro'yxatdan o'tgan foydalanuvchining har qanday xabarini
    murojaat sifatida qabul qilib, adminlarga yuboradi.

    Server'da hech qanday fayl saqlanmaydi - faqat text/caption bazaga
    yoziladi. Adminlarga xabar bot.copy_message orqali yuboriladi, fayl
    bot serverida qoldirilmaydi.
    """
    if message.from_user is None or message.from_user.is_bot:
        return

    # Adminning shaxsiy chatdagi xabarlari murojaat emas
    if message.from_user.id in config.admin_ids:
        return

    user = await queries.get_user(message.from_user.id)
    if not user:
        await message.answer(t("not_registered", "uz"))
        return

    lang = user["language"]
    content, content_type = message_content_pair(message)

    request_id = await queries.create_request(
        user_id=message.from_user.id,
        content=content,
        content_type=content_type,
    )

    header = t("new_request_header", "uz", name=user["full_name"], rid=request_id)

    # Adminlarga yuborish
    sent_any = False
    for admin_id in config.admin_ids:
        try:
            await bot.send_message(admin_id, header)
            copied = await bot.copy_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=admin_request_kb(request_id, lang="uz", show_answer=True),
            )
            await queries.save_admin_message(
                request_id=request_id,
                admin_id=admin_id,
                chat_id=admin_id,
                message_id=copied.message_id,
            )
            sent_any = True
        except Exception as exc:  # pragma: no cover - log only
            log.warning("Adminga (%s) yuborib bo'lmadi: %s", admin_id, exc)

    if sent_any:
        await message.answer(t("request_sent", lang))
    else:
        # Adminlar ro'yxati bo'sh yoki barcha yuborishlar muvaffaqiyatsiz
        await message.answer(t("request_sent", lang))
