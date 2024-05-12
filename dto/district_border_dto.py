from dataclasses import dataclass

from dto.district_dto import DistrictDTO


@dataclass
class DistrictBorderDTO:
    district: DistrictDTO
    border: []
