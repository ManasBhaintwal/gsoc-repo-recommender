# services/user_db_ops.py
from backend.database.connect import get_conn
from psycopg.rows import dict_row
import bcrypt  # or use passlib if preferred
import json

# NOTE: use bcrypt.hashpw/ checkpw (bcrypt library) OR use passlib for convenience.
# Example below uses bcrypt (sync).

def create_user(username: str, email: str, password: str, github_username: str = None,
                languages: list = None, experience_level: str = None, interests: list = None):
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    languages_arr = languages or []
    interests_arr = interests or []

    conn = get_conn()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO users
                (username, email, password_hash, github_username, languages, experience_level, interests)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, username, email, github_username, languages, experience_level, interests, created_at;
                """,
                (username, email, pw_hash, github_username, languages_arr, experience_level, interests_arr)
            )
            user = cur.fetchone()
            conn.commit()
            return user
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_conn()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, username, email, github_username, languages, experience_level, interests, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def get_user_by_username(username: str):
    conn = get_conn()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, username, email, password_hash FROM users WHERE username = %s",
                (username,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def update_user(user_id: int, **fields):
    # fields may include: email, github_username, languages (list), experience_level, interests (list)
    allowed = {"email", "github_username", "languages", "experience_level", "interests"}
    set_parts = []
    values = []
    for k, v in fields.items():
        if k in allowed:
            set_parts.append(f"{k} = %s")
            values.append(v)
    if not set_parts:
        return None
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(set_parts)}, updated_at = NOW() WHERE id = %s RETURNING id, username, email, github_username, languages, experience_level, interests, updated_at"
    conn = get_conn()
    try:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, tuple(values))
            user = cur.fetchone()
            conn.commit()
            return user
    finally:
        conn.close()
