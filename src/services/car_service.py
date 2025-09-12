"""
car_service.py

Service layer for car-related business logic in the car rental system.
Provides methods to add, update, delete, and retrieve cars by interacting with the DAO and model layers.
"""

from models.car import CarFactory
from dao.car_dao import CarDAO

class CarService:
    """
    Service class for car management operations.
    Handles business logic and delegates database operations to CarDAO.
    """
    @staticmethod
    def add_car(make: str, model: str, year: int, mileage: int, available_now: int, 
                min_rent_period: int, max_rent_period: int, car_type: str) -> bool:
        """
        Add a new car to the database.
        Returns True if the operation is successful, False otherwise.
        """
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
        """
        Update car details by car_id.
        Accepts keyword arguments for fields to update.
        Returns True if the operation is successful.
        """
        return CarDAO.update_car(car_id, **kwargs)

    @staticmethod
    def delete_car(car_id: int) -> bool:
        """
        Delete a car from the database by car_id.
        Returns True if the operation is successful.
        """
        return CarDAO.delete_car(car_id)

    @staticmethod
    def get_available_cars():
        """
        Return a list of available cars from the database.
        """
        return CarDAO.get_available_cars()
