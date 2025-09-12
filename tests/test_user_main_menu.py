import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class TestUserMainMenu:
    def test_user_main_menu_output(self, monkeypatch, capsys):
        import builtins
        from controllers.user_controller import UserController
        from utils.text_utils import UserTexts as txts
        # Simulate user entering '0' to trigger exit
        monkeypatch.setattr(builtins, 'input', lambda _: '0')
        import pytest
        with pytest.raises(SystemExit):
            UserController.user_main_menu()
        captured = capsys.readouterr()
        assert txts.txt_welcome in captured.out
        assert txts.txt_are_you_admin_or_customer in captured.out
        assert txts.txt_admin_option in captured.out
        assert txts.txt_customer_option in captured.out
        assert txts.txt_exit_option in captured.out
