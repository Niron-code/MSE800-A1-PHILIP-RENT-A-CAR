from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    password: str
    role: str

class AdminUser(User):
    def __init__(self, id: int, username: str, password: str):
        super().__init__(id, username, password, 'admin')
    # Admin-specific methods can be added here

class CustomerUser(User):
    def __init__(self, id: int, username: str, password: str):
        super().__init__(id, username, password, 'customer')
    # Customer-specific methods can be added here

class UserFactory:
    @staticmethod
    def create_user(id: int, username: str, password: str, role: str) -> User:
        if role == 'admin':
            return AdminUser(id, username, password)
        elif role == 'customer':
            return CustomerUser(id, username, password)
        else:
            return User(id, username, password, role)