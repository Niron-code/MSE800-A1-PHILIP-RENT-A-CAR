"""
user.py

Defines the User model hierarchy for the car rental system.
Includes base User class, AdminUser and CustomerUser subclasses, and a UserFactory for instantiation.
"""

from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    role: str

class AdminUser(User):
    """
    Subclass representing an admin user.
    Inherits from User and sets role to 'admin'.
    """
    def __init__(self, id: int, username: str, password: str, email: str):
        super().__init__(id, username, password, email, 'admin')
    # Admin-specific methods can be added here

class CustomerUser(User):
    """
    Subclass representing a customer user.
    Inherits from User and sets role to 'customer'.
    """
    def __init__(self, id: int, username: str, password: str, email: str):
        super().__init__(id, username, password, email, 'customer')
    # Customer-specific methods can be added here

class UserFactory:
    """
    Factory class for creating User instances based on role.
    """
    @staticmethod
    def create_user(id: int, username: str, password: str, email: str, role: str) -> User:
        """
        Create a User, AdminUser, or CustomerUser instance based on the role.
        """
        if role == 'admin':
            return AdminUser(id, username, password, email)
        elif role == 'customer':
            return CustomerUser(id, username, password, email)
        else:
            return User(id, username, password, email, role)