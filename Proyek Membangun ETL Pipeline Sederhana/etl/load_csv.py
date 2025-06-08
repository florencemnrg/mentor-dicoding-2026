def save_to_csv(df, csv_path='products.csv'):
    df.to_csv(csv_path, index=False)
    print(f"Data saved to CSV file: {csv_path}")
