from models.rental import Rental

class RentalService:
    @staticmethod
    def book_rental(user_id: int, car_id: int, start_date: str, end_date: str, total_fee: float) -> bool:
        """Book a rental for a car."""
        return Rental.book(user_id, car_id, start_date, end_date, total_fee)

    @staticmethod
    def calculate_rental_fee(car_id: int, start_date: str, end_date: str, extra_charges: float = 0.0) -> float:
        """Calculate the rental fee for a car."""
        return Rental.calculate_fee(car_id, start_date, end_date, extra_charges)

    @staticmethod
    def get_pending_rentals():
        """Return a list of pending rental requests."""
        return Rental.get_pending()

    @staticmethod
    def update_rental_status(rental_id: int, status: str) -> bool:
        """Update the status of a rental (approve/reject)."""
        return Rental.update_status(rental_id, status)
