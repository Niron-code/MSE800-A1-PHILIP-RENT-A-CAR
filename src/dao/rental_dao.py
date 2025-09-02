from models.rental import Rental
from database import get_connection
from typing import List, Optional, Tuple
from datetime import datetime

class RentalDAO:
    @staticmethod
    def book_rental(rental: Rental) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rentals (user_id, car_id, start_date, end_date, total_fee, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (rental.user_id, rental.car_id, rental.start_date, rental.end_date, rental.total_fee, rental.status))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def calculate_rental_fee(car_id: int, start_date: str, end_date: str, extra_charges: float = 0.0) -> float:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT min_rent_period, max_rent_period FROM cars WHERE id=?', (car_id,))
        car = cursor.fetchone()
        days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        base_fee = 50 * days
        total_fee = base_fee + extra_charges
        conn.close()
        return total_fee

    @staticmethod
    def get_pending_rentals() -> List[Tuple]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rentals WHERE status="pending"')
        rentals = cursor.fetchall()
        conn.close()
        return rentals

    @staticmethod
    def update_rental_status(rental_id: int, status: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE rentals SET status=? WHERE id=?', (status, rental_id))
        conn.commit()
        conn.close()
        return True
