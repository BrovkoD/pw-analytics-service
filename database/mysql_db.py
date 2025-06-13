import threading
import configparser
from mysql.connector import connect, Error

mysql_con = None
threadLock = threading.Lock()

config = configparser.RawConfigParser()
config.read('resources/application.properties')


def get_mysql_connection():
    if mysql_con is None:
        threadLock.acquire()
        if mysql_con is None:
            init_connection()
            threadLock.release()

    return mysql_con


def init_connection():
    global mysql_con

    try:
        mysql_con = connect(
            host=config.get("database", "mysql.host"),
            database=config.get("database", "mysql.database"),
            user=config.get("database", "mysql.user"),
            password=config.get("database", "mysql.password")
        )
    except Error as e:
        print(e)
