from datetime import datetime

from dto.weather_dto import WeatherDTO
from database.mysql_db import get_mysql_connection

con = get_mysql_connection()


def find_all_after_time(time: datetime):
    cursor = con.cursor(prepared=True)
    cursor.execute("select * from weather_journal where time > ?", (time,))

    result = []
    for data in cursor.fetchall():
        result.append(WeatherDTO(data[0], data[1], data[2], data[3], data[4]))

    return result
