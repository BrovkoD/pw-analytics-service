import pandas as pd

from dto.ragweed_dto import RagweedDTO
from database.mysql_db import get_mysql_connection

con = get_mysql_connection()


def find_all():
    cursor = con.cursor()
    cursor.execute("select rj.id, rj.latitude, rj.longitude, rs.size"
                   " from ragweed_journal rj"
                   " join ragweed_size rs on rj.size_id = rs.id")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], data[1], data[2], data[3]])

    return pd.DataFrame(result, columns=["id", "latitude", "longitude", "size"])



def find_where_district_is_null():
    cursor = con.cursor()
    cursor.execute("select * from ragweed_journal where district_id is null")

    result = []
    for data in cursor.fetchall():
        result.append(RagweedDTO(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

    return result


def count_ragweed_amount_per_district():
    cursor = con.cursor()
    cursor.execute("select d.id, d.name, count(r.id)"
                   " from ragweed_journal r"
                   " join district_journal d"
                   " where r.district_id is not null"
                   " and r.district_id = d.id"
                   " and r.active is true"
                   " group by district_id")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], data[1], data[2]])

    return pd.DataFrame(result, columns=["id", "territory", "amount"])


def count_ragweed_size_per_district():
    cursor = con.cursor()

    cursor.execute("select dj.name as district, count(rj.id) as amount, ifnull(rs.size, \"3-10 units\") as size"
                   " from ragweed_journal rj"
                   " join district_journal dj"
                   " left join ragweed_size rs on rs.id = rj.size_id"
                   " where rj.district_id = dj.id"
                   " and rj.district_id != 0"
                   " and rj.active is true"
                   " group by rj.district_id, ifnull(rs.size, \"3-10 units\")"
                   " order by rj.district_id, ifnull(rs.size, \"3-10 units\")")

    result = []
    for data in cursor.fetchall():
        result.append([data[0], data[1], data[2]])

    return pd.DataFrame(result, columns=["district", "amount", "size"])


def update(data: RagweedDTO):
    cursor = con.cursor(prepared=True)
    cursor.execute("update ragweed_journal set id = ?, latitude = ?, longitude = ?, size_id = ?, district_id = ?,"
                   " active = ?, deleted = ? where id = ?", (data.id, data.latitude, data.longitude,
                                                             data.size_id, data.district_id, data.active,
                                                             data.deleted, data.id))

    con.commit()
