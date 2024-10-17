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
    
    # Konversi kolom season ke nama musim
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_name'] = df['season'].map(season_mapping)
    
    # Konversi kolom weekday ke nama hari
    weekday_mapping = {
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 
        3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 
        6: 'Saturday'
    }
    df['weekday_name'] = df['weekday'].map(weekday_mapping)
    
    # Pastikan kolom dteday dikonversi menjadi datetime
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

# Insight musiman
st.info(f"""
    💡 Insight Musiman:
    - Musim dengan penyewaan tertinggi: {seasonal_avg.idxmax()}
    - Rata-rata penyewaan tertinggi: {seasonal_avg.max():.2f} sepeda/hari
    - Variasi antar musim: {(seasonal_avg.max() - seasonal_avg.min()) / seasonal_avg.mean() * 100:.1f}%
""")

# RFM Analysis
st.header('RFM Analysis')

# Menghitung recency, frequency, dan monetary
df['recency'] = (df['dteday'].max() - df['dteday']).dt.days  # Hitung jumlah hari sejak pembelian terakhir
df['frequency'] = df.groupby('instant')['cnt'].transform('count')  # Hitung frekuensi transaksi
df['monetary'] = df['cnt']  # Gunakan jumlah penyewaan sebagai proxy untuk monetary value

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
