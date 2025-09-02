import sqlite3
from datetime import datetime
from typing import List, Tuple
from ..database import get_connection

class Rental:
    def __init__(self, user_id: int, car_id: int, start_date: str, end_date: str, total_fee: float, status: str = 'pending'):
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_fee = total_fee
        self.status = status

    @staticmethod
    def book(user_id: int, car_id: int, start_date: str, end_date: str, total_fee: float) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rentals (user_id, car_id, start_date, end_date, total_fee)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, car_id, start_date, end_date, total_fee))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def calculate_fee(car_id: int, start_date: str, end_date: str, extra_charges: float = 0.0) -> float:
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
    def get_pending() -> List[Tuple]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rentals WHERE status="pending"')
        rentals = cursor.fetchall()
        conn.close()
        return rentals

    @staticmethod
    def update_status(rental_id: int, status: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE rentals SET status=? WHERE id=?', (status, rental_id))
        conn.commit()
        conn.close()
        return True
