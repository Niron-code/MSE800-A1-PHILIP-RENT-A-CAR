from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str
    role: str

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