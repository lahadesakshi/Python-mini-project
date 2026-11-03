
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO expenses
            (title, amount, category, date)
            VALUES (?, ?, ?, ?)""",
            (title, amount, category, date)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()

    # Total Income
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE LOWER(TRIM(category)) = 'income'
    """)
    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE LOWER(TRIM(category)) IN
        ('expense', 'food', 'travel', 'shopping',
         'education', 'other')
    """)
    total_expense = cursor.fetchone()[0]

    # Total Balance
    total_balance = total_income - total_expense

    conn.close()

    return render_template(
        'index.html',
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        total_balance=total_balance
    )


if __name__ == '__main__':
    create_table()
    app.run(debug=True)


    