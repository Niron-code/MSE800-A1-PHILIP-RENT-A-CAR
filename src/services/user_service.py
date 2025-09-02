from models.user import User, UserFactory
from dao.user_dao import UserDAO

class UserService:
    @staticmethod
    def register_user(username: str, password: str, role: str) -> bool:
        """Register a new user (admin or customer). Returns True if successful, False if username exists."""
        return UserDAO.register_user(UserFactory.create_user(username, password, role))

    @staticmethod
    def login_user(username: str, password: str):
        """Login a user and return the appropriate User object (AdminUser, CustomerUser, or User) using UserFactory."""
        from database import get_connection
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
    def get_user_type(user_obj) -> str:
        """Return the type of user (admin, customer, or other)."""
        return getattr(user_obj, 'role', None)

    @staticmethod
    def change_admin_password(username: str, old_password: str, new_password: str) -> bool:
        """
        Change admin password after verifying the old password.
        Returns True if successful, False if verification fails or user is not admin.
        """
        user = User.login(username, old_password)
        if user and user.role == 'admin':
            from database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password=? WHERE username=? AND role=?', (new_password, username, 'admin'))
            conn.commit()
            conn.close()
            return True
        return False
