from email.mime.text import MIMEText
from dao.user_dao import UserDAO
from services.rental_service import RentalService
from services.email_service import EmailService
from utils.prompt_utils import RentalTexts as txts
from utils.utils import Utils


def rental_approval_menu():
    print(txts.pending_requests)
    pending = RentalService.get_pending_rentals()
    if not pending:
        print(txts.no_pending)
        return
    for rental in pending:
        print(f"ID: {rental[0]}, User ID: {rental[1]}, Car ID: {rental[2]}, Start: {rental[3]}, End: {rental[4]}, Fee: {rental[6]}, Status: {rental[5]}")
    rental_id = input(txts.rental_id_prompt).strip()
    if not rental_id:
        return
    try:
        rental_id = int(rental_id)
    except ValueError:
        print(txts.invalid_rental_id)
        return
    action = input(txts.approve_or_reject).strip().lower()
    rental = next((r for r in pending if r[0] == rental_id), None)
    if not rental:
        print(txts.not_found)
        return
    user_email = UserDAO.get_user_email_by_id(rental[1])
    car_id = rental[2]
    start_date = rental[3]
    end_date = rental[4]
    if action == 'a':
        success = RentalService.update_rental_status(rental_id, 'approved')
        if success:
            print(txts.approved)
            if user_email:
                amount = rental[6]
                EmailService.send_approval_email(user_email, car_id, start_date, end_date, amount)
        else:
            print(txts.approve_fail)
    elif action == 'r':
        success = RentalService.update_rental_status(rental_id, 'rejected')
        if success:
            print(txts.rejected)
            if user_email:
                EmailService.send_rejection_email(user_email, car_id, start_date, end_date)
        else:
            print(txts.reject_fail)
    else:
        print(txts.invalid_action)

def book_rental_menu(user):
    while True:
        start_date = input(txts.start_date_prompt).strip()
        if not Utils.is_start_date_today_or_future(start_date):
            print(txts.start_date_invalid)
            continue
        end_date = input(txts.end_date_prompt).strip()
        if not Utils.is_end_date_valid(start_date, end_date):
            print(txts.end_date_invalid)
            continue
        break
    cars, car_status = RentalService.get_car_status_for_dates(start_date, end_date)
    available_cars = [car for car in cars if car_status.get(car[0], 'available') == 'available']
    print(txts.cars_for_dates)
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
        print(txts.no_cars_available)
        return
    car_id = input(txts.car_id_prompt).strip()
    try:
        car_id = int(car_id)
    except ValueError:
        print(txts.invalid_car_id)
        return
    if car_id not in [car[0] for car in available_cars]:
        print(txts.not_available)
        return
    extra_charges = 0.0
    total_fee = RentalService.calculate_rental_fee(car_id, start_date, end_date, extra_charges)
    print(txts.total_fee.format(fee=total_fee))
    confirm = input(txts.confirm_booking).strip().lower()
    if confirm == 'yes':
        success = RentalService.book_rental(user_id=user.id, car_id=car_id, start_date=start_date, end_date=end_date, total_fee=total_fee)
        if success:
            print(txts.booked_success)
        else:
            print(txts.booked_fail)
    else:
        print(txts.booking_cancelled)

def customer_booking_menu(user):
    while True:
        print(txts.booking_menu)
        print(txts.view_bookings)
        print(txts.cancel_booking)
        print(txts.update_booking)
        print(txts.back_to_customer)
        choice = input(txts.booking_choice).strip()
        if choice == '1':
            bookings = RentalService.get_bookings_for_user(user.id)
            if not bookings:
                print(txts.no_bookings)
            else:
                for booking in bookings:
                    print(f"ID: {booking[0]}, Car ID: {booking[2]}, Start: {booking[3]}, End: {booking[4]}, Fee: {booking[5]}, Status: {booking[6]}")
        elif choice == '2':
            rental_id = input(txts.booking_id_cancel).strip()
            try:
                rental_id = int(rental_id)
                success = RentalService.cancel_booking(rental_id, user.id)
                if success:
                    print(txts.cancel_success)
                else:
                    print(txts.cancel_fail)
            except ValueError:
                print(txts.invalid_booking_id)
        elif choice == '3':
            rental_id = input(txts.booking_id_update).strip()
            try:
                rental_id = int(rental_id)
                while True:
                    start_date = input(txts.new_start_date).strip()
                    if not Utils.is_start_date_today_or_future(start_date):
                        print(txts.start_date_invalid)
                        continue
                    end_date = input(txts.new_end_date).strip()
                    if not Utils.is_end_date_valid(start_date, end_date):
                        print(txts.end_date_invalid)
                        continue
                    break
                car_id = input(txts.new_car_id).strip()
                car_id = int(car_id) if car_id else None
                success = RentalService.update_booking(rental_id, user.id, start_date, end_date, car_id)
                if success:
                    print(txts.update_success)
                else:
                    print(txts.update_fail)
            except ValueError:
                print(txts.invalid_input)
        elif choice == '4':
            break
        else:
            print(txts.invalid_choice)
