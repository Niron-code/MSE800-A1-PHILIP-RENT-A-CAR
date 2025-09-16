"""
car_controller.py

Controller module for car management operations in the car rental system.
Handles user interaction for adding, viewing, updating, and deleting cars.
Relies on CarService for business logic and database operations.
"""

from services.car_service import CarService


class CarController:
    """
    Controller class for car management operations in the car rental system.
    Provides static methods to interact with the car management menu and handle user actions.
    """
    @staticmethod
    def management_menu(texts):
        """
        Displays the car management menu and handles user input for car operations.
        """
        car_txts = texts['CarTexts']
        while True:
            print(car_txts['menu_header'])
            print(car_txts['add_new_car'])
            print(car_txts['view_all_cars'])
            print(car_txts['update_car'])
            print(car_txts['delete_car'])
            print(car_txts['back_to_admin'])
            choice = input(car_txts['enter_choice']).strip()
            if choice == '1':
                # Add a new car
                print(car_txts['add_new_car_header'])
                make = input(car_txts['enter_make']).strip()
                model = input(car_txts['enter_model']).strip()
                year = int(input(car_txts['enter_year']).strip())
                mileage = int(input(car_txts['enter_mileage']).strip())
                min_rent = int(input(car_txts['enter_min_rent']).strip())
                max_rent = int(input(car_txts['enter_max_rent']).strip())
                print(car_txts['select_type'])
                print(car_txts['type_luxury'])
                print(car_txts['type_sedan'])
                print(car_txts['type_suv'])
                type_choice = input(car_txts['enter_type_choice']).strip()
                car_types = {"1": "luxury", "2": "sedan", "3": "suv"}
                car_type = car_types.get(type_choice)
                if not car_type:
                    print(car_txts['invalid_type'])
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
                    print(car_txts['add_success'])
                else:
                    print(car_txts['add_fail'])
            elif choice == '2':
                # View all available cars
                print(car_txts['all_cars_header'])
                cars = CarService.get_available_cars()
                if not cars:
                    print(car_txts['no_cars'])
                else:
                    for car in cars:
                        print(f"\n{car_txts['id'].format(id=car[0])}")
                        print(f"{car_txts['make'].format(make=car[1])}")
                        print(f"{car_txts['model'].format(model=car[2])}")
                        print(f"{car_txts['year'].format(year=car[3])}")
                        print(f"{car_txts['mileage'].format(mileage=car[4])}")
                        print(f"{car_txts['available'].format(available='Yes' if car[5] else 'No')}")
                        print(f"{car_txts['rental_period'].format(min=car[6], max=car[7])}")
                        print(car_txts['separator'])
            elif choice == '3':
                # Update car details
                car_id = input(car_txts['enter_update_id']).strip()
                try:
                    car_id = int(car_id)
                    print(car_txts['new_values'])
                    updates = {}
                    make = input(car_txts['enter_new_make']).strip()
                    if make: updates['make'] = make
                    model = input(car_txts['enter_new_model']).strip()
                    if model: updates['model'] = model
                    year = input(car_txts['enter_new_year']).strip()
                    if year: updates['year'] = int(year)
                    mileage = input(car_txts['enter_new_mileage']).strip()
                    if mileage: updates['mileage'] = int(mileage)
                    available = input(car_txts['is_available']).strip()
                    if available in ('0', '1'): updates['available_now'] = int(available)
                    if updates:
                        if CarService.update_car(car_id, **updates):
                            print(car_txts['update_success'])
                        else:
                            print(car_txts['update_fail'])
                    else:
                        print(car_txts['no_updates'])
                except ValueError:
                    print(car_txts['invalid_id'])
            elif choice == '4':
                # Delete a car
                car_id = input(car_txts['enter_delete_id']).strip()
                try:
                    car_id = int(car_id)
                    confirm = input(car_txts['confirm_delete'].format(id=car_id)).strip().lower()
                    if confirm == 'yes':
                        if CarService.delete_car(car_id):
                            print(car_txts['delete_success'])
                        else:
                            print(car_txts['delete_fail'])
                    else:
                        print(car_txts['delete_cancel'])
                except ValueError:
                    print(car_txts['invalid_id'])
            elif choice == '5':
                # Return to previous menu
                break
            else:
                print(car_txts['invalid_choice'])
