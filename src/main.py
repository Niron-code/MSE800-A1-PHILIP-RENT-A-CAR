from controllers.user_controller import user_main_menu
from database import init_db

init_db()

def main():
    user_main_menu()

if __name__ == "__main__":
    main()
 