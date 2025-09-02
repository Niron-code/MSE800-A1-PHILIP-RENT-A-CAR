from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class Car(ABC):
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
        """Calculate the rental rate for the given number of days"""
        pass

@dataclass
class LuxuryCar(Car):
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="luxury",
            base_rate_per_day=200.0  # Higher base rate for luxury cars
        )
    
    def calculate_rate(self, days: int) -> float:
        # Luxury cars get more expensive for shorter rentals
        rate_multiplier = 1.5 if days < 7 else 1.2
        return self.base_rate_per_day * days * rate_multiplier

@dataclass
class SedanCar(Car):
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="sedan",
            base_rate_per_day=100.0  # Standard rate for sedans
        )
    
    def calculate_rate(self, days: int) -> float:
        # Sedans get cheaper for longer rentals
        rate_multiplier = 0.9 if days > 7 else 1.0
        return self.base_rate_per_day * days * rate_multiplier

@dataclass
class SUVCar(Car):
    def __init__(self, make: str, model: str, year: int, mileage: int, 
                 available_now: int, min_rent_period: int, max_rent_period: int):
        super().__init__(
            make=make, model=model, year=year, mileage=mileage,
            available_now=available_now, min_rent_period=min_rent_period,
            max_rent_period=max_rent_period, car_type="suv",
            base_rate_per_day=150.0  # Higher than sedan but lower than luxury
        )
    
    def calculate_rate(self, days: int) -> float:
        # SUVs have a balanced rate structure
        rate_multiplier = 1.2 if days < 3 else (0.9 if days > 7 else 1.0)
        return self.base_rate_per_day * days * rate_multiplier

class CarFactory:
    @staticmethod
    def create_car(car_type: str, make: str, model: str, year: int, mileage: int,
                   available_now: int, min_rent_period: int, max_rent_period: int) -> Optional[Car]:
        """
        Create a car of the specified type
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