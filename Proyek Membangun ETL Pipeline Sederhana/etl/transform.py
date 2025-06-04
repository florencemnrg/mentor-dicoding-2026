import re
import numpy as np
from datetime import datetime

def convert_price_to_rupiah(price_str, rate=16000):
    if not isinstance(price_str, str):
        return np.nan
    price_str = price_str.strip()
    if price_str.startswith('$'):
        try:
            value = float(price_str.replace('$', '').replace(',', ''))
            return value * rate
        except:
            return np.nan
    else:
        return np.nan

def clean_rating(rating_str):
    if not isinstance(rating_str, str):
        return np.nan
    invalid_keywords = ['invalid', 'not rated']
    if any(kw in rating_str.lower() for kw in invalid_keywords):
        return np.nan
    match = re.search(r'(\d+(\.\d+)?)', rating_str)
    if match:
        return float(match.group(1))
    return np.nan

def transform_data(df):
    dirty_patterns = {
        "Product Name": ["Unknown Product"],
        "Rating": ["Invalid Rating / 5", "Not Rated"],
        "Price": ["Price Unavailable"]
    }
    for col, invalids in dirty_patterns.items():
        df = df[~df[col].isin(invalids)]

    df['Price'] = df['Price'].apply(convert_price_to_rupiah)
    df = df.dropna(subset=['Price'])

    df['Rating'] = df['Rating'].apply(clean_rating)
    df = df.dropna(subset=['Rating'])
    df = df[df['Rating'] > 0]

    df['timestamp'] = datetime.now()
    df = df.drop_duplicates().reset_index(drop=True)

    return df
