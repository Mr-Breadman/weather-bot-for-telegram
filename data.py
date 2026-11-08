import sqlite3
DB_NAME = "weather_bot.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                notify_time TEXT NOT NULL
            )
        """)
        conn.commit()

def add_user(user_id, city, notify_time):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, city, notify_time)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                city = excluded.city,
                notify_time = excluded.notify_time
        """, (user_id, city, notify_time))
        conn.commit()


def get_all_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, city, notify_time FROM users")
        return cursor.fetchall()


def get_users_by_time(time_str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, city FROM users WHERE notify_time = ?", (time_str,))
        return cursor.fetchall()


def remove_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
