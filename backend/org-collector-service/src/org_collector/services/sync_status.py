from database.connect import get_conn
from datetime import datetime

def update_sync_status(name: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO sync_status (name, last_synced)
            VALUES (%s, NOW())
            ON CONFLICT (name)
            DO UPDATE SET last_synced = NOW();
            """,
            (name,)
        )
    conn.commit()
    conn.close()

def get_sync_status(name: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT last_synced FROM sync_status WHERE name = %s", (name,))
        row = cur.fetchone()
    conn.close()
    return row[0] if row else None
