import os
import pg8000.dbapi
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Helper function to connect using your Supabase URL
def get_conn():
    url = urlparse(os.environ["DATABASE_URL"])
    return pg8000.dbapi.connect(
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        database=url.path[1:]
    )

def create_user(name):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (%s) RETURNING user_id;", (name,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    finally:
        conn.close()

def create_account(user_id, account_name):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (user_id, account_name) VALUES (%s, %s) RETURNING account_id;", (user_id, account_name))
        account_id = cursor.fetchone()[0]
        conn.commit()
        return account_id
    finally:
        conn.close()

def add_transaction(account_id, amount_cents, description, created_at):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (account_id, amount_cents, description, created_at) VALUES (%s, %s, %s, %s);",
            (account_id, amount_cents, description, created_at)
        )
        conn.commit()
    finally:
        conn.close()

def get_balance(account_id):
    try:
        conn = get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount_cents) FROM transactions WHERE account_id = %s;", (account_id,))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        finally:
            conn.close()
    except Exception:
        return 0