"""
car.py

Defines the Car model hierarchy for the car rental system.
Includes abstract base class Car and concrete subclasses for different car types (Luxury, Sedan, SUV).
Provides a CarFactory for creating car instances based on type.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class Car(ABC):
    """
    Abstract base class for car objects in the rental system.
    Defines common attributes and an abstract method for rate calculation.
    """
    make: str
    model: str
    year: int
    mileage: int
    available_now: int
    min_rent_period: int
    max_rent_period: int
    car_type: str
    base_rate_per_day: float

    @abstractmethod
    def calculate_rate(self, days: int) -> float:
        """
        Calculate the rental rate for the given number of days.
        Must be implemented by subclasses.
        """
        pass

@dataclass
class LuxuryCar(Car):
    """
    Concrete Car subclass for luxury cars with higher rates and custom rate logic.
    """
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="luxury",
            base_rate_per_day=200.0  # Higher base rate for luxury cars
        )
    
    def calculate_rate(self, days: int) -> float:
        """
        Calculate rate for luxury cars. More expensive for shorter rentals.
        """
        rate_multiplier = 1.5 if days < 7 else 1.2
        return self.base_rate_per_day * days * rate_multiplier

@dataclass
class SedanCar(Car):
    """
    Concrete Car subclass for sedan cars with standard rates and custom rate logic.
    """
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="sedan",
            base_rate_per_day=100.0  # Standard rate for sedans
        )
    
    def calculate_rate(self, days: int) -> float:
        """
        Calculate rate for sedans. Cheaper for longer rentals.
        """
        rate_multiplier = 0.9 if days > 7 else 1.0
        return self.base_rate_per_day * days * rate_multiplier

@dataclass
class SUVCar(Car):
    """
    Concrete Car subclass for SUV cars with balanced rates and custom rate logic.
    """
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="suv",
            base_rate_per_day=150.0  # Higher than sedan but lower than luxury
        )
    
    def calculate_rate(self, days: int) -> float:
        """
        Calculate rate for SUVs. Balanced rate structure.
        """
        rate_multiplier = 1.2 if days < 3 else (0.9 if days > 7 else 1.0)
        return self.base_rate_per_day * days * rate_multiplier

class CarFactory:
    """
    Factory class for creating car instances based on car_type string.
    """
    @staticmethod
    def create_car(car_type: str, make: str, model: str, year: int, mileage: int,
                   available_now: int, min_rent_period: int, max_rent_period: int) -> Optional[Car]:
        """
        Create a car of the specified type (luxury, sedan, suv).
        Returns an instance of the appropriate Car subclass or None if type is invalid.
        """
        car_types = {
            "luxury": LuxuryCar,
            "sedan": SedanCar,
            "suv": SUVCar
        }
        
        car_class = car_types.get(car_type.lower())
        if car_class:
            return car_class(
                make=make,
                model=model,
                year=year,
                mileage=mileage,
                available_now=available_now,
                min_rent_period=min_rent_period,
                max_rent_period=max_rent_period
            )
        return None