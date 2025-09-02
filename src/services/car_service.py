from models.car import Car

class CarService:
    @staticmethod
    def add_car(make: str, model: str, year: int, mileage: int, available_now: int, min_rent_period: int, max_rent_period: int) -> bool:
        """Add a new car to the database."""
        return Car.add(make, model, year, mileage, available_now, min_rent_period, max_rent_period)

    @staticmethod
    def update_car(car_id: int, **kwargs) -> bool:
        """Update car details by car_id."""
        return Car.update(car_id, **kwargs)

    @staticmethod
    def delete_car(car_id: int) -> bool:
        """Delete a car from the database."""
        return Car.delete(car_id)

    @staticmethod
    def get_available_cars():
        """Return a list of available cars."""
        return Car.get_available()
