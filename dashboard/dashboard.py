import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan halaman
st.set_page_config(
    page_title="Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Fungsi untuk load data dengan cache
@st.cache_data
def load_data():
    df = pd.read_csv('data/day.csv')
    
    # Correct the mapping of season to season_name
    season_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    df['season_name'] = df['season'].map(season_mapping)
    
    # Map weekdays to names
    weekday_mapping = {
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 
        3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 
        6: 'Saturday'
    }
    df['weekday_name'] = df['weekday'].map(weekday_mapping)
    
    # Ensure date column is in datetime format
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    return df


# Load data
df = load_data()

# Header
st.title('🚲 Analisis Penyewaan Sepeda')
st.markdown("""
    Dashboard ini menampilkan analisis komprehensif pola penyewaan sepeda
    berdasarkan berbagai faktor seperti musim, hari dalam seminggu, dan kondisi cuaca.
""")

# Tampilkan struktur data
if st.checkbox('Tampilkan struktur data'):
    st.write("Kolom dalam dataset:", df.columns.tolist())
    st.write("Sample data:", df.head())

# Palet warna seragam
sns.set_palette('coolwarm')

# Analisis Musiman
st.header('Analisis Berdasarkan Musim')

# Grafik penyewaan berdasarkan musim
fig_season, ax_season = plt.subplots(figsize=(10, 6))
seasonal_avg = df.groupby('season_name')['cnt'].mean()

# Penonjolan musim dengan penyewaan tertinggi
sns.barplot(x=seasonal_avg.index, y=seasonal_avg.values, ax=ax_season, 
            palette=['#3498db' if season != seasonal_avg.idxmax() else '#e74c3c' for season in seasonal_avg.index])

ax_season.set_title('Rata-rata Penyewaan Sepeda per Musim')
ax_season.set_xlabel('Musim')
ax_season.set_ylabel('Rata-rata Penyewaan')
plt.xticks(rotation=0)
st.pyplot(fig_season)

# Grafik penyewaan berdasarkan hari kerja
fig_workingday, ax_workingday = plt.subplots(figsize=(10, 6))
sns.barplot(x='workingday', y='cnt', data=df, ax=ax_workingday)
ax_workingday.set_title('Penyewaan Berdasarkan Hari Kerja')
ax_workingday.set_xlabel('Hari Kerja')
ax_workingday.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig_workingday)

# Grafik penyewaan berdasarkan cuaca
fig_weathersit, ax_weathersit = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=df, ax=ax_weathersit)
ax_weathersit.set_title('Penyewaan Berdasarkan Cuaca')
ax_weathersit.set_xlabel('Kondisi Cuaca')
ax_weathersit.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig_weathersit)

# Insight musiman
st.info(f"""
    💡 Insight Musiman:
    - Musim dengan penyewaan tertinggi: {seasonal_avg.idxmax()}
    - Rata-rata penyewaan tertinggi: {seasonal_avg.max():.2f} sepeda/hari
    - Variasi antar musim: {(seasonal_avg.max() - seasonal_avg.min()) / seasonal_avg.mean() * 100:.1f}%
""")

# analisis pengaruh perubahan cuaca dan suhu
st.header('Analisis Pengaruh Cuaca dan Suhu')

# Menghitung recency, frequency, dan monetary
df['recency'] = (df['dteday'].max() - df['dteday']).dt.days  # Hitung jumlah hari sejak pembelian terakhir
df['frequency'] = df.groupby('instant')['cnt'].transform('count')  # Hitung frekuensi transaksi
df['monetary'] = df['cnt']  # Gunakan jumlah penyewaan sebagai proxy untuk monetary value

# Visualisasi Pengaruh Suhu terhadap Jumlah Penyewaan
fig_temp, ax_temp = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', hue='season', data=df, ax=ax_temp)
ax_temp.set_title('Pengaruh Suhu terhadap Jumlah Penyewaan')
ax_temp.set_xlabel('Suhu (Normalized)')
ax_temp.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig_temp)

# Visualisasi Pengaruh Cuaca terhadap Jumlah Penyewaan
fig_weathersit, ax_weathersit = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=df, ax=ax_weathersit)
ax_weathersit.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan')
ax_weathersit.set_xlabel('Kondisi Cuaca')
ax_weathersit.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig_weathersit)

# Korelasi antara RFM
fig_rfm, ax_rfm = plt.subplots(figsize=(10, 6))
sns.heatmap(df[['recency', 'frequency', 'monetary']].corr(), annot=True, cmap='coolwarm', ax=ax_rfm)
ax_rfm.set_title('RFM Correlation')
st.pyplot(fig_rfm)


# Clustering Manual (Binning)
st.header('Clustering Manual: Pengelompokan Usia Pelanggan')

# Dummy clustering (contoh: pengelompokan berdasarkan jumlah penyewaan)
df['cnt_group'] = pd.cut(df['cnt'], bins=[0, 100, 200, 300, 400, 500], labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])

# Tampilkan hasil clustering
st.write(df[['cnt', 'cnt_group']].head())

# Kesimpulan
st.markdown("""
---
### 📊 Kesimpulan Utama
1. Musim panas merupakan periode dengan tingkat penyewaan tertinggi.
2. Terdapat perbedaan pola yang signifikan antara hari kerja dan akhir pekan.
3. Cuaca memiliki dampak besar terhadap jumlah penyewaan.
4. Ada korelasi positif antara temperatur dan jumlah penyewaan.
5. Analisis RFM memberikan wawasan penting tentang perilaku pelanggan.
6. Pengelompokan manual membantu memahami pola data berdasarkan jumlah penyewaan.

### 📈 Rekomendasi
1. Optimalkan ketersediaan sepeda pada musim panas.
2. Terapkan strategi harga berbeda untuk hari kerja dan akhir pekan.
3. Siapkan rencana kontingensi untuk kondisi cuaca buruk.
4. Pertimbangkan penambahan sepeda pada musim ramai.
""")
