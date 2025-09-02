import sqlite3
from datetime import datetime
from typing import List, Tuple
from database import get_connection
from dataclasses import dataclass

@dataclass
class Rental:
    user_id: int
    car_id: int
    start_date: str
    end_date: str
    total_fee: float
    status: str = 'pending'