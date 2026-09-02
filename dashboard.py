import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Konfigurasi Halaman (Harus di baris pertama)
st.set_page_config(page_title="Sewadah Dashboard", page_icon="🚲", layout="wide")

# 2. Fungsi Load & Clean Data
@st.cache_data
def load_data():
    # Membaca data yang sudah bersih
    day_df = pd.read_csv("main_data.csv")
    hour_df = pd.read_csv("hour_data.csv")
    
    # Mengembalikan tipe data datetime yang berubah menjadi string saat diekspor ke CSV
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# 3. Sidebar (Profil Perusahaan)
# Menggunakan gambar publik dari Unsplash sebagai pemanis
st.sidebar.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60", use_container_width=True)
st.sidebar.title("🚲 Sewadah")
st.sidebar.markdown('''
Sewadah: Teman andalan sewa sepeda untuk mobilitas harian dan rekreasi akhir pekanmu.
''')
st.sidebar.markdown("---")
st.sidebar.markdown('''
Dashboard ini dirancang untuk memantau performa armada dan menganalisis perilaku pelanggan kami guna meningkatkan operasional harian.
''')
st.sidebar.markdown("---")
st.sidebar.markdown('''
**Profil Analis:**  
👤 **Nama:** Renaldi Akbar Priamnodo  
📧 **Email:** renaldi.akbar75@gmail.com  
🎓 **ID Dicoding:** renaldi_akbar_QdHm  
''')
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Sewadah.")

# 4. Header Utama Dashboard
st.title("📊 Laporan Performa Penyewaan Sepeda")
st.markdown("Analisis komprehensif mengenai pola peminjaman sepeda berdasarkan faktor waktu, musim, dan kondisi lingkungan.")
st.divider()


# Analisis Kategori dan Perilaku
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Penyewaan: Hari Kerja vs Libur")
    st.caption("Fokus: Musim Panas 2012")
    
    summer_2012_df = day_df[(day_df['season'] == 'Summer') & (day_df['yr'] == 1)]
    q1_explore = summer_2012_df.groupby('workingday')['cnt'].mean().reset_index()
    q1_explore['workingday_label'] = q1_explore['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})
    
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='workingday_label', y='cnt', data=q1_explore, palette=['#D3D3D3', '#1F77B4'], ax=ax1)
    ax1.set_xlabel('Tipe Hari')
    ax1.set_ylabel('Rata-rata Peminjaman')
    st.pyplot(fig1)
    
    st.markdown("""
    Pada musim panas 2012, intensitas penyewaan harian lebih tinggi pada akhir pekan (6.347) dibandingkan hari kerja (6.149). Ini mengindikasikan dominasi penggunaan sepeda untuk tujuan rekreasi.
    """)

with col2:
    st.subheader("Top 5 Jam Puncak Pengguna Casual")
    st.caption("Fokus: Cuaca Cerah Tahun 2011")
    
    clear_2011_df = hour_df[(hour_df['weathersit'] == 'Clear/Partly Cloudy') & (hour_df['yr'] == 0)]
    q2_explore = clear_2011_df.groupby('hr')['casual'].sum().reset_index()
    top_hours = q2_explore.sort_values(by='casual', ascending=False).head()
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='hr', y='casual', data=top_hours, palette='viridis', ax=ax2)
    ax2.set_xlabel('Jam (0-23)')
    ax2.set_ylabel('Total Pengguna Kasual')
    st.pyplot(fig2)
    
    st.markdown(""" 
    Pengguna casual memusatkan aktivitasnya pada siang hingga sore hari. Lonjakan tertinggi terjadi pada pukul 17:00, yang membutuhkan kesiapan armada maksimal pada jam tersebut.
    """)

st.divider()


# Tren dan Korelasi Lingkungan

col3, col4 = st.columns(2)

with col3:
    st.subheader("Tren Total Peminjaman Sepeda Bulanan")
    st.caption("Perbandingan Year-over-Year (2011 vs 2012)")
    
    # Agregasi bulanan
    monthly_trend = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
    monthly_trend['Tahun'] = monthly_trend['yr'].map({0: '2011', 1: '2012'})
    
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.lineplot(x='mnth', y='cnt', hue='Tahun', data=monthly_trend, marker='o', palette=['#FF9999', '#66B2FF'], ax=ax3)
    ax3.set_xticks(range(1, 13))
    ax3.set_xlabel('Bulan')
    ax3.set_ylabel('Total Peminjaman')
    st.pyplot(fig3)
    
    st.markdown(""" 
    Terjadi pertumbuhan yang konsisten antara tahun 2011 dan 2012. Grafik menunjukkan tren peminjaman memuncak pada pertengahan tahun (bulan 6-9) dan anjlok di awal serta akhir tahun akibat musim dingin.
    """)

with col4:
    st.subheader("Korelasi Suhu Terhadap Peminjaman")
    st.caption("Distribusi berdasarkan Musim (2011-2012)")
    
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x='temp', y='cnt', hue='season', data=day_df, palette='Set2', alpha=0.7, ax=ax4)
    ax4.set_xlabel('Suhu Normalisasi (temp)')
    ax4.set_ylabel('Total Peminjaman (cnt)')
    st.pyplot(fig4)
    
    st.markdown("""
    Terdapat korelasi positif antara suhu dan total peminjaman. Semakin hangat suhu (mendekati 0.7 - 0.8), jumlah peminjaman cenderung meningkat drastis, terutama yang didominasi oleh titik data dari musim panas (*Summer*) dan gugur (*Fall*).
    """)