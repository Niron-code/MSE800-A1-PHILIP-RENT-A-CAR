from models.rental import Rental
from dao.rental_dao import RentalDAO

class RentalService:
    @staticmethod
    def book_rental(user_id: int, car_id: int, start_date: str, end_date: str, total_fee: float) -> bool:
        """Book a rental for a car."""
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
        """Calculate the rental fee for a car."""
        return RentalDAO.calculate_rental_fee(car_id, start_date, end_date, extra_charges)

    @staticmethod
    def get_pending_rentals():
        """Return a list of pending rental requests."""
        return RentalDAO.get_pending_rentals()

    @staticmethod
    def update_rental_status(rental_id: int, status: str) -> bool:
        """Update the status of a rental (approve/reject)."""
        return RentalDAO.update_rental_status(rental_id, status)
    
    @staticmethod
    def get_available_cars_for_specific_dates(start_date: str, end_date: str):
        """Get a list of available cars for specific dates."""
        return RentalDAO.get_available_cars_for_specific_dates(start_date, end_date)

    @staticmethod
    def get_car_status_for_dates(start_date, end_date):
        """Get the status of cars for specific dates."""
        return RentalDAO.get_car_status_for_dates(start_date, end_date)
