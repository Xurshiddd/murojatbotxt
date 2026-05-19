"""Adminlar uchun /statistika buyrug'i."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import Config
from database import queries
from locales.translations import t

router = Router()


@router.message(Command("statistika", "statistics", "stats"))
async def cmd_statistics(message: Message, config: Config) -> None:
    if message.from_user.id not in config.admin_ids:
        await message.answer(t("not_admin", "uz"))
        return

    stats = await queries.get_statistics()
    await message.answer(t("stats_text", "uz", **stats))
