import os
import logging
import pg8000.dbapi
import db_module
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Configure logging to write to ledger.log
logging.basicConfig(
    filename="ledger.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def setup_database():
    logging.info("Setting up the database tables using schema.sql...")
    url = urlparse(os.environ.get("DATABASE_URL"))
    
    with open("schema.sql", "r") as f:
        schema_sql = f.read()
        
    try:
        conn = pg8000.dbapi.connect(
            user=url.username, password=url.password,
            host=url.hostname, port=url.port, database=url.path[1:]
        )
        try:
            cursor = conn.cursor()
            # pg8000 prefers running commands one by one
            for statement in schema_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
            logging.info("Database setup complete.")
        finally:
            conn.close()
    except Exception as e:
        logging.error(f"Exception during database setup: {e}", exc_info=True)
        raise

def run_tests():
    try:
        setup_database()
        
        logging.info("Creating a user...")
        user_id = db_module.create_user("Charlie")
        logging.info(f"Created user with ID: {user_id}")
        
        logging.info("Creating an account...")
        account_id = db_module.create_account(user_id, "Charlie Checking")
        logging.info(f"Created account with ID: {account_id}")
        
        logging.info("Adding transactions...")
        db_module.add_transaction(account_id, 1000, "Refund credit", "2026-07-10")
        db_module.add_transaction(account_id, 500, "Dividends", "2026-07-10")
        db_module.add_transaction(account_id, -200, "Coffee purchase", "2026-07-10")
        logging.info("Added 3 transactions.")
        
        logging.info("Calculating balance...")
        balance = db_module.get_balance(account_id)
        logging.info(f"Account Balance (in cents): {balance}")
        expected_balance = 1000 + 500 - 200
        assert balance == expected_balance, f"Expected {expected_balance}, but got {balance}"
        
        sql_injection_input = "' OR '1'='1"
        logging.info(f"Testing SQL injection safety with input: {sql_injection_input}")
        injection_balance = db_module.get_balance(sql_injection_input)
        logging.info(f"SQL injection test returned balance: {injection_balance}")
        assert injection_balance == 0, f"Expected 0 on SQL injection test, but got {injection_balance}"
        logging.info("SQL injection test passed safely.")
        
        logging.info("All tests completed successfully!")
    except Exception as e:
        logging.error(f"Exception during test run: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    run_tests()