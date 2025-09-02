from models.car import CarFactory
from dao.car_dao import CarDAO

class CarService:
    @staticmethod
    def add_car(make: str, model: str, year: int, mileage: int, available_now: int, 
                min_rent_period: int, max_rent_period: int, car_type: str) -> bool:
        """Add a new car to the database."""
        car = CarFactory.create_car(
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            available_now=available_now,
            min_rent_period=min_rent_period,
            max_rent_period=max_rent_period,
            car_type=car_type
        )
        if car:
            return CarDAO.add_car(car)
        return False

    @staticmethod
    def update_car(car_id: int, **kwargs) -> bool:
        """Update car details by car_id."""
        return CarDAO.update_car(car_id, **kwargs)

    @staticmethod
    def delete_car(car_id: int) -> bool:
        """Delete a car from the database."""
        return CarDAO.delete_car(car_id)

    @staticmethod
    def get_available_cars():
        """Return a list of available cars."""
        return CarDAO.get_available_cars()
