import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from controllers.user_controller import UserController
from utils.text_utils import UserTexts as txts

class TestUserController:
    def test_main_menu_texts(self, monkeypatch, capsys):
        # Simulate user entering '0' to exit
        monkeypatch.setattr('builtins.input', lambda _: '0')
        with pytest.raises(SystemExit):
            UserController.user_main_menu()
        captured = capsys.readouterr()
        assert txts.txt_welcome in captured.out
        assert txts.txt_are_you_admin_or_customer in captured.out
        assert txts.txt_admin_option in captured.out
        assert txts.txt_customer_option in captured.out
        assert txts.txt_exit_option in captured.out

    def test_main_menu_invalid_choice(self, monkeypatch, capsys):
        inputs = iter(['invalid', '0'])  # First invalid, then exit
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(SystemExit):
            UserController.user_main_menu()
        captured = capsys.readouterr()
        assert txts.txt_invalid_choice in captured.out
        assert txts.txt_welcome in captured.out  # Menu displayed again

    def test_admin_login_success(self, monkeypatch, capsys):
        # Simulate username and password input
        inputs = iter(['admin', 'secret'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        # Patch pwinput.pwinput to return password
        import pwinput
        monkeypatch.setattr(pwinput, 'pwinput', lambda _: 'secret')
        # Patch UserService.login_user to return a mock admin user
        from controllers import user_controller
        class MockAdmin:
            role = 'admin'
            username = 'admin'
        monkeypatch.setattr(user_controller, 'UserService', type('MockService', (), {'login_user': staticmethod(lambda u, p: MockAdmin())}))
        # Patch admin_menu to exit after login
        monkeypatch.setattr(user_controller.AdminUserController, 'admin_menu', lambda username: exit())
        with pytest.raises(SystemExit):
            user_controller.AdminUserController.admin_login()
        captured = capsys.readouterr()
        assert user_controller.txts.txt_admin_login in captured.out
        assert user_controller.txts.txt_welcome_admin.format(username='admin') in captured.out

    def test_admin_login_fail(self, monkeypatch, capsys):
        # Simulate username and password input
        inputs = iter(['admin', 'wrongpw'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        import pwinput
        monkeypatch.setattr(pwinput, 'pwinput', lambda _: 'wrongpw')
        from controllers import user_controller
        monkeypatch.setattr(user_controller, 'UserService', type('MockService', (), {'login_user': staticmethod(lambda u, p: None)}))
        with pytest.raises(SystemExit):
            # Patch user_main_menu to exit after failed login
            monkeypatch.setattr(user_controller.UserController, 'user_main_menu', lambda: exit())
            user_controller.AdminUserController.admin_login()
        captured = capsys.readouterr()
        assert user_controller.txts.txt_admin_login in captured.out
        assert user_controller.txts.txt_invalid_admin_credentials in captured.out

