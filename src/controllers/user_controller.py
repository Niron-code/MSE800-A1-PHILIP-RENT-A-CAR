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

import sys
from utils.utils import Utils


# Forward declarations for type hints
AdminUserController = None
CustomerUserController = None

class UserController:
    @staticmethod
    def entry_point():
        # Always load English first for language selection
        texts_en = Utils.load_texts('en')
        print(texts_en['UserTexts']['txt_select_language'])
        print(texts_en['UserTexts']['txt_language_english'])
        print(texts_en['UserTexts']['txt_language_maori'])
        lang_choice = input(texts_en['UserTexts']['txt_language_prompt']).strip()
        language = 'maori' if lang_choice == '2' else 'en'
        texts = Utils.load_texts(language)
        # Call main menu using self class reference
        globals()['UserController'].user_main_menu(texts)

    @staticmethod
    def user_main_menu(texts):
        """
        Displays the main menu for user selection (admin or customer).
        Handles navigation to admin or customer login/registration flows.
        """
        user_txts = texts['UserTexts']
        Utils.clear_screen()
        print(user_txts['txt_welcome'])
        print(user_txts['txt_are_you_admin_or_customer'])
        print(user_txts['txt_admin_option'])
        print(user_txts['txt_customer_option'])
        print(user_txts['txt_exit_option'])
        choice = input(user_txts['txt_customer_menu_prompt']).strip()
        if choice == '1':
            globals()['AdminUserController'].admin_login(texts)
        elif choice == '2':
            globals()['CustomerUserController'].customer_menu(texts)
        elif choice == '0':
            print(user_txts['txt_exiting'])
            sys.exit()
        else:
            print(user_txts['txt_invalid_choice'])
            UserController.user_main_menu(texts)

class AdminUserController(UserController):
    @staticmethod
    def admin_login(texts):
        """
        Handles admin login process and authentication.
        Navigates to admin menu on successful login.
        """
        user_txts = texts['UserTexts']
        print(user_txts['txt_admin_login'])
        username = input(user_txts['txt_enter_username']).strip()
        password = pwinput.pwinput(user_txts['txt_enter_password']).strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'admin':
            print(user_txts['txt_welcome_admin'].format(username=username))
            AdminUserController.admin_menu(username, texts)
        else:
            print(user_txts['txt_invalid_admin_credentials'])
            UserController.user_main_menu(texts)

    @staticmethod
    def admin_menu(username, texts):
        """
        Displays the admin menu and handles admin actions such as car management,
        rental approval, and password changes.
        """
        user_txts = texts['UserTexts']
        Utils.clear_screen()
        print(user_txts['txt_welcome_admin'].format(username=username))
        while True:
            print(user_txts['txt_admin_menu'])
            print(user_txts['txt_manage_cars'])
            print(user_txts['txt_approve_reject_rentals'])
            print(user_txts['txt_admin_change_password_option'])
            print(user_txts['txt_admin_logout_option'])
            choice = input(user_txts['txt_admin_menu_prompt']).strip()
            if choice == '1':
                CarController.management_menu(texts)
            elif choice == '2':
                RentalController.rental_approval_menu(texts)
            elif choice == '3':
                old_pw = pwinput.pwinput(user_txts['txt_enter_current_password']).strip()
                while True:
                    new_pw = pwinput.pwinput(user_txts['txt_enter_new_password']).strip()
                    confirm_pw = pwinput.pwinput(user_txts['txt_confirm_new_password']).strip()
                    if new_pw != confirm_pw:
                        print(user_txts['txt_passwords_do_not_match'])
                        continue
                    if not Utils.is_valid_password(new_pw):
                        print(user_txts['txt_password_invalid'])
                        continue
                    break
                from services.user_service import AdminService
                success = AdminService.change_admin_password(username, old_pw, new_pw)
                if success:
                    print(user_txts['txt_password_changed_success'])
                else:
                    print(user_txts['txt_incorrect_current_password'])
            elif choice == '4':
                print(user_txts['txt_logging_out'])
                Utils.clear_screen()
                UserController.user_main_menu(texts)
                break
            else:
                print(user_txts['txt_invalid_choice'])


class CustomerUserController(UserController):
    @staticmethod
    def customer_menu(texts):
        """
        Displays the customer menu for new or existing customers.
        Handles navigation to registration or login flows.
        """
        user_txts = texts['UserTexts']
        Utils.clear_screen()
        print(user_txts['txt_new_customer_option'])
        print(user_txts['txt_existing_customer_option'])
        print(user_txts['txt_back_option'])
        choice = input(user_txts['txt_back_prompt']).strip()
        if choice == '1':
            CustomerUserController.customer_signup(texts)
        elif choice == '2':
            CustomerUserController.customer_login(texts)
        elif choice == '0':
            UserController.user_main_menu(texts)
        else:
            print(user_txts['txt_invalid_choice'])
            CustomerUserController.customer_menu(texts)

    @staticmethod
    def customer_signup(texts):
        """
        Handles customer registration, including username, email, and password validation.
        Calls UserService to register the new customer.
        """
        user_txts = texts['UserTexts']
        print(user_txts['txt_customer_registration_header'])
        username = input(user_txts['txt_choose_username']).strip()
        while True:
            email = input(user_txts['txt_enter_email']).strip()
            if not Utils.is_valid_email(email):
                print(user_txts['txt_invalid_email'])
                continue
            break
        while True:
            password = pwinput.pwinput(user_txts['txt_enter_new_password']).strip()
            confirm_password = pwinput.pwinput(user_txts['txt_confirm_new_password']).strip()
            if password != confirm_password:
                print(user_txts['txt_passwords_do_not_match'])
                continue
            if not Utils.is_valid_password(password):
                print(user_txts['txt_password_invalid'])
                continue
            break
        success = UserService.register_customer(username, email, password)
        if success:
            print(user_txts['txt_registration_success'])
            CustomerUserController.customer_login(texts)
        else:
            print(user_txts['txt_username_exists'])
            CustomerUserController.customer_signup(texts)

    @staticmethod
    def customer_login(texts):
        """
        Handles customer login process and authentication.
        Navigates to customer main menu on successful login.
        """
        user_txts = texts['UserTexts']
        print(user_txts['txt_customer_login'])
        username = input(user_txts['txt_enter_username']).strip()
        password = pwinput.pwinput(user_txts['txt_enter_password']).strip()
        user = UserService.login_user(username, password)
        if user and user.role == 'customer':
            print(user_txts['txt_welcome_customer'].format(username=username, email=user.email))
            CustomerUserController.customer_main_menu(user, texts)
        else:
            print(user_txts['txt_invalid_customer_credentials'])
            CustomerUserController.customer_menu(texts)

    @staticmethod
    def customer_main_menu(user, texts):
        """
        Displays the main menu for logged-in customers and handles actions such as booking rentals,
        managing bookings, changing password, and logging out.
        """
        user_txts = texts['UserTexts']
        Utils.clear_screen()
        while True:
            print(user_txts['txt_customer_menu'].format(username=user.username))
            print(user_txts['txt_book_rental'])
            print(user_txts['txt_manage_bookings'])
            print(user_txts['txt_change_password_option'])
            print(user_txts['txt_logout_option'])
            choice = input(user_txts['txt_customer_main_menu_prompt']).strip()
            if choice == '1':
                RentalController.book_rental_menu(user, texts)
            elif choice == '2':
                RentalController.customer_booking_menu(user, texts)
            elif choice == '3':
                CustomerUserController.change_password(user, texts)
            elif choice == '4':
                print(user_txts['txt_logging_out'])
                Utils.clear_screen()
                UserController.user_main_menu(texts)
                break
            else:
                print(user_txts['txt_invalid_choice'])

    @staticmethod
    def change_password(user, texts):
        """
        Handles the password change process for customers.
        Validates current and new passwords, and calls CustomerService to update the password.
        """
        user_txts = texts['UserTexts']
        print(user_txts['txt_change_password'])
        old_password = pwinput.pwinput(user_txts['txt_enter_current_password']).strip()
        while True:
            new_password = pwinput.pwinput(user_txts['txt_enter_new_password']).strip()
            confirm_password = pwinput.pwinput(user_txts['txt_confirm_new_password']).strip()
            if new_password != confirm_password:
                print(user_txts['txt_passwords_do_not_match'])
                continue
            if not Utils.is_valid_password(new_password):
                print(user_txts['txt_password_invalid'])
                continue
            break
        from services.user_service import CustomerService
        success = CustomerService.change_customer_password(user.username, old_password, new_password)
        if success:
            print(user_txts['txt_password_changed_success'])
        else:
            print(user_txts['txt_password_change_failed'])

# Assign classes to globals for forward reference
globals()['AdminUserController'] = AdminUserController
globals()['CustomerUserController'] = CustomerUserController