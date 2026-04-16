import sqlite3

DB_PATH = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class History:
    def __init__(self, id, user_id, fortune_id, created_at):
        self.id = id
        self.user_id = user_id
        self.fortune_id = fortune_id
        self.created_at = created_at

    @classmethod
    def create(cls, user_id, fortune_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (user_id, fortune_id) VALUES (?, ?)",
            (user_id, fortune_id)
        )
        conn.commit()
        history_id = cursor.lastrowid
        conn.close()
        return history_id

    @classmethod
    def get_by_id(cls, history_id):
        conn = get_db_connection()
        history = conn.execute("SELECT * FROM history WHERE id = ?", (history_id,)).fetchone()
        conn.close()
        if history:
            return cls(**dict(history))
        return None

    @classmethod
    def get_by_user_id(cls, user_id):
        conn = get_db_connection()
        # Join with fortune to get detailed history data including python
        histories = conn.execute(
            """
            SELECT h.*, f.title as fortune_title, f.fortune_num 
            FROM history h
            JOIN fortune f ON h.fortune_id = f.id
            WHERE h.user_id = ? 
            ORDER BY h.created_at DESC
            """, 
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(h) for h in histories]

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        histories = conn.execute("SELECT * FROM history").fetchall()
        conn.close()
        return [cls(**dict(h)) for h in histories]

    @classmethod
    def update(cls, history_id, user_id, fortune_id):
        conn = get_db_connection()
        conn.execute(
            "UPDATE history SET user_id = ?, fortune_id = ? WHERE id = ?",
            (user_id, fortune_id, history_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, history_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM history WHERE id = ?", (history_id,))
        conn.commit()
        conn.close()
