import sqlite3

DB_NAME = 'car_rental_v1.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
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
            max_rent_period INTEGER NOT NULL
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
            status TEXT CHECK(status IN ('pending', 'approved', 'rejected')) NOT NULL DEFAULT 'pending',
            total_fee REAL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(car_id) REFERENCES cars(id)
        )
    ''')
    conn.commit()
    conn.close()