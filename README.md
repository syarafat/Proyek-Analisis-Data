# Bike Rental Analysis Dashboard 🚲✨

Dashboard ini menyajikan analisis komprehensif terkait pola penyewaan sepeda berdasarkan data yang diberikan. Menggunakan beberapa teknik visualisasi, serta RFM Analysis dan clustering manual, dashboard ini memberikan wawasan penting terkait faktor-faktor yang mempengaruhi penyewaan sepeda.

## Requirements
Pastikan Anda memiliki Python 3.9 atau versi yang lebih baru.

## Setup Environment

### Menggunakan Anaconda (Rekomendasi)
Jika menggunakan Anaconda, ikuti langkah-langkah berikut untuk membuat environment baru dan menginstal dependensi:

1. Buat environment baru:
    ```bash
    conda create --name bike-rental-analysis python=3.9
    ```
2. Aktifkan environment:
    ```bash
    conda activate bike-rental-analysis
    ```
3. Install semua dependensi yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

### Menggunakan Shell/Terminal (Virtual Environment)
Jika tidak menggunakan Anaconda, Anda bisa menggunakan virtual environment standar Python:

1. Buat virtual environment baru:
    ```bash
    python -m venv bike-rental-env
    ```
2. Aktifkan virtual environment:
    - Untuk **Linux** atau **MacOS**:
        ```bash
        source bike-rental-env/bin/activate
        ```
    - Untuk **Windows**:
        ```bash
        .venv\Scripts\activate
        ```
3. Install semua dependensi:
    ```bash
    pip install -r requirements.txt
    ```

## Menjalankan Aplikasi Streamlit

Setelah environment siap, jalankan aplikasi Streamlit dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
