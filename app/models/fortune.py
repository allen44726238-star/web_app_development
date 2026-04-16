import sqlite3

DB_PATH = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Fortune:
    def __init__(self, id, fortune_num, title, poem, explanation, career_explanation, love_explanation, created_at):
        self.id = id
        self.fortune_num = fortune_num
        self.title = title
        self.poem = poem
        self.explanation = explanation
        self.career_explanation = career_explanation
        self.love_explanation = love_explanation
        self.created_at = created_at

    @classmethod
    def create(cls, fortune_num, title, poem, explanation, career_explanation=None, love_explanation=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO fortune 
            (fortune_num, title, poem, explanation, career_explanation, love_explanation) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (fortune_num, title, poem, explanation, career_explanation, love_explanation)
        )
        conn.commit()
        fortune_id = cursor.lastrowid
        conn.close()
        return fortune_id

    @classmethod
    def get_by_id(cls, fortune_id):
        conn = get_db_connection()
        fortune = conn.execute("SELECT * FROM fortune WHERE id = ?", (fortune_id,)).fetchone()
        conn.close()
        if fortune:
            return cls(**dict(fortune))
        return None

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        fortunes = conn.execute("SELECT * FROM fortune").fetchall()
        conn.close()
        return [cls(**dict(f)) for f in fortunes]

    @classmethod
    def draw_random(cls):
        conn = get_db_connection()
        # Query random row
        fortune = conn.execute("SELECT * FROM fortune ORDER BY RANDOM() LIMIT 1").fetchone()
        conn.close()
        if fortune:
            return cls(**dict(fortune))
        return None

    @classmethod
    def update(cls, fortune_id, fortune_num, title, poem, explanation, career_explanation, love_explanation):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE fortune 
            SET fortune_num = ?, title = ?, poem = ?, explanation = ?, 
                career_explanation = ?, love_explanation = ? 
            WHERE id = ?
            """,
            (fortune_num, title, poem, explanation, career_explanation, love_explanation, fortune_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, fortune_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM fortune WHERE id = ?", (fortune_id,))
        conn.commit()
        conn.close()
