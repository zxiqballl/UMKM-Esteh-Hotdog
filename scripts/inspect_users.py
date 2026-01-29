import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
DB = os.path.abspath(DB)
print('DB:', DB)

try:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        print('\nSchema for users:')
        for col in c.execute("PRAGMA table_info(users)"):
            print(col)
        print('\nSample rows:')
        c.execute('SELECT * FROM users LIMIT 10')
        rows = c.fetchall()
        print('FOUND', len(rows))
        for r in rows:
            print(r)
    except Exception as e:
        print('QUERY ERROR:', e)
    conn.close()
except Exception as e:
    print('OPEN ERROR:', e)
