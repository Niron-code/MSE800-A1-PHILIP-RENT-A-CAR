from services.user_service import UserService
import pwinput
from controllers.car_controller import car_management_menu
from controllers.rental_controller import rental_approval_menu, book_rental_menu, customer_booking_menu


# Forward declarations for type hints
AdminUserController = None
CustomerUserController = None

class UserController:
    @staticmethod
    def user_main_menu():
        print("Welcome to Philip Rent-A-Car!")
        print("Are you an Admin or Customer?")
        print("1. Admin")
        print("2. Customer")
        print("0. Exit")
        choice = input("Enter choice (1/2): ").strip()
        if choice == '1':
            globals()['AdminUserController'].admin_login()
        elif choice == '2':
            globals()['CustomerUserController'].customer_menu()
        elif choice == '0':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")
            UserController.user_main_menu()


class AdminUserController(UserController):
    @staticmethod
    def admin_login():
        print("\nAdmin Login")
        username = input("Username: ").strip()
        password = pwinput.pwinput("Password: ").strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'admin':
            print(f"Welcome, Admin {username}!")
            AdminUserController.admin_menu(username)
        else:
            print("Invalid admin credentials.")
            UserController.user_main_menu()

    @staticmethod
    def admin_menu(username):
        while True:
            print("\nAdmin Menu")
            print("1. Manage Cars")
            print("2. Approve/Reject Rentals")
            print("3. Change Password")
            print("4. Logout")
            choice = input("Enter choice: ").strip()
            if choice == '1':
                car_management_menu()
            elif choice == '2':
                rental_approval_menu()
            elif choice == '3':
                old_pw = pwinput.pwinput("Enter current password: ").strip()
                while True:
                    new_pw = pwinput.pwinput("Enter new password: ").strip()
                    confirm_pw = pwinput.pwinput("Confirm new password: ").strip()
                    if new_pw != confirm_pw:
                        print("Passwords do not match. Please try again.")
                    else:
                        break
                from services.user_service import AdminService
                success = AdminService.change_admin_password(username, old_pw, new_pw)
                if success:
                    print("Password changed successfully.")
                else:
                    print("Incorrect current password.")
            elif choice == '4':
                print("Logging out...")
                UserController.user_main_menu()
                break
            else:
                print("Invalid choice. Try again.")


class CustomerUserController(UserController):
    @staticmethod
    def customer_menu():
        print("\nAre you a new or existing customer?")
        print("1. New Customer (Sign Up)")
        print("2. Existing Customer (Login)")
        choice = input("Enter choice (1/2): ").strip()
        if choice == '1':
            CustomerUserController.customer_signup()
        elif choice == '2':
            CustomerUserController.customer_login()
        else:
            print("Invalid choice. Please try again.")
            CustomerUserController.customer_menu()

    @staticmethod
    def customer_signup():
        print("\nCustomer Registration")
        username = input("Choose a username: ").strip()
        while True:
            password = pwinput.pwinput("Choose a password: ").strip()
            confirm_password = pwinput.pwinput("Confirm password: ").strip()
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
            else:
                break
        email = input("Enter your email: ").strip()
        success = UserService.register_user(username, password, email, 'customer')
        if success:
            print("Registration successful! Please login.")
            CustomerUserController.customer_login()
        else:
            print("Username already exists. Try again.")
            CustomerUserController.customer_signup()

    @staticmethod
    def customer_login():
        print("\nCustomer Login")
        username = input("Username: ").strip()
        password = pwinput.pwinput("Password: ").strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'customer':
            print(f"Welcome, {username}! Email: {user.email}")
            CustomerUserController.customer_main_menu(user)
        else:
            print("Invalid customer credentials.")
            CustomerUserController.customer_menu()

    @staticmethod
    def customer_main_menu(user):
        while True:
            print(f"\nCustomer Menu - {user.username}")
            print("1. Book Rental")
            print("2. Manage My Bookings")
            print("3. Change Password")
            print("4. Logout")
            choice = input("Enter choice: ").strip()
            if choice == '1':
                book_rental_menu(user)
            elif choice == '2':
                customer_booking_menu(user)
            elif choice == '3':
                CustomerUserController.change_password(user)
            elif choice == '4':
                print("Logging out...")
                UserController.user_main_menu()
                break
            else:
                print("Invalid choice. Try again.")

    @staticmethod
    def change_password(user):
        print("\nChange Password")
        old_password = pwinput.pwinput("Enter current password: ").strip()
        while True:
            new_password = pwinput.pwinput("Enter new password: ").strip()
            confirm_password = pwinput.pwinput("Confirm new password: ").strip()
            if new_password != confirm_password:
                print("Passwords do not match. Please try again.")
            else:
                break
        from services.user_service import CustomerService
        success = CustomerService.change_customer_password(user.username, old_password, new_password)
        if success:
            print("Password changed successfully!.")
        else:
            print("Incorrect current password. Password change failed.")

# Assign classes to globals for forward reference
globals()['AdminUserController'] = AdminUserController
globals()['CustomerUserController'] = CustomerUserController