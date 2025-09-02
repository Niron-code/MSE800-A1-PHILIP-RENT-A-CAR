from services.user_service import UserService
from database import init_db

init_db()

def main_menu():
    print("Welcome to Philip Rent-A-Car!")
    print("Are you an Admin or Customer?")
    print("1. Admin")
    print("2. Customer")
    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        admin_login()
    elif choice == '2':
        customer_menu()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def admin_login():
    print("\nAdmin Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = UserService.login_user(username, password)
    if user and user.role == 'admin':
        print(f"Welcome, Admin {username}!")
        admin_menu(username)
    else:
        print("Invalid admin credentials.")
        main_menu()

def admin_menu(username):
    while True:
        print("\nAdmin Menu")
        print("1. Change Password")
        print("2. Logout")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            old_pw = input("Enter current password: ").strip()
            new_pw = input("Enter new password: ").strip()
            success = UserService.change_admin_password(username, old_pw, new_pw)
            if success:
                print("Password changed successfully.")
            else:
                print("Incorrect current password.")
        elif choice == '2':
            print("Logging out...")
            main_menu()
            break
        else:
            print("Invalid choice. Try again.")

def customer_menu():
    print("\nAre you a new or existing customer?")
    print("1. New Customer (Sign Up)")
    print("2. Existing Customer (Login)")
    choice = input("Enter choice (1/2): ").strip()
    if choice == '1':
        customer_signup()
    elif choice == '2':
        customer_login()
    else:
        print("Invalid choice. Please try again.")
        customer_menu()

def customer_signup():
    print("\nCustomer Registration")
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()
    success = UserService.register_user(username, password, 'customer')
    if success:
        print("Registration successful! Please login.")
        customer_login()
    else:
        print("Username already exists. Try again.")
        customer_signup()

def customer_login():
    print("\nCustomer Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = UserService.login_user(username, password)
    if user and user.role == 'customer':
        print(f"Welcome, {username}!")
        # Customer menu logic here
    else:
        print("Invalid customer credentials.")
        customer_menu()

if __name__ == "__main__":
    main_menu()
