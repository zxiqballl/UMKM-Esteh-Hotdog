import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "umkm_esteh_hotdog")

SECRET_KEY = os.getenv("APP_SECRET", "rahasia123")
