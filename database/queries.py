
import sqlite3
from pathlib import Path



DB_PATH = Path(__file__).parent / "database.db"

def get_db():
    """Возвращает подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализирует таблицы с новыми полями"""
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS search_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            query TEXT,
            genre_filter TEXT,
            limit_results INTEGER DEFAULT 10,
            budget TEXT,
            page INTEGER DEFAULT 1,
            rating REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id)  -- Гарантируем одну запись на пользователя
        )
        """)
        conn.commit()

init_db()


def save_search_request(
        user_id: int,
        query: str = None,
        genre: str = None,
        quantity: int = None,
        budget: str = None,
        page: int = None,
        rating: float = None
) -> None:
    """
    Сохраняет или обновляет данные поиска для пользователя.
    Поле query теперь необязательное.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Проверяем существование записи
        cursor.execute("SELECT 1 FROM search_requests WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()

        if exists:
            # Формируем динамический запрос для обновления
            updates = []
            params = []

            if query is not None:
                updates.append("query = ?")
                params.append(query)
            if genre is not None:
                updates.append("genre_filter = ?")
                params.append(genre)
            if quantity is not None:
                updates.append("limit_results = ?")
                params.append(quantity)
            if budget is not None:
                updates.append("budget = ?")
                params.append(budget)
            if page is not None:
                updates.append("page = ?")
                params.append(page)
            if rating is not None:
                updates.append("rating = ?")
                params.append(rating)

            if updates:
                params.append(user_id)
                query = f"""
                UPDATE search_requests 
                SET {', '.join(updates)} 
                WHERE user_id = ?
                """
                cursor.execute(query, params)
        else:
            # Создаем новую запись (query теперь необязательное)
            cursor.execute("""
            INSERT INTO search_requests (
                user_id, query, genre_filter, limit_results,
                budget, page, rating
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, query, genre, quantity,
                budget, page, rating
            ))

        conn.commit()


def get_user_search_request(user_id: int) -> dict:
    """Возвращает последний поисковый запрос пользователя"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT  
            query, 
            genre_filter as genre, 
            limit_results as quantity,
            budget,
            page,
            rating
        FROM search_requests 
        WHERE user_id = ?
        """, (user_id,))

        result = cursor.fetchone()
        return dict(result) if result else None