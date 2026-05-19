from aiogram import Router

from handlers import admin, commands, settings, start, user


def setup_routers() -> Router:
    """Barcha routerlarni birlashtirish.

    Tartib muhim: avval admin callbacklari va FSM holatlari, keyin
    settings/commands, eng oxirida user (catch-all) va start.
    """
    root = Router()
    root.include_router(start.router)
    root.include_router(settings.router)
    root.include_router(commands.router)
    root.include_router(admin.router)
    root.include_router(user.router)
    return root
