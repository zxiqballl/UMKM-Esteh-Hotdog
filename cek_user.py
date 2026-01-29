import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect("database/database.db")
c = conn.cursor()

c.execute("SELECT password FROM users WHERE email=?", ("admin@umkm.com",))
data = c.fetchone()

if data:
    print("CHECK 123456:", check_password_hash(data[0], "123456"))
    print("CHECK salah :", check_password_hash(data[0], "salah"))
else:
    print("USER TIDAK ADA")

conn.close()
