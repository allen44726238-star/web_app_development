import sqlite3

DB_PATH = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @classmethod
    def create(cls, username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @classmethod
    def get_by_id(cls, user_id):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            return cls(**dict(user))
        return None

    @classmethod
    def get_by_username(cls, username):
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user:
            return cls(**dict(user))
        return None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        users = conn.execute("SELECT * FROM user").fetchall()
        conn.close()
        return [cls(**dict(u)) for u in users]

    @classmethod
    def update(cls, user_id, username, password_hash):
        conn = get_db_connection()
        conn.execute(
            "UPDATE user SET username = ?, password_hash = ? WHERE id = ?",
            (username, password_hash, user_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, user_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM user WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
