"""
user_dao.py

Data Access Object (DAO) module for user-related database operations.
Provides methods for user authentication, registration, password management, and email retrieval.
Relies on the User model, bcrypt for password hashing, and database connection utility.
"""

from models.user import User, UserFactory
from database import Database
from typing import Optional
import bcrypt

class UserDAO:
    """
    DAO class for performing CRUD operations and authentication on user records in the database.
    """
    @staticmethod
    def login_user(username: str, password: str):
        """
        Authenticates a user by username and password.
        Returns user details tuple if successful, None otherwise.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT id, username, password, email, role FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            id, username_db, hashed_pw, email, role = result
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
                return (id, username_db, hashed_pw, email, role)
        return None
    
    @staticmethod
    def change_user_password(username: str, old_password: str, new_password: str, role: str) -> bool:
        """
        Changes the password for a user if the old password matches.
        Returns True if the operation is successful, False otherwise.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT password FROM users WHERE username=? AND role=?', (username, role))
        result = cursor.fetchone()
        if result and bcrypt.checkpw(old_password.encode('utf-8'), result[0].encode('utf-8')):
            hashed_new_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('UPDATE users SET password=? WHERE username=? AND role=?', (hashed_new_pw, username, role))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
    
    @staticmethod
    def register_user(user: User) -> bool:
        """
        Registers a new user in the database.
        Returns True if the operation is successful, False otherwise.
        """
        conn, cursor = Database.get_conn_cursor()
        try:
            hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)', (user.username, hashed_pw, user.role, user.email))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_by_credentials(username: str, password: str) -> Optional[User]:
        """
        Retrieves a User object by username and password if credentials are valid.
        Returns a User instance or None.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT id, username, password, role FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            id, username_db, hashed_pw, role = result
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
                return UserFactory.create_user(id, username_db, hashed_pw, role)
        return None

    @staticmethod
    def get_user_email_by_id(user_id: int) -> Optional[str]:
        """
        Retrieves the email address for a user by user_id.
        Returns the email as a string or None if not found.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT email FROM users WHERE id=?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None
