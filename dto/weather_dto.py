from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class WeatherDTO:
    id: int
    time: datetime
    temp: Decimal()
    pressure: Decimal()
    hum: Decimal()
