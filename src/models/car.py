from dataclasses import dataclass

@dataclass
class Car:
    make: str
    model: str
    year: int
    mileage: int
    available_now: int
    min_rent_period: int
    max_rent_period: int