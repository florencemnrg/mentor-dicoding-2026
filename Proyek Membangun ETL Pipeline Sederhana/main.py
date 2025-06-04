import pandas as pd
from sqlalchemy import create_engine
from etl.extract import extract_all_pages
from etl.transform import transform_data
from etl.load import save_data_with_retry

def main():
    base_url = "https://fashion-studio.dicoding.dev/"
    print("Starting ETL process...")

    extracted_df = extract_all_pages(base_url, 50)
    print(f"Extracted {len(extracted_df)} rows")

    transformed_df = transform_data(extracted_df)
    print(f"Transformed {len(transformed_df)} rows")

    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/ecommercedb')
    save_data_with_retry(transformed_df, engine, 'fashion_studio')

if __name__ == "__main__":
    main()
