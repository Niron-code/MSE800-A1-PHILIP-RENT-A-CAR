"""
user_service.py

Service layer for user-related business logic in the car rental system.
Provides methods for user registration, authentication, and password management by interacting with the DAO and model layers.
"""

from models.user import User, UserFactory
from dao.user_dao import UserDAO

class UserService:
    """
    Service class for user management operations.
    Handles registration and authentication, delegating database operations to UserDAO.
    """
    @staticmethod
    def register_user(username: str, email: str, password: str, role: str) -> bool:
        """
        Register a new user. Returns True if successful, False if username exists.
        """
        return UserDAO.register_user(UserFactory.create_user(None, username, password, email, role))

    @staticmethod
    def login_user(username: str, password: str):
        """
        Login a user and return the appropriate User object (AdminUser, CustomerUser, or User) using UserFactory.
        Returns a User instance or None if authentication fails.
        """
        result = UserDAO.login_user(username, password)
        if result:
            id, username, password, email, role = result
            return UserFactory.create_user(id, username, password, email, role)
        return None

class AdminService(UserService):
    """
    Service class for admin-specific operations.
    Inherits from UserService and adds admin password management.
    """
    @staticmethod
    def change_admin_password(username: str, old_password: str, new_password: str) -> bool:
        """
        Change admin password after verifying the old password.
        Returns True if the operation is successful, False otherwise.
        """
        return UserDAO.change_user_password(username, old_password, new_password, 'admin')

class CustomerService(UserService):
    """
    Service class for customer-specific operations.
    Inherits from UserService and adds customer password management and registration.
    """
    @staticmethod
    def change_customer_password(username: str, old_password: str, new_password: str) -> bool:
        """
        Change customer password after verifying the old password.
        Returns True if the operation is successful, False otherwise.
        """
        return UserDAO.change_user_password(username, old_password, new_password, 'customer')
    
    @staticmethod
    def register_customer(username: str, password: str, email: str) -> bool:
        """
        Register a new customer.
        Returns True if the operation is successful, False otherwise.
        """
        success = UserService.register_user(username, email, password, "customer")
