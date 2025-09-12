"""
rental.py

Defines the Rental model for the car rental system.
Represents a rental transaction between a user and a car, including dates, fee, and status.
"""

from dataclasses import dataclass

@dataclass
class Rental:
    user_id: int
    car_id: int
    start_date: str
    end_date: str
    total_fee: float
    status: str = 'pending'