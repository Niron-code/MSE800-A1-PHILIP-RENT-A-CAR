"""
database.py

Handles SQLite database connection and schema initialization for the car rental system.
Defines functions to get a database connection and initialize tables for users, cars, and rentals.
"""

import sqlite3

class Database:
    """
    Handles SQLite database connection and schema initialization for the car rental system.
    Provides methods to get a database connection and initialize tables for users, cars, and rentals.
    """
    DB_NAME = 'car_rental_v1.db'

    @staticmethod
    def get_connection():
        """
        Returns a new SQLite database connection using the configured database name.
        """
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def init_db():
        """
        Initializes the database schema for users, cars, and rentals tables.
        Creates tables if they do not exist and inserts default admin and car records.
        """
        conn = Database.get_connection()
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('customer', 'admin')) NOT NULL
            )
        ''')
        # Cars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                mileage INTEGER NOT NULL,
                available_now INTEGER NOT NULL,
                min_rent_period INTEGER NOT NULL,
                max_rent_period INTEGER NOT NULL,
                car_type TEXT CHECK(car_type IN ('luxury', 'sedan', 'suv')) NOT NULL,
                base_rate_per_day REAL NOT NULL
            )
        ''')
        # Rentals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                car_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT CHECK(status IN ('pending', 'approved', 'rejected', 'cancelled')) NOT NULL DEFAULT 'pending',
                total_fee REAL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(car_id) REFERENCES cars(id)
            )
        ''')
        # Insert default admin if not exists
        cursor.execute('SELECT * FROM users WHERE username=? AND role=?', ('admin', 'admin'))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', ('admin', 'philip.car.rental@gmail.com', 'admin123', 'admin'))
        # Insert or update 3 default cars
        default_cars = [
            ('Mercedes-Benz', 'S-Class', 2025, 1500, 1, 2, 10, 'luxury', 200.0),
            ('Toyota', 'RAV4', 2024, 5000, 1, 3, 14, 'suv', 150.0), 
            ('Honda', 'Accord', 2023, 8000, 1, 4, 15, 'sedan', 100.0)
        ]
        for make, model, year, mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day in default_cars:
            cursor.execute('''SELECT id FROM cars WHERE make=? AND model=? AND year=?''', (make, model, year))
            car = cursor.fetchone()
            if car:
                cursor.execute('''UPDATE cars SET mileage=?, available_now=?, min_rent_period=?, max_rent_period=?, car_type=?, base_rate_per_day=? WHERE id=?''',
                    (mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day, car[0]))
            else:
                cursor.execute('''INSERT INTO cars (make, model, year, mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (make, model, year, mileage, available_now, min_rent_period, max_rent_period, car_type, base_rate_per_day))
        conn.commit()
        conn.close()