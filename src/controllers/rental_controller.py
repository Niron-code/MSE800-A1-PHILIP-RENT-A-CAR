from services.rental_service import RentalService

def rental_approval_menu():
    print("\nPending Rental Requests:")
    pending = RentalService.get_pending_rentals()
    if not pending:
        print("No pending rentals.")
        return
    for rental in pending:
        print(f"ID: {rental[0]}, User ID: {rental[1]}, Car ID: {rental[2]}, Start: {rental[3]}, End: {rental[4]}, Fee: {rental[6]}, Status: {rental[5]}")
    rental_id = input("Enter Rental ID to approve/reject (or press Enter to go back): ").strip()
    if not rental_id:
        return
    try:
        rental_id = int(rental_id)
    except ValueError:
        print("Invalid Rental ID.")
        return
    action = input("Approve or Reject? (a/r): ").strip().lower()
    if action == 'a':
        success = RentalService.update_rental_status(rental_id, 'approved')
        if success:
            print("Rental approved.")
        else:
            print("Failed to approve rental.")
    elif action == 'r':
        success = RentalService.update_rental_status(rental_id, 'rejected')
        if success:
            print("Rental rejected.")
        else:
            print("Failed to reject rental.")
    else:
        print("Invalid action.")

def book_rental_menu(user):
    print("\nEnter rental start date (YYYY-MM-DD): ")
    start_date = input().strip()
    print("Enter rental end date (YYYY-MM-DD): ")
    end_date = input().strip()
    cars, car_status = RentalService.get_car_status_for_dates(start_date, end_date)
    available_cars = [car for car in cars if car_status.get(car[0], 'available') == 'available']
    print("\nCars for selected dates:")
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
        print("No cars available for booking for the selected dates.")
        return
    car_id = input("Enter Car ID to book (only AVAILABLE): ").strip()
    try:
        car_id = int(car_id)
    except ValueError:
        print("Invalid Car ID.")
        return
    if car_id not in [car[0] for car in available_cars]:
        print("Selected car is not available for booking.")
        return
    extra_charges = 0.0
    total_fee = RentalService.calculate_rental_fee(car_id, start_date, end_date, extra_charges)
    print(f"Total rental fee: ${total_fee}")
    confirm = input("Confirm booking? (yes/no): ").strip().lower()
    if confirm == 'yes':
        success = RentalService.book_rental(user_id=user.id, car_id=car_id, start_date=start_date, end_date=end_date, total_fee=total_fee)
        if success:
            print("Rental booked successfully! Pending approval.")
        else:
            print("Failed to book rental.")
    else:
        print("Booking cancelled.")

def customer_booking_menu(user):
    while True:
        print("\nBooking Management Menu")
        print("1. View My Bookings")
        print("2. Cancel a Booking")
        print("3. Update a Booking")
        print("4. Back to Customer Menu")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            bookings = RentalService.get_bookings_for_user(user.id)
            if not bookings:
                print("No bookings found.")
            else:
                for booking in bookings:
                    print(f"ID: {booking[0]}, Car ID: {booking[2]}, Start: {booking[3]}, End: {booking[4]}, Fee: {booking[5]}, Status: {booking[6]}")
        elif choice == '2':
            rental_id = input("Enter Booking ID to cancel: ").strip()
            try:
                rental_id = int(rental_id)
                success = RentalService.cancel_booking(rental_id, user.id)
                if success:
                    print("Booking cancelled successfully.")
                else:
                    print("Failed to cancel booking or booking not found.")
            except ValueError:
                print("Invalid Booking ID.")
        elif choice == '3':
            rental_id = input("Enter Booking ID to update: ").strip()
            try:
                rental_id = int(rental_id)
                start_date = input("Enter new start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter new end date (YYYY-MM-DD): ").strip()
                car_id = input("Enter new Car ID (or press Enter to keep current): ").strip()
                car_id = int(car_id) if car_id else None
                success = RentalService.update_booking(rental_id, user.id, start_date, end_date, car_id)
                if success:
                    print("Booking updated successfully.")
                else:
                    print("Failed to update booking. Only pending bookings can be updated.")
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")
