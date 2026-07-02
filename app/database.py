import sqlite3
from datetime import datetime

DATABASE = "finance.db"

def initialise_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_transaction(user_id, amount, category):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (user_id, amount, category)
    VALUES (?, ?, ?)
    """, (user_id, amount, category))

    conn.commit()
    conn.close()

def get_latest_transaction(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, amount, category
    FROM transactions
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (user_id,))

    transaction = cursor.fetchone()

    conn.close()
    return transaction

def delete_transaction(transaction_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM transactions
    WHERE id = ?
    """, (transaction_id,))

    conn.commit()
    conn.close()

def get_month_summary(user_id, month, year):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, category
        FROM transactions
        WHERE user_id = ?
        AND strftime('%Y', created_at) = ?
        AND strftime('%m', created_at) = ?
    """, (user_id, str(year), f"{month:02d}"))

    rows = cursor.fetchall()
    income = {}
    expense = {}
    for amount, category in rows:
        if amount < 0:
            if category not in expense:
                expense[category] = 0
            expense[category] += abs(amount)
        elif amount > 0:
            if category not in income:
                income[category] = 0
            income[category] += amount
    conn.close()
    return (income, expense)

def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT user_id
        FROM transactions
    """)

    users = [row[0] for row in cursor.fetchall()]

    conn.close()
    return users

def clear_old():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    current_year = datetime.now().year

    cursor.execute("""
    DELETE FROM transactions
    WHERE CAST(strftime('%Y', transaction_date) AS INTEGER) < ?
    """, (current_year,))