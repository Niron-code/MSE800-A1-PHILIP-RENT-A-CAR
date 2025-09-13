import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from models.user import User, AdminUser, CustomerUser, UserFactory

class TestUserModel:
    def test_user_instantiation(self):
        user = User(1, 'philip', 'pass', 'philip@email.com', 'admin')
        assert user.id == 1
        assert user.username == 'philip'
        assert user.password == 'pass'
        assert user.email == 'philip@email.com'
        assert user.role == 'admin'

    def test_admin_user_instantiation(self):
        admin = AdminUser(2, 'admin', 'secret', 'admin@email.com')
        assert admin.role == 'admin'
        assert isinstance(admin, User)

    def test_customer_user_instantiation(self):
        customer = CustomerUser(3, 'susha', 'pw', 'susha@email.com')
        assert customer.role == 'customer'
        assert isinstance(customer, User)

    def test_user_factory_admin(self):
        user = UserFactory.create_user(4, 'super', 'pw', 'super@email.com', 'admin')
        assert isinstance(user, AdminUser)
        assert user.role == 'admin'

    def test_user_factory_customer(self):
        user = UserFactory.create_user(5, 'cust', 'pw', 'cust@email.com', 'customer')
        assert isinstance(user, CustomerUser)
        assert user.role == 'customer'
