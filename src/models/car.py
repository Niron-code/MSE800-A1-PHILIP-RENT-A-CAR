import sqlite3
from typing import List, Tuple
from ..database import get_connection

class Car:
    def __init__(self, make: str, model: str, year: int, mileage: int, available_now: int, min_rent_period: int, max_rent_period: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available_now = available_now
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period

    @staticmethod
    def add(make: str, model: str, year: int, mileage: int, available_now: int, min_rent_period: int, max_rent_period: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cars (make, model, year, mileage, available_now, min_rent_period, max_rent_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (make, model, year, mileage, available_now, min_rent_period, max_rent_period))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def update(car_id: int, **kwargs) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        fields = ', '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        values.append(car_id)
        cursor.execute(f'UPDATE cars SET {fields} WHERE id=?', values)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(car_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id=?', (car_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_available() -> List[Tuple]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE available_now=1')
        cars = cursor.fetchall()
        conn.close()
        return cars
