from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from werkzeug.security import check_password_hash
from datetime import datetime
import os
import config


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET', 'rahasia123')


def get_db():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

app.secret_key = config.SECRET_KEY



def verify_password(stored, provided):
    try:
        return check_password_hash(stored, provided)
    except Exception:
        return stored == provided


# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        try:
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE email=%s", (email,))
            row = c.fetchone()
            conn.close()

            if row and verify_password(row['password'], password):
                session['login'] = True
                return redirect(url_for('dashboard'))

        except Exception as e:
            print(e)

        return render_template(
            'auth/login.html',
            error='Email atau Password salah',
            current_year=datetime.now().year
        )

    return render_template('auth/login.html', current_year=datetime.now().year)


def try_query_table(c, table_names):
    for t in table_names:
        try:
            c.execute(f"SELECT 1 FROM {t} LIMIT 1")
            return t
        except Exception:
            continue
    return None


@app.route('/dashboard')
def dashboard():
    if not session.get('login'):
        return redirect(url_for('login'))

    totals = {
        'total_sales': 0,
        'total_orders': 0,
        'total_products': 0,
        'recent_transactions': []
    }

    try:
        conn = get_db()
        c = conn.cursor()

        t_products = try_query_table(c, ['products', 'menu', 'items'])
        if t_products:
            c.execute(f"SELECT COUNT(*) AS cnt FROM {t_products}")
            totals['total_products'] = c.fetchone()['cnt']

        t_orders = try_query_table(c, ['orders', 'sales', 'transactions'])
        if t_orders:
            c.execute(f"SELECT COUNT(*) AS cnt FROM {t_orders}")
            totals['total_orders'] = c.fetchone()['cnt']

            try:
                c.execute(f"SELECT SUM(total) AS s FROM {t_orders}")
                totals['total_sales'] = c.fetchone()['s'] or 0
            except Exception:
                pass

            try:
                c.execute(f"SELECT * FROM {t_orders} ORDER BY id DESC LIMIT 5")
                for r in c.fetchall():
                    totals['recent_transactions'].append({
                        'id': r.get('id'),
                        'customer': r.get('customer'),
                        'total': r.get('total'),
                        'time': r.get('created_at', '')
                    })
            except Exception:
                pass

        conn.close()

    except Exception as e:
        print(e)

    return render_template('dashboard/dashboard.html', **totals)

@app.route('/pos')
def pos():
    if not session.get('login'):
        return redirect(url_for('login'))

    products = []

    try:
        conn = get_db()
        c = conn.cursor()

        t = try_query_table(c, ['products', 'menu', 'items'])
        if t:
            c.execute(f"SELECT * FROM {t}")
            for r in c.fetchall():
                products.append({
                    'id': r.get('id'),
                    'name': r.get('name') or r.get('title') or r.get('product') or 'Produk',
                    'price': r.get('price') or r.get('harga') or 0
                })

        conn.close()

    except Exception as e:
        print(e)
        products = [
            {'id': 1, 'name': 'Es Teh Manis', 'price': 5000},
            {'id': 2, 'name': 'Hotdog Special', 'price': 15000}
        ]

    return render_template('kasir/pos.html', products=products)

@app.route('/stok', methods=['GET', 'POST'])
def stok():
    if not session.get('login'):
        return redirect(url_for('login'))

    conn = get_db()

    try:
        c = conn.cursor()

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'add':
                c.execute(
                    "INSERT INTO stok (name, sku, qty) VALUES (%s,%s,%s)",
                    (
                        request.form.get('name'),
                        request.form.get('sku'),
                        request.form.get('qty')
                    )
                )

            elif action == 'update':
                c.execute(
                    "UPDATE stok SET qty=%s WHERE id=%s",
                    (
                        request.form.get('qty'),
                        request.form.get('id')
                    )
                )

            elif action == 'delete':
                c.execute(
                    "DELETE FROM stok WHERE id=%s",
                    (request.form.get('id'),)
                )

            conn.commit()
            return redirect(url_for('stok'))

        c.execute("SELECT * FROM stok ORDER BY id DESC")
        rows = c.fetchall()

        return render_template('stok/stok.html', stok_items=rows)

    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
