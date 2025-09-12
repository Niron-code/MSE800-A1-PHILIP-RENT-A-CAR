"""
rental_service.py

Service layer for rental-related business logic in the car rental system.
Provides methods to book rentals, calculate fees, update statuses, and manage bookings by interacting with the DAO and model layers.
"""

from models.rental import Rental
from dao.rental_dao import RentalDAO

class RentalService:
    """
    Service class for rental management operations.
    Handles business logic and delegates database operations to RentalDAO.
    """
    @staticmethod
    def book_rental(user_id: int, car_id: int, start_date: str, end_date: str, total_fee: float) -> bool:
        """
        Book a rental for a car.
        Returns True if the operation is successful, False otherwise.
        """
        rental = Rental(
            user_id=user_id,
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
            total_fee=total_fee,
            status='pending'
        )
        return RentalDAO.book_rental(rental)

    @staticmethod
    def calculate_rental_fee(car_id: int, start_date: str, end_date: str, extra_charges: float = 0.0) -> float:
        """
        Calculate the rental fee for a car between two dates, including any extra charges.
        Returns the calculated fee as a float.
        """
        return RentalDAO.calculate_rental_fee(car_id, start_date, end_date, extra_charges)

    @staticmethod
    def get_pending_rentals():
        """
        Return a list of pending rental requests from the database.
        """
        return RentalDAO.get_pending_rentals()

    @staticmethod
    def update_rental_status(rental_id: int, status: str) -> bool:
        """
        Update the status of a rental (approve/reject) by rental_id.
        Returns True if the operation is successful.
        """
        return RentalDAO.update_rental_status(rental_id, status)
    
    @staticmethod
    def get_available_cars_for_specific_dates(start_date: str, end_date: str):
        """
        Get a list of available cars for specific dates.
        Returns a list of car records.
        """
        return RentalDAO.get_available_cars_for_specific_dates(start_date, end_date)

    @staticmethod
    def get_car_status_for_dates(start_date, end_date):
        """
        Get the status of cars for specific dates.
        Returns a tuple of (cars, car_status_dict).
        """
        return RentalDAO.get_car_status_for_dates(start_date, end_date)

    @staticmethod
    def cancel_booking(rental_id: int, user_id: int) -> bool:
        """
        Cancel a booking for a user by rental_id.
        Returns True if the operation is successful, False otherwise.
        """
        return RentalDAO.cancel_booking(rental_id, user_id)

    @staticmethod
    def update_booking(rental_id: int, user_id: int, start_date: str, end_date: str, car_id: int = None) -> bool:
        """
        Update a booking for a user (dates or car).
        Returns True if the operation is successful, False otherwise.
        """
        return RentalDAO.update_booking(rental_id, user_id, start_date, end_date, car_id)

    @staticmethod
    def get_bookings_for_user(user_id: int):
        """
        Get all bookings for a user by user_id.
        Returns a list of booking records.
        """
        return RentalDAO.get_bookings_for_user(user_id)
