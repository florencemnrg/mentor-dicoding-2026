import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('order_df.csv', parse_dates=['order_purchase_timestamp'])
    return df

df = load_data()

st.title("Interactive E-commerce Dashboard")

# Prepare filter widgets
states = df['customer_state'].dropna().unique().tolist()
states.insert(0, "All")

years = df['order_purchase_timestamp'].dt.year.unique().tolist()
years.sort()
years.insert(0, "All")

categories = df['product_category_name_english'].dropna().unique().tolist()
categories.insert(0, "All")

top_n = st.sidebar.selectbox("Number of top records to show", options=[5,10,20,50], index=1)
sort_order = st.sidebar.radio("Sort order", options=['Descending', 'Ascending'], index=0)

# --- TOP REVENUE ---
st.header("Top Revenue by City")

selected_state = st.selectbox("Filter by State", states)
selected_year = st.selectbox("Filter by Year", years)

df_rev = df.copy()

# Calculate revenue = price * 16000
df_rev['revenue'] = df_rev['price'] * 16000


if selected_state != "All":
    df_rev = df_rev[df_rev['customer_state'] == selected_state]
if selected_year != "All":
    df_rev = df_rev[df_rev['order_purchase_timestamp'].dt.year == selected_year]

rev_by_city = df_rev.groupby('customer_city')['revenue'].sum().reset_index()

rev_by_city = rev_by_city.sort_values(by='revenue', ascending=(sort_order=='Ascending')).head(top_n)

def format_rupiah(x):
    return f"Rp {x:,.0f},-"

rev_by_city['revenue in IDR'] = rev_by_city['revenue'].apply(format_rupiah)
rev_by_city.drop(columns=['revenue'], inplace=True)

# Reset index to start from 1 for display
rev_by_city_display = rev_by_city.reset_index(drop=True)
rev_by_city_display.index = rev_by_city_display.index + 1

st.dataframe(rev_by_city_display)

# --- TOP PRODUCTS ORDERED ---
st.header("Top Products Ordered")

selected_category = st.selectbox("Filter by Product Category", categories, key='category_filter')

df_prod = df.copy()
df_prod = df_prod.rename(columns={'product_category_name_english': 'product_name'})


if selected_category != "All":
    df_prod = df_prod[df_prod['product_category_name'] == selected_category]
if selected_state != "All":
    df_prod = df_prod[df_prod['customer_state'] == selected_state]

prod_count = df_prod.groupby('product_name')['order_id'].count().reset_index().rename(columns={'order_id':'order_count'})

prod_count = prod_count.sort_values(by='order_count', ascending=(sort_order=='Ascending')).head(top_n)
prod_count = prod_count.reset_index(drop=True)
st.dataframe(prod_count)

# --- EVOLUTION OF ORDERS ---
st.header("Evolution of Total Orders Over Time")

selected_city = st.selectbox("Filter by City", ["All"] + df['customer_city'].dropna().unique().tolist())

df_time = df.copy()
if selected_city != "All":
    df_time = df_time[df_time['customer_city'] == selected_city]

df_time['year_month'] = df_time['order_purchase_timestamp'].dt.to_period('M').astype(str)

orders_monthly = df_time.groupby('year_month').size()

fig, ax = plt.subplots(figsize=(10,4))
orders_monthly.plot(ax=ax, marker='o')
ax.set_ylabel("Number of Orders")
ax.set_xlabel("Year-Month")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- ORDERS BY DAY & TIME OF DAY ---
st.header("Total Orders by Day of Week and Time of Day")

df_time['day_of_week'] = df_time['order_purchase_timestamp'].dt.day_name()

def categorize_time(hour):
    if 4 <= hour < 8:
        return 'Dawn'
    elif 8 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    else:
        return 'Night'

df_time['hour'] = df_time['order_purchase_timestamp'].dt.hour
df_time['time_of_day'] = df_time['hour'].apply(categorize_time)

orders_by_day = df_time.groupby('day_of_week').size().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

orders_by_time = df_time.groupby('time_of_day').size().reindex(
    ['Dawn', 'Morning', 'Afternoon', 'Night']
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))

sns.barplot(x=orders_by_day.index, y=orders_by_day.values, ax=ax1)
ax1.set_title("Orders by Day of Week")
ax1.set_ylabel("Number of Orders")
ax1.set_xlabel("Day")

sns.barplot(x=orders_by_time.index, y=orders_by_time.values, ax=ax2)
ax2.set_title("Orders by Time of Day")
ax2.set_ylabel("Number of Orders")
ax2.set_xlabel("Time")

st.pyplot(fig)
