




import sqlite3
from pathlib import Path



DB_PATH = Path(__file__).parent / "database.db"

def get_db():
    """Возвращает подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализирует таблицы"""
    with get_db() as conn:
        conn.execute("""
                CREATE TABLE IF NOT EXISTS search_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    query TEXT NOT NULL,
                    genre_filter TEXT,
                    limit_results INTEGER DEFAULT 10,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
        conn.commit()
