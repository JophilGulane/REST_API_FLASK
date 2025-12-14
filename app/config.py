import os


class Config:
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "admin")
    MYSQL_DB = os.environ.get("MYSQL_DB", "souls_db")
    MYSQL_POOL_NAME = "app_pool"
    MYSQL_POOL_SIZE = int(os.environ.get("MYSQL_POOL_SIZE", "5"))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jays-secret")
    API_USER = os.environ.get("API_USER", "admin")
    API_PASSWORD = os.environ.get("API_PASSWORD", "password")

 