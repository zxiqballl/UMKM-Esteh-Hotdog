from werkzeug.security import generate_password_hash
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
DB = os.path.abspath(DB)

new_pw = 'admin123'
hash = generate_password_hash(new_pw, method='scrypt')

print('DB:', DB)
print('Setting admin@umkm.com password to:', new_pw)

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("UPDATE users SET password=? WHERE email=?", (hash, 'admin@umkm.com'))
conn.commit()
print('Updated rows:', conn.total_changes)
conn.close()
