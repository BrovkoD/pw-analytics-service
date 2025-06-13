from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RagweedDTO:
    id: int
    latitude: Decimal()
    longitude: Decimal()
    size_id: int
    district_id: int
    active: bool
    deleted: bool
