"""Murojaat bot - asosiy fayl. python bot.py orqali ishga tushiriladi."""
from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeChat

from config import Config, load_config
from database.db import db
from handlers import setup_routers


async def _set_commands(bot: Bot, config: Config) -> None:
    # Foydalanuvchilar uchun
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni qayta ishga tushirish"),
        BotCommand(command="settings", description="Sozlamalar (til, ism, telefon)"),
    ])
    # Adminlar uchun (qo'shimcha /statistika)
    for admin_id in config.admin_ids:
        try:
            await bot.set_my_commands(
                [
                    BotCommand(command="start", description="Botni qayta ishga tushirish"),
                    BotCommand(command="settings", description="Sozlamalar"),
                    BotCommand(command="statistika", description="Murojaatlar statistikasi"),
                ],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except Exception:
            pass


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = load_config()
    await db.connect(config.dsn)

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Handlerlarga config'ni yetkazib berish
    dp["config"] = config

    dp.include_router(setup_routers())

    await _set_commands(bot, config)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
