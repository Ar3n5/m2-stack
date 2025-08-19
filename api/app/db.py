import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname=os.environ.get("DB_NAME", "m2db"),
    )

def init_db():
    conn = get_conn()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS current_name (
                id INT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        cur.execute("INSERT INTO current_name (id, name) VALUES (1, %s) ON CONFLICT (id) DO NOTHING", ("Your Name",))
    conn.close()

def get_name():
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT name FROM current_name WHERE id = 1")
        row = cur.fetchone()
    conn.close()
    return row["name"] if row else "Unknown"

def set_name(new_name: str):
    conn = get_conn()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO current_name (id, name) VALUES (1, %s)
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
        """, (new_name,))
    conn.close()
