import sqlite3
import bcrypt
from datetime import datetime

class Database:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Users tablosu
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            full_name TEXT,
            theme TEXT DEFAULT 'light',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Income tablosu
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Expenses tablosu
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        conn.commit()
        conn.close()

    def register_user(self, username, password, email="", full_name=""):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('''
            INSERT INTO users (username, password, email, full_name)
            VALUES (?, ?, ?, ?)
            ''', (username, hashed.decode('utf-8'), email, full_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return True
        return False

    def get_user_id(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_user_info(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT username, email, full_name, theme
        FROM users WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                'username': result[0],
                'email': result[1],
                'full_name': result[2],
                'theme': result[3]
            }
        return None

    def update_user_info(self, user_id, email="", full_name=""):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE users
            SET email = ?, full_name = ?
            WHERE id = ?
            ''', (email, full_name, user_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    def update_theme(self, user_id, theme):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE users
            SET theme = ?
            WHERE id = ?
            ''', (theme, user_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    def add_income(self, user_id, category, amount, description=""):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO income (user_id, category, amount, description)
        VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, description))
        conn.commit()
        conn.close()

    def add_expense(self, user_id, category, amount, description=""):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO expenses (user_id, category, amount, description)
        VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, description))
        conn.commit()
        conn.close()

    def get_income_summary(self, user_id, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = 'SELECT category, SUM(amount) FROM income WHERE user_id = ?'
        params = [user_id]
        
        if start_date and end_date:
            query += ' AND date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        
        query += ' GROUP BY category'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def get_expense_summary(self, user_id, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = 'SELECT category, SUM(amount) FROM expenses WHERE user_id = ?'
        params = [user_id]
        
        if start_date and end_date:
            query += ' AND date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        
        query += ' GROUP BY category'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results 