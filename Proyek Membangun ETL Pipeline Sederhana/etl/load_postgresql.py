import time
from sqlalchemy import create_engine

def save_to_postgresql_with_retry(df, engine, table_name, max_retries=5):
    attempt = 0
    delay = 1
    while attempt < max_retries:
        try:
            with engine.connect() as con:
                print("Connecting to database...")
                df.to_sql(table_name, con=con, if_exists='replace', index=False)
                print("Data saved successfully to database!")
                break
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("Max retries reached. Failed to save data.")
                raise
            else:
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2
