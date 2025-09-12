from models.user import User, UserFactory
from dao.user_dao import UserDAO

class UserService:

    @staticmethod
    def register_user(username: str, password: str, email: str, role: str) -> bool:
        """Register a new user. Returns True if successful, False if username exists."""
        return UserDAO.register_user(UserFactory.create_user(None, username, password, email, role))

    @staticmethod
    def login_user(username: str, password: str):
        """Login a user and return the appropriate User object (AdminUser, CustomerUser, or User) using UserFactory."""
        result = UserDAO.login_user(username, password)
        if result:
            id, username, password, email, role = result
            return UserFactory.create_user(id, username, password, email, role)
        return None

class AdminService(UserService):

    @staticmethod
    def change_admin_password(username: str, old_password: str, new_password: str) -> bool:
        """Change admin password after verifying the old password."""
        return UserDAO.change_user_password(username, old_password, new_password, 'admin')

class CustomerService(UserService):

    @staticmethod
    def change_customer_password(username: str, old_password: str, new_password: str) -> bool:
        """Change customer password after verifying the old password."""
        return UserDAO.change_user_password(username, old_password, new_password, 'customer')
    
    @staticmethod
    def register_customer(username: str, password: str, email: str) -> bool:
        """Register a new customer."""
        return UserService.register_user(username, password, email, 'customer')
