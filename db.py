import aiosqlite
from datetime import datetime

DB_NAME = "Krim.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            amount REAL,
            description TEXT,
            timestamp TEXT
        )''')
        await db.commit()

async def add_transaction(user_id, t_type, amount, description):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO transactions (user_id, type, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_id, t_type, amount, description, time_now)
        )
        await db.commit()
    return time_now

async def get_report(user_id, t_type):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, amount, description, timestamp FROM transactions WHERE user_id = ? AND type = ?",
            (user_id, t_type)
        )
        return await cursor.fetchall()

async def delete_transaction(item_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM transactions WHERE id = ?", (item_id,))
        await db.commit()

async def clear_user_history(user_id, t_type):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM transactions WHERE user_id = ? AND type = ?", (user_id, t_type))
        await db.commit()