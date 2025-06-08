import pandas as pd
from sqlalchemy import create_engine
from etl.extract import extract_all_pages
from etl.transform import transform_data
from etl.load_csv import save_to_csv
from etl.load_postgresql import save_to_postgresql_with_retry

def main():
    base_url = "https://fashion-studio.dicoding.dev/"
    print("Starting ETL process...")

    extracted_df = extract_all_pages(base_url, 50)
    print(f"Extracted {len(extracted_df)} rows")

    transformed_df = transform_data(extracted_df)
    print(f"Transformed {len(transformed_df)} rows")

    # Save to CSV
    save_to_csv(transformed_df, csv_path='results/products.csv')

    # Save to PostgreSQL with retry
    engine = create_engine('your_postgres_connection_string')
    save_to_postgresql_with_retry(transformed_df, engine, table_name='your_table_name')

if __name__ == "__main__":
    main()
