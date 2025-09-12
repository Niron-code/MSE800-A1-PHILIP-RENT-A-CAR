
from services.car_service import CarService
from utils.text_utils import CarTexts as txts

def car_management_menu():
    while True:
        print(txts.menu_header)
        print(txts.add_new_car)
        print(txts.view_all_cars)
        print(txts.update_car)
        print(txts.delete_car)
        print(txts.back_to_admin)
        choice = input(txts.enter_choice).strip()
        if choice == '1':
            print(txts.add_new_car_header)
            make = input(txts.enter_make).strip()
            model = input(txts.enter_model).strip()
            year = int(input(txts.enter_year).strip())
            mileage = int(input(txts.enter_mileage).strip())
            min_rent = int(input(txts.enter_min_rent).strip())
            max_rent = int(input(txts.enter_max_rent).strip())
            print(txts.select_type)
            print(txts.type_luxury)
            print(txts.type_sedan)
            print(txts.type_suv)
            type_choice = input(txts.enter_type_choice).strip()
            car_types = {"1": "luxury", "2": "sedan", "3": "suv"}
            car_type = car_types.get(type_choice)
            if not car_type:
                print(txts.invalid_type)
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
                print(txts.add_success)
            else:
                print(txts.add_fail)
        elif choice == '2':
            print(txts.all_cars_header)
            cars = CarService.get_available_cars()
            if not cars:
                print(txts.no_cars)
            else:
                for car in cars:
                    print(f"\n{txts.id.format(id=car[0])}")
                    print(f"{txts.make.format(make=car[1])}")
                    print(f"{txts.model.format(model=car[2])}")
                    print(f"{txts.year.format(year=car[3])}")
                    print(f"{txts.mileage.format(mileage=car[4])}")
                    print(f"{txts.available.format(available='Yes' if car[5] else 'No')}")
                    print(f"{txts.rental_period.format(min=car[6], max=car[7])}")
                    print(txts.separator)
        elif choice == '3':
            car_id = input(txts.enter_update_id).strip()
            try:
                car_id = int(car_id)
                print(txts.new_values)
                updates = {}
                make = input(txts.enter_new_make).strip()
                if make: updates['make'] = make
                model = input(txts.enter_new_model).strip()
                if model: updates['model'] = model
                year = input(txts.enter_new_year).strip()
                if year: updates['year'] = int(year)
                mileage = input(txts.enter_new_mileage).strip()
                if mileage: updates['mileage'] = int(mileage)
                available = input(txts.is_available).strip()
                if available in ('0', '1'): updates['available_now'] = int(available)
                if updates:
                    if CarService.update_car(car_id, **updates):
                        print(txts.update_success)
                    else:
                        print(txts.update_fail)
                else:
                    print(txts.no_updates)
            except ValueError:
                print(txts.invalid_id)
        elif choice == '4':
            car_id = input(txts.enter_delete_id).strip()
            try:
                car_id = int(car_id)
                confirm = input(txts.confirm_delete.format(id=car_id)).strip().lower()
                if confirm == 'yes':
                    if CarService.delete_car(car_id):
                        print(txts.delete_success)
                    else:
                        print(txts.delete_fail)
                else:
                    print(txts.delete_cancel)
            except ValueError:
                print(txts.invalid_id)
        elif choice == '5':
            break
        else:
            print(txts.invalid_choice)
