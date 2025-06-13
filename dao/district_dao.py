from dto.district_dto import DistrictDTO
from database.mysql_db import get_mysql_connection

con = get_mysql_connection()


def find_all():
    cursor = con.cursor()
    cursor.execute("select * from district_journal")

    result = []
    for data in cursor.fetchall():
        result.append(DistrictDTO(data[0], data[1]))

    return result


def find_by_district_id(district_id: int):
    cursor = con.cursor(prepared=True)
    cursor.execute("select * from district_border where district_id = ?", (district_id,))

    result = []
    for data in cursor.fetchall():
        result.append([data[2], data[3]])

    return result
