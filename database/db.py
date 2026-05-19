"""PostgreSQL ulanishi va jadval sxemasi."""
from __future__ import annotations

import asyncpg


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    tg_id        BIGINT PRIMARY KEY,
    full_name    TEXT NOT NULL,
    phone        TEXT NOT NULL,
    language     TEXT NOT NULL DEFAULT 'uz',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS requests (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    content      TEXT,                 -- xabardagi text yoki caption
    content_type TEXT NOT NULL,        -- text / photo / video / document / voice / audio / sticker / video_note / animation / location / contact
    answered     BOOLEAN NOT NULL DEFAULT FALSE,
    answered_by  BIGINT,               -- javob bergan admin tg_id
    answered_at  TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_messages (
    id           BIGSERIAL PRIMARY KEY,
    request_id   BIGINT NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    admin_id     BIGINT NOT NULL,
    chat_id      BIGINT NOT NULL,
    message_id   BIGINT NOT NULL,
    UNIQUE (request_id, admin_id)
);

CREATE TABLE IF NOT EXISTS answers (
    id           BIGSERIAL PRIMARY KEY,
    request_id   BIGINT NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    admin_id     BIGINT NOT NULL,
    content      TEXT,
    content_type TEXT NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_requests_user ON requests(user_id);
CREATE INDEX IF NOT EXISTS idx_requests_answered ON requests(answered);
CREATE INDEX IF NOT EXISTS idx_admin_messages_request ON admin_messages(request_id);
"""


class Database:
    """asyncpg connection pool ustidan ishlovchi wrapper."""

    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None

    async def connect(self, dsn: str) -> None:
        self._pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=10)
        async with self._pool.acquire() as conn:
            await conn.execute(CREATE_SQL)

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("Database hali ulanmagan")
        return self._pool


# Loyiha bo'ylab ishlatiladigan global namuna
db = Database()
