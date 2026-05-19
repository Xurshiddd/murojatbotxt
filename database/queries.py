"""Bazadagi CRUD operatsiyalari."""
from __future__ import annotations

from typing import Any

from database.db import db


# ---------- USERS ----------

async def get_user(tg_id: int) -> dict[str, Any] | None:
    row = await db.pool.fetchrow(
        "SELECT tg_id, full_name, phone, language FROM users WHERE tg_id = $1",
        tg_id,
    )
    return dict(row) if row else None


async def upsert_user(tg_id: int, full_name: str, phone: str, language: str) -> None:
    await db.pool.execute(
        """
        INSERT INTO users (tg_id, full_name, phone, language)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (tg_id) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            phone     = EXCLUDED.phone,
            language  = EXCLUDED.language
        """,
        tg_id, full_name, phone, language,
    )


async def update_user_field(tg_id: int, field: str, value: str) -> None:
    if field not in {"full_name", "phone", "language"}:
        raise ValueError(f"Yaroqsiz field: {field}")
    await db.pool.execute(
        f"UPDATE users SET {field} = $1 WHERE tg_id = $2",
        value, tg_id,
    )


async def get_phone(tg_id: int) -> str | None:
    row = await db.pool.fetchrow("SELECT phone FROM users WHERE tg_id = $1", tg_id)
    return row["phone"] if row else None


# ---------- REQUESTS ----------

async def create_request(user_id: int, content: str | None, content_type: str) -> int:
    row = await db.pool.fetchrow(
        """
        INSERT INTO requests (user_id, content, content_type)
        VALUES ($1, $2, $3)
        RETURNING id
        """,
        user_id, content, content_type,
    )
    return int(row["id"])


async def get_request(request_id: int) -> dict[str, Any] | None:
    row = await db.pool.fetchrow(
        "SELECT * FROM requests WHERE id = $1",
        request_id,
    )
    return dict(row) if row else None


async def mark_request_answered(request_id: int, admin_id: int) -> bool:
    """Atomik: faqat answered=FALSE bo'lsa belgilanadi. True qaytarsa - shu admin
    birinchi bo'lib javob bermoqda; False bo'lsa boshqa admin allaqachon bergan."""
    row = await db.pool.fetchrow(
        """
        UPDATE requests
           SET answered = TRUE,
               answered_by = $2,
               answered_at = NOW()
         WHERE id = $1 AND answered = FALSE
         RETURNING id
        """,
        request_id, admin_id,
    )
    return row is not None


# ---------- ADMIN MESSAGES (qaysi adminga qaysi xabarda yuborilganini saqlash) ----------

async def save_admin_message(request_id: int, admin_id: int, chat_id: int, message_id: int) -> None:
    await db.pool.execute(
        """
        INSERT INTO admin_messages (request_id, admin_id, chat_id, message_id)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (request_id, admin_id) DO UPDATE SET
            chat_id = EXCLUDED.chat_id,
            message_id = EXCLUDED.message_id
        """,
        request_id, admin_id, chat_id, message_id,
    )


async def get_admin_messages(request_id: int) -> list[dict[str, Any]]:
    rows = await db.pool.fetch(
        "SELECT admin_id, chat_id, message_id FROM admin_messages WHERE request_id = $1",
        request_id,
    )
    return [dict(r) for r in rows]


# ---------- ANSWERS ----------

async def save_answer(request_id: int, admin_id: int, content: str | None, content_type: str) -> None:
    await db.pool.execute(
        """
        INSERT INTO answers (request_id, admin_id, content, content_type)
        VALUES ($1, $2, $3, $4)
        """,
        request_id, admin_id, content, content_type,
    )


# ---------- STATISTIKA ----------

async def get_statistics() -> dict[str, int]:
    row = await db.pool.fetchrow(
        """
        SELECT
            COUNT(*)                                       AS total,
            COUNT(*) FILTER (WHERE answered = TRUE)        AS answered,
            COUNT(*) FILTER (WHERE answered = FALSE)       AS pending
        FROM requests
        """
    )
    return {
        "total": int(row["total"]),
        "answered": int(row["answered"]),
        "pending": int(row["pending"]),
    }
