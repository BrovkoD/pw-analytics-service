from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class WeatherFactorDTO:
    id: int
    time: datetime
    value: Decimal()
