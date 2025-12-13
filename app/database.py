import mysql.connector
from mysql.connector import pooling
from .config import Config


pool = None


def get_pool():
    global pool
    if pool is None:
        pool = pooling.MySQLConnectionPool(
            pool_name=Config.MYSQL_POOL_NAME,
            pool_size=Config.MYSQL_POOL_SIZE,
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            auth_plugin="mysql_native_password",
        )
    return pool


def get_connection():
    return get_pool().get_connection()


def get_cursor(dictionary=True):
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)
    return conn, cursor

