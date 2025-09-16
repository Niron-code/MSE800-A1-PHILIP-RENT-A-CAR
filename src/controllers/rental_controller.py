"""
rental_controller.py

Controller module for rental operations in the car rental system.
Handles user interaction for booking, approving, updating, and cancelling rentals.
Relies on RentalService and EmailService for business logic and notifications.
"""

from dao.user_dao import UserDAO
from dao.car_dao import CarDAO
from services.rental_service import RentalService
from services.email_service import EmailService

from utils.utils import Utils


class RentalController:
    """
    Controller class for rental operations in the car rental system.
    Handles user interaction for booking, approving, updating, and cancelling rentals.
    Relies on RentalService and EmailService for business logic and notifications.
    """

    @staticmethod
    def rental_approval_menu(texts):
        """
        Displays the rental approval menu for admin users.
        Allows admins to approve or reject pending rental requests and sends notification emails.
        """
        rental_txts = texts['RentalTexts']
        print(rental_txts['pending_requests'])
        pending = RentalService.get_pending_rentals()
        if not pending:
            print(rental_txts['no_pending'])
            return
        for rental in pending:
            print(f"ID: {rental[0]}, User ID: {rental[1]}, Car ID: {rental[2]}, Start: {rental[3]}, End: {rental[4]}, Fee: {rental[6]}, Status: {rental[5]}")
        rental_id = input(rental_txts['rental_id_prompt']).strip()
        if not rental_id:
            return
        try:
            rental_id = int(rental_id)
        except ValueError:
            print(rental_txts['invalid_rental_id'])
            return
        action = input(rental_txts['approve_or_reject']).strip().lower()
        rental = next((r for r in pending if r[0] == rental_id), None)
        if not rental:
            print(rental_txts['not_found'])
            return
        user_email = UserDAO.get_user_email_by_id(rental[1])
        car_id = rental[2]
        start_date = rental[3]
        end_date = rental[4]
        # Fetch car make/model for email
        car = CarDAO.get_car_by_id(car_id)
        car_make = car[1] if car else "Unknown"
        car_model = car[2] if car else "Unknown"
        if action == 'a':
            success = RentalService.update_rental_status(rental_id, 'approved')
            if success:
                print(rental_txts['approved'])
                if user_email:
                    amount = rental[6]
                    EmailService.send_approval_email(user_email, car_make, car_model, start_date, end_date, amount, texts)
            else:
                print(rental_txts['approve_fail'])
        elif action == 'r':
            success = RentalService.update_rental_status(rental_id, 'rejected')
            if success:
                print(rental_txts['rejected'])
                if user_email:
                    EmailService.send_rejection_email(user_email, car_make, car_model, start_date, end_date, texts)
            else:
                print(rental_txts['reject_fail'])
        else:
            print(rental_txts['invalid_action'])

    @staticmethod
    def book_rental_menu(user, texts):
        """
        Allows a customer to book a rental car by selecting dates and a car.
        Validates date input and displays available cars for the selected period.
        Calculates total fee and confirms booking with the user.
        """
        rental_txts = texts['RentalTexts']
        while True:
            start_date = input(rental_txts['start_date_prompt']).strip()
            if not Utils.is_start_date_today_or_future(start_date):
                print(rental_txts['start_date_invalid'])
                continue
            while True:
                end_date = input(rental_txts['end_date_prompt']).strip()
                if not Utils.is_end_date_valid(start_date, end_date):
                    print(rental_txts['end_date_invalid'])
                    continue
                break
            break
        cars, car_status = RentalService.get_car_status_for_dates(start_date, end_date)
        available_cars = [car for car in cars if car_status.get(car[0], 'available') == 'available']
        print(rental_txts['cars_for_dates'])
        for car in cars:
            status = car_status.get(car[0], 'available')
            if status == 'available':
                customer_friendly_status = "AVAILABLE"
                print(f"ID: {car[0]}, {car[1]} {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Type: {car[8]}, Rate: ${car[9]}/day, Min Days: {car[6]}, Max Days: {car[7]} - {customer_friendly_status}")
            elif status == 'pending':
                customer_friendly_status = "Booking Requested"
                print(f"ID: {car[0]}, {car[1]} {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Type: {car[8]}, Rate: ${car[9]}/day, Min Days: {car[6]}, Max Days: {car[7]} - {customer_friendly_status}")
            elif status == 'approved':
                customer_friendly_status = "Booked Already"
                print(f"ID: {car[0]}, {car[1]} {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Type: {car[8]}, Rate: ${car[9]}/day, Min Days: {car[6]}, Max Days: {car[7]} - {customer_friendly_status}")
            else:
                customer_friendly_status = f"UNAVAILABLE ({status})"
                print(f"ID: {car[0]}, {car[1]} {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Type: {car[8]}, Rate: ${car[9]}/day, Min Days: {car[6]}, Max Days: {car[7]} - {customer_friendly_status}")
        if not available_cars:
            print(rental_txts['no_cars_available'])
            return
        car_id = input(rental_txts['car_id_prompt']).strip()
        try:
            car_id = int(car_id)
        except ValueError:
            print(rental_txts['invalid_car_id'])
            return
        if car_id not in [car[0] for car in available_cars]:
            print(rental_txts['not_available'])
            return
        extra_charges = 0.0
        total_fee = RentalService.calculate_rental_fee(car_id, start_date, end_date, extra_charges)
        print(rental_txts['total_fee'].format(fee=total_fee))
        confirm = input(rental_txts['confirm_booking']).strip().lower()
        if confirm == 'yes':
            success = RentalService.book_rental(user_id=user.id, car_id=car_id, start_date=start_date, end_date=end_date, total_fee=total_fee)
            if success:
                print(rental_txts['booked_success'])
            else:
                print(rental_txts['booked_fail'])
        else:
            print(rental_txts['booking_cancelled'])

    @staticmethod
    def customer_booking_menu(user, texts):
        """
        Displays the customer booking menu for managing bookings.
        Allows viewing, cancelling, and updating bookings for the logged-in customer.
        """
        rental_txts = texts['RentalTexts']
        while True:
            print(rental_txts['booking_menu'])
            print(rental_txts['view_bookings'])
            print(rental_txts['cancel_booking'])
            print(rental_txts['update_booking'])
            print(rental_txts['back_to_customer'])
            choice = input(rental_txts['booking_choice']).strip()
            if choice == '1':
                bookings = RentalService.get_bookings_for_user(user.id)
                if not bookings:
                    print(rental_txts['no_bookings'])
                else:
                    for booking in bookings:
                        print(f"ID: {booking[0]}, Car ID: {booking[2]}, Start: {booking[3]}, End: {booking[4]}, Status: {booking[5]}, Fee: {booking[6]}")
            elif choice == '2':
                rental_id = input(rental_txts['booking_id_cancel']).strip()
                try:
                    rental_id = int(rental_id)
                    success = RentalService.cancel_booking(rental_id, user.id)
                    if success:
                        print(rental_txts['cancel_success'])
                    else:
                        print(rental_txts['cancel_fail'])
                except ValueError:
                    print(rental_txts['invalid_booking_id'])
            elif choice == '3':
                rental_id = input(rental_txts['booking_id_update']).strip()
                try:
                    rental_id = int(rental_id)
                    while True:
                        start_date = input(rental_txts['new_start_date']).strip()
                        if not Utils.is_start_date_today_or_future(start_date):
                            print(rental_txts['start_date_invalid'])
                            continue
                        end_date = input(rental_txts['new_end_date']).strip()
                        if not Utils.is_end_date_valid(start_date, end_date):
                            print(rental_txts['end_date_invalid'])
                            continue
                        break
                    car_id = input(rental_txts['new_car_id']).strip()
                    car_id = int(car_id) if car_id else None
                    success = RentalService.update_booking(rental_id, user.id, start_date, end_date, car_id)
                    if success:
                        print(rental_txts['update_success'])
                    else:
                        print(rental_txts['update_fail'])
                except ValueError:
                    print(rental_txts['invalid_input'])
            elif choice == '4':
                break
            else:
                print(rental_txts['invalid_choice'])
