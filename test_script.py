import sqlite3
import db_module

def setup_database():
    print("Setting up the database tables using schema.sql...")
    with open("schema.sql", "r") as f:
        schema_sql = f.read()
        
    with sqlite3.connect("mini_ledger.db") as conn:
        conn.executescript(schema_sql)
    print("Database setup complete.")

def run_tests():
    setup_database()
    
    print("\nCreating a user...")
    user_id = db_module.create_user("Charlie")
    print(f"Created user with ID: {user_id}")
    
    print("Creating an account...")
    account_id = db_module.create_account(user_id, "Charlie Checking")
    print(f"Created account with ID: {account_id}")
    
    print("Adding transactions...")
    db_module.add_transaction(account_id, 1000, "Refund credit", "2026-07-10")
    db_module.add_transaction(account_id, 500, "Dividends", "2026-07-10")
    db_module.add_transaction(account_id, -200, "Coffee purchase", "2026-07-10")
    print("Added 3 transactions.")
    
    print("Calculating balance...")
    balance = db_module.get_balance(account_id)
    print(f"Account Balance (in cents): {balance}")
    expected_balance = 1000 + 500 - 200
    assert balance == expected_balance, f"Expected {expected_balance}, but got {balance}"
    
    sql_injection_input = "' OR '1'='1"
    print(f"\nTesting SQL injection safety with input: {sql_injection_input}")
    injection_balance = db_module.get_balance(sql_injection_input)
    print(f"SQL injection test returned balance: {injection_balance}")
    assert injection_balance == 0, f"Expected 0 on SQL injection test, but got {injection_balance}"
    print("SQL injection test passed safely (returned 0 without crashing or dumping data).")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    run_tests()