import sqlite3
from werkzeug.security import generate_password_hash
import os

# pastikan folder database ada
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/database.db")
c = conn.cursor()

# ===== TABEL USERS =====
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# ===== TABEL STOK =====
c.execute("""
CREATE TABLE IF NOT EXISTS stok (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sku TEXT,
    qty INTEGER
)
""")

# hapus user lama (biar tidak dobel)
c.execute("DELETE FROM users")

# user admin
email = "admin@umkm.com"
password = generate_password_hash("123456")

c.execute(
    "INSERT INTO users (email, password) VALUES (?, ?)",
    (email, password)
)

conn.commit()
conn.close()

print("DATABASE BERHASIL DIBUAT")
print("User admin dibuat:")
print("Email : admin@umkm.com")
print("Pass  : 123456")
