"""
car_dao.py

Data Access Object (DAO) module for car-related database operations.
Provides methods to add, update, delete, and retrieve car records from the database.
Relies on the Car model and database connection utility.
"""

from models.car import Car
from database import Database
from typing import List,  Tuple

class CarDAO:  
    """
    DAO class for performing CRUD operations on car records in the database.
    """
    @staticmethod
    def add_car(car: Car) -> bool:
        """
        Inserts a new car record into the database.
        Returns True if the operation is successful.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('''
            INSERT INTO cars (
                make, model, year, mileage, available_now, 
                min_rent_period, max_rent_period, car_type, base_rate_per_day
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (car.make, car.model, car.year, car.mileage, car.available_now,
              car.min_rent_period, car.max_rent_period, car.car_type, car.base_rate_per_day))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def update_car(car_id: int, **kwargs) -> bool:
        """
        Updates fields of an existing car record by car_id.
        Accepts keyword arguments for fields to update.
        Returns True if the operation is successful.
        """
        conn, cursor = Database.get_conn_cursor()
        fields = ', '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        values.append(car_id)
        cursor.execute(f'UPDATE cars SET {fields} WHERE id=?', values)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete_car(car_id: int) -> bool:
        """
        Deletes a car record from the database by car_id.
        Returns True if the operation is successful.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('DELETE FROM cars WHERE id=?', (car_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_available_cars() -> List[Tuple]:
        """
        Retrieves all available cars from the database (where available_now=1).
        Returns a list of car records as tuples.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT * FROM cars WHERE available_now=1')
        cars = cursor.fetchall()
        conn.close()
        return cars
    
    @staticmethod
    def get_car_by_id(car_id: int) -> tuple:
        """
        Retrieves a car record from the database by car_id.
        Returns the car record as a tuple, or None if not found.
        """
        conn, cursor = Database.get_conn_cursor()
        cursor.execute('SELECT * FROM cars WHERE id=?', (car_id,))
        car = cursor.fetchone()
        conn.close()
        return car
