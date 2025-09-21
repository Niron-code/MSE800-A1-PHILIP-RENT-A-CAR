import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from services.user_service import UserService, AdminService, CustomerService

class DummyUserDAO:
    users = {}
    @classmethod
    def register_user(cls, user):
        if user.username in cls.users:
            return False
        cls.users[user.username] = user
        return True
    @classmethod
    def login_user(cls, username, password):
        user = cls.users.get(username)
        if user and user.password == password:
            return (1, user.username, user.password, user.email, user.role)
        return None
    @classmethod
    def change_user_password(cls, username, old_password, new_password, role):
        user = cls.users.get(username)
        if user and user.password == old_password and user.role == role:
            user.password = new_password
            return True
        return False

# Patch UserDAO in the service modules for isolated testing
import services.user_service as user_service_mod
user_service_mod.UserDAO = DummyUserDAO

class DummyUser:
    def __init__(self, id, username, password, email, role):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

class DummyUserFactory:
    @staticmethod
    def create_user(id, username, password, email, role):
        return DummyUser(id, username, password, email, role)

user_service_mod.UserFactory = DummyUserFactory

class TestUserService:
    def test_register_user(self):
        DummyUserDAO.users.clear()
        assert UserService.register_user('alice', 'pass', 'alice@email.com', 'customer') is True
        assert UserService.register_user('alice', 'pass', 'alice@email.com', 'customer') is False

    def test_login_user(self):
        DummyUserDAO.users.clear()
        UserService.register_user('bob', 'bob@email.com', 'secret', 'admin')
        user = UserService.login_user('bob', 'secret')
        assert user is not None
        assert user.username == 'bob'
        assert UserService.login_user('bob', 'wrong') is None

    def test_admin_password_change(self):
        DummyUserDAO.users.clear()
        UserService.register_user('admin', 'admin@email.com', 'old', 'admin')
        assert AdminService.change_admin_password('admin', 'old', 'new') is True
        assert AdminService.change_admin_password('admin', 'old', 'new2') is False
        assert AdminService.change_admin_password('admin', 'new', 'new2') is True

    def test_customer_password_change(self):
        DummyUserDAO.users.clear()
        UserService.register_user('cust', 'cust@email.com', 'old', 'customer')
        assert CustomerService.change_customer_password('cust', 'old', 'new') is True
        assert CustomerService.change_customer_password('cust', 'old', 'new2') is False
        assert CustomerService.change_customer_password('cust', 'new', 'new2') is True
