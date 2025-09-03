from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    role: str

class AdminUser(User):
    def __init__(self, id: int, username: str, password: str, email: str):
        super().__init__(id, username, password, email, 'admin')
    # Admin-specific methods can be added here

class CustomerUser(User):
    def __init__(self, id: int, username: str, password: str, email: str):
        super().__init__(id, username, password, email, 'customer')
    # Customer-specific methods can be added here

class UserFactory:
    @staticmethod
    def create_user(id: int, username: str, password: str, email: str, role: str) -> User:
        if role == 'admin':
            return AdminUser(id, username, password, email)
        elif role == 'customer':
            return CustomerUser(id, username, password, email)
        else:
            return User(id, username, password, email, role)