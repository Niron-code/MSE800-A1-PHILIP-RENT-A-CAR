from services.user_service import UserService
from database import init_db

init_db()

def main_menu():
    print("Welcome to Philip Rent-A-Car!")
    print("Are you an Admin or Customer?")
    print("1. Admin")
    print("2. Customer")
    print("0. Exit")
    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        admin_login()
    elif choice == '2':
        customer_menu()
    elif choice == '0':
        print("Exiting...")
        exit()
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
    from services.car_service import CarService
    from services.rental_service import RentalService
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
            old_pw = input("Enter current password: ").strip()
            new_pw = input("Enter new password: ").strip()
            success = UserService.change_admin_password(username, old_pw, new_pw)
            if success:
                print("Password changed successfully.")
            else:
                print("Incorrect current password.")
        elif choice == '4':
            print("Logging out...")
            main_menu()
            break
        else:
            print("Invalid choice. Try again.")

def rental_approval_menu():
    from services.rental_service import RentalService
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

def car_management_menu():
    from services.car_service import CarService
    
    while True:
        print("\nCar Management Menu")
        print("1. Add New Car")
        print("2. View All Cars")
        print("3. Update Car")
        print("4. Delete Car")
        print("5. Back to Admin Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            print("\nAdd New Car")
            make = input("Enter car make: ").strip()
            model = input("Enter car model: ").strip()
            year = int(input("Enter car year: ").strip())
            mileage = int(input("Enter car mileage: ").strip())
            min_rent = int(input("Enter minimum rental period (days): ").strip())
            max_rent = int(input("Enter maximum rental period (days): ").strip())
            
            print("\nSelect Car Type:")
            print("1. Luxury")
            print("2. Sedan")
            print("3. SUV")
            type_choice = input("Enter choice (1-3): ").strip()
            
            car_types = {
                "1": "luxury",
                "2": "sedan",
                "3": "suv"
            }
            
            car_type = car_types.get(type_choice)
            if not car_type:
                print("Invalid car type selected!")
                continue
                
            success = CarService.add_car(
                make=make,
                model=model,
                year=year,
                mileage=mileage,
                available_now=1,  # New cars are available by default
                min_rent_period=min_rent,
                max_rent_period=max_rent,
                car_type=car_type
            )
            
            if success:
                print("Car added successfully!")
            else:
                print("Failed to add car. Please try again.")
                
        elif choice == '2':
            print("\nAll Cars:")
            cars = CarService.get_available_cars()
            if not cars:
                print("No cars found.")
            else:
                for car in cars:
                    print(f"\nID: {car[0]}")
                    print(f"Make: {car[1]}")
                    print(f"Model: {car[2]}")
                    print(f"Year: {car[3]}")
                    print(f"Mileage: {car[4]}")
                    print(f"Available: {'Yes' if car[5] else 'No'}")
                    print(f"Rental Period: {car[6]}-{car[7]} days")
                    print("-" * 30)
                    
        elif choice == '3':
            car_id = input("\nEnter car ID to update: ").strip()
            try:
                car_id = int(car_id)
                print("Enter new values (leave blank to keep current value):")
                
                updates = {}
                make = input("Enter new make: ").strip()
                if make: updates['make'] = make
                
                model = input("Enter new model: ").strip()
                if model: updates['model'] = model
                
                year = input("Enter new year: ").strip()
                if year: updates['year'] = int(year)
                
                mileage = input("Enter new mileage: ").strip()
                if mileage: updates['mileage'] = int(mileage)
                
                available = input("Is car available? (1/0): ").strip()
                if available in ('0', '1'): updates['available_now'] = int(available)
                
                if updates:
                    if CarService.update_car(car_id, **updates):
                        print("Car updated successfully!")
                    else:
                        print("Failed to update car. Please try again.")
                else:
                    print("No updates provided.")
            except ValueError:
                print("Invalid car ID.")
                
        elif choice == '4':
            car_id = input("\nEnter car ID to delete: ").strip()
            try:
                car_id = int(car_id)
                confirm = input(f"Are you sure you want to delete car {car_id}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    if CarService.delete_car(car_id):
                        print("Car deleted successfully!")
                    else:
                        print("Failed to delete car. Please try again.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Invalid car ID.")
                
        elif choice == '5':
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

def customer_main_menu(user):
    from services.car_service import CarService
    from services.rental_service import RentalService
    while True:
        print(f"\nCustomer Menu - {user.username}")
        print("1. Book Rental")
        print("2. Logout")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            book_rental_menu(user)
        elif choice == '2':
            print("Logging out...")
            main_menu()
            break
        else:
            print("Invalid choice. Try again.")

def book_rental_menu(user):
    from services.rental_service import RentalService
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
    from services.rental_service import RentalService
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

def customer_login():
    print("\nCustomer Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = UserService.login_user(username, password)
    if user and user.role == 'customer':
        print(f"Welcome, {username}!")
        customer_main_menu(user)
    else:
        print("Invalid customer credentials.")
        customer_menu()

if __name__ == "__main__":
    main_menu()
