from models.user import User, UserFactory
from database import get_connection
from typing import Optional

class UserDAO:
    @staticmethod
    def register_user(user: User) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (user.username, user.password, user.role))
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
        cursor.execute('SELECT username, password, role FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            username, password, role = result
            return UserFactory.create_user(username, password, role)
        return None

    @staticmethod
    def change_admin_password(username: str, old_password: str, new_password: str) -> bool:
        user = UserDAO.get_user_by_credentials(username, old_password)
        if user and user.role == 'admin':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password=? WHERE username=? AND role=?', (new_password, username, 'admin'))
            conn.commit()
            conn.close()
            return True
        return False
