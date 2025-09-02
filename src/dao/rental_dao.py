from models.rental import Rental
from database import get_connection
from typing import List, Optional, Tuple
from datetime import datetime
from models.car import CarFactory, LuxuryCar, SedanCar, SUVCar

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
        cursor.execute('SELECT make, model, year, mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day FROM cars WHERE id=?', (car_id,))
        car_row = cursor.fetchone()
        if not car_row:
            conn.close()
            return 0.0
        days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        if days <= 0:
            conn.close()
            return 0.0
        make, model, year, mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day = car_row
        # Create car object using factory
        car = CarFactory.create_car(
            car_type=car_type,
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            available_now=available_now,
            min_rent_period=min_rent_period,
            max_rent_period=max_rent_period
        )
        if car:
            fee = car.calculate_rate(days) + extra_charges
        else:
            fee = base_rate_per_day * days + extra_charges
        conn.close()
        return fee

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
