from services.car_service import CarService

def car_management_menu():
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
            car_types = {"1": "luxury", "2": "sedan", "3": "suv"}
            car_type = car_types.get(type_choice)
            if not car_type:
                print("Invalid car type selected!")
                continue
            success = CarService.add_car(
                make=make,
                model=model,
                year=year,
                mileage=mileage,
                available_now=1,
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
