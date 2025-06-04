# Data Analysis Dashboard Project

This project contains an interactive dashboard for e-commerce data analysis using Streamlit.  
It includes features such as revenue analysis by city, product popularity, order trends over time, and more.

---

## Setup Instructions

### 1. Setup Virtual Environment

It's recommended to use a virtual environment to manage dependencies without affecting your global Python setup.

- Create virtual environment (using `.venv` as example):

  ```bash
  python -m venv .venv
  ```

- Activate virtual environment:

On Windows (PowerShell):
  ```bash
 .\.venv\Scripts\Activate.ps1
  ```

### 2. Install Required Libraries
To install required Python libraries, use the provided requirements.txt file:
  ```bash
  pip install -r requirements.txt
  ```

This is preferred over manual installations to ensure consistent dependencies.

3. Running the Dashboard
Make sure your data files (e.g., order_df.csv) are placed in the correct folder (e.g., dashboard folder).

Run the Streamlit dashboard script with:

  ```bash
  streamlit run dashboard/dashboard.py
  ```

Project Structure

  ```bash
    project-root/
    │
    ├── dashboard/
    │   ├── dashboard.py          # Main Streamlit app
    │   ├── order_df.csv          # Data for dashboard
    │
    ├── dashboard/E-commerce-public-dataset   #Dataset
    ├── requirements.txt         # Python dependencies
    ├── url.txt                   # Important url text
    ├── proyek_analisis_data.ipynb          # Notebook 
    └── README.md                          # This file

  ```

### Notes
This project uses Streamlit for interactive data visualization.

Make sure to activate your virtual environment before running the dashboard.

Modify filter options and data paths in dashboard.py as needed for your data setup.

