from models.car import Car
from database import get_connection
from typing import List, Optional, Tuple

class CarDAO:
    @staticmethod
    def add_car(car: Car) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
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
    def delete_car(car_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id=?', (car_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_available_cars() -> List[Tuple]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE available_now=1')
        cars = cursor.fetchall()
        conn.close()
        return cars
