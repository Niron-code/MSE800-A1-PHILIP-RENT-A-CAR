"""
user_controller.py

Controller module for user authentication and management in the car rental system.
Handles admin and customer registration, login, password changes, and menu navigation.
Relies on UserService and related services for business logic and data operations.
"""

from services.user_service import UserService
import pwinput
from controllers.car_controller import CarController
from controllers.rental_controller import RentalController
from utils.utils import Utils
from utils.text_utils import UserTexts as txts

# Forward declarations for type hints
AdminUserController = None
CustomerUserController = None

class UserController:

    @staticmethod
    def user_main_menu(): 
        """
        Displays the main menu for user selection (admin or customer).
        Handles navigation to admin or customer login/registration flows.
        """
        Utils.clear_screen()
        print(txts.txt_welcome)
        print(txts.txt_are_you_admin_or_customer)
        print(txts.txt_admin_option)
        print(txts.txt_customer_option)
        print(txts.txt_exit_option)
        choice = input(txts.txt_exit_prompt).strip()
        if choice == '1':
            globals()['AdminUserController'].admin_login()
        elif choice == '2':
            globals()['CustomerUserController'].customer_menu()
        elif choice == '0':
            print(txts.txt_exiting)
            exit()
        else:
            print(txts.txt_invalid_choice)
            UserController.user_main_menu()

class AdminUserController(UserController):
    @staticmethod
    def admin_login():
        """
        Handles admin login process and authentication.
        Navigates to admin menu on successful login.
        """
        print(txts.txt_admin_login)
        username = input(txts.txt_enter_username).strip()
        password = pwinput.pwinput(txts.txt_enter_password).strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'admin':
            print(txts.txt_welcome_admin.format(username=username))
            AdminUserController.admin_menu(username)
        else:
            print(txts.txt_invalid_admin_credentials)
            UserController.user_main_menu()

    @staticmethod
    def admin_menu(username):
        """
        Displays the admin menu and handles admin actions such as car management,
        rental approval, and password changes.
        """
        Utils.clear_screen()
        print(txts.txt_welcome_admin.format(username=username))
        while True:
            print(txts.txt_admin_menu)
            print(txts.txt_manage_cars)
            print(txts.txt_approve_reject_rentals)
            print(txts.txt_admin_change_password_option)
            print(txts.txt_admin_logout_option)
            choice = input(txts.txt_admin_menu_prompt).strip()
            if choice == '1':
                CarController.management_menu()
            elif choice == '2':
                RentalController.rental_approval_menu()
            elif choice == '3':
                old_pw = pwinput.pwinput(txts.txt_enter_current_password).strip()
                while True:
                    new_pw = pwinput.pwinput(txts.txt_enter_new_password).strip()
                    confirm_pw = pwinput.pwinput(txts.txt_confirm_new_password).strip()
                    if new_pw != confirm_pw:
                        print(txts.txt_passwords_do_not_match)
                        continue
                    if not Utils.is_valid_password(new_pw):
                        print(txts.txt_password_invalid)
                        continue
                    break
                from services.user_service import AdminService
                success = AdminService.change_admin_password(username, old_pw, new_pw)
                if success:
                    print(txts.txt_password_changed_success)
                else:
                    print(txts.txt_incorrect_current_password)
            elif choice == '4':
                print(txts.txt_logging_out)
                Utils.clear_screen()
                UserController.user_main_menu()
                break
            else:
                print(txts.txt_invalid_choice)


class CustomerUserController(UserController):
    @staticmethod
    def customer_menu(): 
        """
        Displays the customer menu for new or existing customers.
        Handles navigation to registration or login flows.
        """
        Utils.clear_screen()
        print(txts.txt_new_customer_option)
        print(txts.txt_existing_customer_option)
        print(txts.txt_back_option)
        choice = input(txts.txt_back_prompt).strip()
        if choice == '1':
            CustomerUserController.customer_signup()
        elif choice == '2':
            CustomerUserController.customer_login()
        elif choice == '0':
            UserController.user_main_menu()
        else:
            print(txts.txt_invalid_choice)
            CustomerUserController.customer_menu()

    @staticmethod
    def customer_signup():
        """
        Handles customer registration, including username, email, and password validation.
        Calls UserService to register the new customer.
        """
        print(txts.txt_customer_registration_header)
        username = input(txts.txt_choose_username).strip()
        while True:
            email = input(txts.txt_enter_email).strip()
            if not Utils.is_valid_email(email):
                print(txts.txt_invalid_email)
                continue
            break
        while True:
            password = pwinput.pwinput(txts.txt_enter_new_password).strip()
            confirm_password = pwinput.pwinput(txts.txt_confirm_new_password).strip()
            if password != confirm_password:
                print(txts.txt_passwords_do_not_match)
                continue
            if not Utils.is_valid_password(password):
                print(txts.txt_password_invalid)
                continue
            break
        success = UserService.register_customer(username, email, password)
        if success:
            print(txts.txt_registration_success)
            CustomerUserController.customer_login()
        else:
            print(txts.txt_username_exists)
            CustomerUserController.customer_signup()

    @staticmethod
    def customer_login():
        """
        Handles customer login process and authentication.
        Navigates to customer main menu on successful login.
        """
        print(txts.txt_customer_login)
        username = input(txts.txt_enter_username).strip()
        password = pwinput.pwinput(txts.txt_enter_password).strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'customer':
            print(txts.txt_welcome_customer.format(username=username, email=user.email))
            CustomerUserController.customer_main_menu(user)
        else:
            print(txts.txt_invalid_customer_credentials)
            CustomerUserController.customer_menu()

    @staticmethod
    def customer_main_menu(user): 
        """
        Displays the main menu for logged-in customers and handles actions such as booking rentals,
        managing bookings, changing password, and logging out.
        """
        Utils.clear_screen()
        while True:
            print(txts.txt_customer_menu.format(username=user.username))
            print(txts.txt_book_rental)
            print(txts.txt_manage_bookings)
            print(txts.txt_change_password_option)
            print(txts.txt_logout_option)
            choice = input(txts.txt_customer_main_menu_prompt).strip()
            if choice == '1':
                RentalController.book_rental_menu(user)
            elif choice == '2':
                RentalController.customer_booking_menu(user)
            elif choice == '3':
                CustomerUserController.change_password(user)
            elif choice == '4':
                print(txts.txt_logging_out)
                Utils.clear_screen()
                UserController.user_main_menu()
                break
            else:
                print(txts.txt_invalid_choice)

    @staticmethod
    def change_password(user):
        """
        Handles the password change process for customers.
        Validates current and new passwords, and calls CustomerService to update the password.
        """
        print(txts.txt_change_password)
        old_password = pwinput.pwinput(txts.txt_enter_current_password).strip()
        while True:
            new_password = pwinput.pwinput(txts.txt_enter_new_password).strip()
            confirm_password = pwinput.pwinput(txts.txt_confirm_new_password).strip()
            if new_password != confirm_password:
                print(txts.txt_passwords_do_not_match)
                continue
            if not Utils.is_valid_password(new_password):
                print(txts.txt_password_invalid)
                continue
            break
        from services.user_service import CustomerService
        success = CustomerService.change_customer_password(user.username, old_password, new_password)
        if success:
            print(txts.txt_password_changed_success)
        else:
            print(txts.txt_password_change_failed)

# Assign classes to globals for forward reference
globals()['AdminUserController'] = AdminUserController
globals()['CustomerUserController'] = CustomerUserController