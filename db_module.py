import sqlite3

def create_user(name):
    with sqlite3.connect("mini_ledger.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        return cursor.lastrowid

def create_account(user_id, account_name):
    with sqlite3.connect("mini_ledger.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (user_id, account_name) VALUES (?, ?)", (user_id, account_name))
        return cursor.lastrowid

def add_transaction(account_id, amount_cents, description, created_at):
    with sqlite3.connect("mini_ledger.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (account_id, amount_cents, description, created_at) VALUES (?, ?, ?, ?)",
            (account_id, amount_cents, description, created_at)
        )

def get_balance(account_id):
    try:
        with sqlite3.connect("mini_ledger.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount_cents) FROM transactions WHERE account_id = ?", (account_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
    except sqlite3.Error:
        return 0