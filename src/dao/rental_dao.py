"""
rental_dao.py

Data Access Object (DAO) module for rental-related database operations.
Provides methods to book rentals, calculate fees, update statuses, and manage bookings.
Relies on the Rental and Car models and database connection utility.
"""

from models.rental import Rental
from database import Database
from typing import List,  Tuple
from datetime import datetime
from models.car import CarFactory

class RentalDAO:
    """
    DAO class for performing CRUD operations and business logic on rental records in the database.
    """
    @staticmethod
    def book_rental(rental: Rental) -> bool:
        """
        Inserts a new rental record into the database.
        Returns True if the operation is successful.
        """
        conn = Database.get_connection()
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
        """
        Calculates the total rental fee for a car between two dates, including any extra charges.
        Returns the calculated fee as a float.
        """
        conn = Database.get_connection()
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
        """
        Retrieves all pending rental requests from the database.
        Returns a list of rental records as tuples.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rentals WHERE status="pending"')
        rentals = cursor.fetchall()
        conn.close()
        return rentals

    @staticmethod
    def update_rental_status(rental_id: int, status: str) -> bool:
        """
        Updates the status of a rental record by rental_id.
        Returns True if the operation is successful.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE rentals SET status=? WHERE id=?', (status, rental_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_car_status_for_dates(start_date, end_date):
        """
        Retrieves all cars and their booking status for the given date range.
        Returns a tuple of (cars, car_status_dict).
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()
        car_status = {}
        for car in cars:
            car_id = car[0]
            cursor.execute('''
                SELECT status FROM rentals WHERE car_id=? AND status != "cancelled" AND NOT (
                    end_date < ? OR start_date > ?
                )
            ''', (car_id, start_date, end_date))
            result = cursor.fetchone()
            if result:
                car_status[car_id] = result[0]
            else:
                car_status[car_id] = 'available'
        conn.close()
        return cars, car_status

    @staticmethod
    def cancel_booking(rental_id: int, user_id: int) -> bool:
        """
        Cancels a booking if it belongs to the user and is not already cancelled.
        Returns True if the operation is successful, False otherwise.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM rentals WHERE id=? AND user_id=?', (rental_id, user_id))
        result = cursor.fetchone()
        if result and result[0] != 'cancelled':
            cursor.execute('UPDATE rentals SET status="cancelled" WHERE id=? AND user_id=?', (rental_id, user_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    @staticmethod
    def update_booking(rental_id: int, user_id: int, start_date: str, end_date: str, car_id: int = None) -> bool:
        """
        Updates booking dates or car if booking belongs to user and is pending.
        Returns True if the operation is successful, False otherwise.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM rentals WHERE id=? AND user_id=?', (rental_id, user_id))
        result = cursor.fetchone()
        if result and result[0] == 'pending':
            if car_id:
                cursor.execute('UPDATE rentals SET start_date=?, end_date=?, car_id=? WHERE id=? AND user_id=?', (start_date, end_date, car_id, rental_id, user_id))
            else:
                cursor.execute('UPDATE rentals SET start_date=?, end_date=? WHERE id=? AND user_id=?', (start_date, end_date, rental_id, user_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    @staticmethod
    def get_bookings_for_user(user_id: int) -> List[Tuple]:
        """
        Returns all bookings for a given user as a list of tuples.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rentals WHERE user_id=?', (user_id,))
        bookings = cursor.fetchall()
        conn.close()
        return bookings
