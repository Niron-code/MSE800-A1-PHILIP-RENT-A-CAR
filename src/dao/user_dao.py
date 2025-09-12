from models.user import User, UserFactory
from database import get_connection
from typing import Optional

class UserDAO:

    @staticmethod
    def login_user(username: str, password: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, email, role FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def change_user_password(username: str, old_password: str, new_password: str, role: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username=? AND password=? AND role=?', (username, old_password, role))
        result = cursor.fetchone()
        if result:
            cursor.execute('UPDATE users SET password=? WHERE username=? AND role=?', (new_password, username, role))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
    
    @staticmethod
    def register_user(user: User) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)', (user.username, user.password, user.role, user.email))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_by_credentials(username: str, password: str) -> Optional[User]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, role FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            id, username, password, role = result
            return UserFactory.create_user(id, username, password, role)
        return None


    @staticmethod
    def get_user_email_by_id(user_id: int) -> Optional[str]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM users WHERE id=?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None
