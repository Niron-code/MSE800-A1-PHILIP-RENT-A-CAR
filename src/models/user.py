import sqlite3
from database import get_connection

class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def register(username: str, password: str, role: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def login(username: str, password: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, role FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            _, username, password, role = result
            return UserFactory.create_user(username, password, role)
        return None

class AdminUser(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, 'admin')
    # Admin-specific methods can be added here

class CustomerUser(User):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, 'customer')
    # Customer-specific methods can be added here

class UserFactory:
    @staticmethod
    def create_user(username: str, password: str, role: str) -> User:
        if role == 'admin':
            return AdminUser(username, password)
        elif role == 'customer':
            return CustomerUser(username, password)
        else:
            return User(username, password, role)
