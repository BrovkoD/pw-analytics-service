from datetime import datetime

import pandas as pd

from dto.weather_factor_dto import WeatherFactorDTO
from database.mysql_db import get_mysql_connection

con = get_mysql_connection()


def get_time_of_last():
    cursor = con.cursor()
    cursor.execute("select time from weather_factor_journal order by time desc limit 1")

    result = cursor.fetchone()

    return datetime.min if (result is None) else result[0]


def save(data: WeatherFactorDTO):
    cursor = con.cursor(prepared=True)
    cursor.execute("insert into weather_factor_journal (time, value) values(?, ?)", (data.time, data.value))

    con.commit()


def get_month_avg():
    cursor = con.cursor()
    cursor.execute("select date_format(time,'%Y-%m-01'), avg(value)"
                   " from weather_factor_journal"
                   " where time < '2021-12-01'"
                   " group by date_format(time,'%Y-%m-01')")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], float(data[1])])

    return pd.DataFrame(result, columns=["ds", "y"])


def get_day_avg():
    cursor = con.cursor()
    cursor.execute("select date(time), avg(value)"
                   " from weather_factor_journal"
                   " where time < '2021-12-01'"
                   " group by date(time)")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], float(data[1])])

    return pd.DataFrame(result, columns=["ds", "y"])


def get_3h():
    cursor = con.cursor()
    cursor.execute("select time, value"
                   " from weather_factor_journal"
                   " where time < '2021-12-01'")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], float(data[1])])

    return pd.DataFrame(result, columns=["ds", "y"])
