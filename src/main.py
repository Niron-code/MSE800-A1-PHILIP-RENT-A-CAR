from controllers.user_controller import UserController
from database import init_db

init_db()

def main():
    UserController.user_main_menu()

if __name__ == "__main__":
    main()
