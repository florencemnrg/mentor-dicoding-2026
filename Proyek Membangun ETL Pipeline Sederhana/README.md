# Proyek Membangun ETL Pipeline Sederhana

## Deskripsi
Proyek ini merupakan implementasi pipeline ETL (Extract, Transform, Load) sederhana untuk mengambil data produk dari website, membersihkan dan mengubah data, serta menyimpannya ke database PostgreSQL dan file CSV.  
Tujuannya adalah membangun pipeline yang terstruktur dengan pengujian unit yang memadai dan mekanisme retry saat menyimpan data.

---

## Struktur Folder

Proyek Membangun ETL Pipeline Sederhana/
├── etl/
│ ├── __init__.py
│ ├── extract.py # Fungsi extract data dari web
│ ├── transform.py # Fungsi transformasi data
│ └── load.py # Fungsi load data ke DB dengan retry dan simpan CSV
│
├── tests/
│ ├── __init__.py
│ ├── test_extract.py # Unit test untuk extract.py
│ ├── test_transform.py# Unit test untuk transform.py
│ ├── test_load.py # Unit test untuk load.py
│ └── hasil_test.txt # Hasil test tersimpan
│
├── main.py # Script utama untuk menjalankan ETL pipeline secara utuh
├── products.csv # Saved result in csv format
├── requirements.txt # Daftar dependency Python
├── submission.txt # Instruksi menjalankan proyek
└── README.md # Dokumentasi proyek ini


---

## Cara Menjalankan ETL Pipeline

1. Pastikan Python sudah terinstall (disarankan versi 3.8+).  
2. Install dependencies dengan perintah:

   ```bash
   pip install -r requirements.txt

3. Pastikan PostgreSQL sudah berjalan dan konfigurasi koneksi di main.py sudah sesuai:

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/ecommercedb')

4. Jalankan pipeline dengan perintah:
python main.py

Proses ini akan:

Extract data dari website (50 halaman produk).

Transform data sesuai aturan (konversi harga, pembersihan rating, filtering).

Load data ke tabel fashion_studio di PostgreSQL dan simpan file CSV di table products.csv.

