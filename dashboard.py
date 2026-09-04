import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Konfigurasi Halaman (Harus di baris pertama)
st.set_page_config(page_title="Sewadah Dashboard", page_icon="🚲", layout="wide")

# 2. Fungsi Load Data
@st.cache_data
def load_data():
    # Membaca data yang sudah bersih
    day_df = pd.read_csv("main_data.csv")
    hour_df = pd.read_csv("hour_data.csv")
    
    # Mengembalikan tipe data datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Label jenis hari agar lebih deskriptif
    day_df['workingday_label'] = day_df['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})
    hour_df['workingday_label'] = hour_df['workingday'].map({0: 'Weekend/Holiday', 1: 'Working Day'})
    
    return day_df, hour_df

day_df, hour_df = load_data()

# 3. Sidebar (Profil & Filter Interaktif)
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

# Filter Interaktif
st.sidebar.header("⚙️ Filter Interaktif")

# Filter 1: Pemilihan Musim untuk Grafik 1
season_options = list(day_df['season'].dropna().unique())
default_season_idx = season_options.index('Summer') if 'Summer' in season_options else 0
selected_season = st.sidebar.selectbox(
    "1. Pilih Musim (Grafik 1 - Tipe Hari):",
    options=season_options,
    index=default_season_idx
)

# Filter 2: Kondisi Cuaca untuk Grafik 2
weather_options = list(hour_df['weathersit'].dropna().unique())
selected_weather = st.sidebar.selectbox(
    "2. Kondisi Cuaca (Grafik 2 - Jam Puncak):",
    options=weather_options,
    index=0
)

# Filter 3: Jenis Hari untuk Grafik 3
selected_day_types = st.sidebar.multiselect(
    "3. Jenis Hari (Grafik 3 - Tren Bulanan):",
    options=['Working Day', 'Weekend/Holiday'],
    default=['Working Day', 'Weekend/Holiday']
)

# Filter 4: Musim untuk Grafik 4
selected_seasons_scatter = st.sidebar.multiselect(
    "4. Musim (Grafik 4 - Korelasi Suhu):",
    options=season_options,
    default=season_options
)

st.sidebar.markdown("---")
st.sidebar.markdown('''
**Profil Analis:**  
👤 **Nama:** Renaldi Akbar Priambodo  
📧 **Email:** renaldi.akbar75@gmail.com  
🎓 **ID Dicoding:** renaldi_akbar_QdHm  
''')
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Sewadah.")

# 4. Header Utama Dashboard
st.title("📊 Laporan Performa Penyewaan Sepeda")
st.markdown("Analisis komprehensif mengenai pola peminjaman sepeda berdasarkan faktor waktu, musim, dan kondisi lingkungan.")
st.divider()

# BARIS 1: Analisis Kategori dan Perilaku
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Rata-rata Penyewaan: Hari Kerja vs Libur")
    st.caption(f"Musim {selected_season} (Tahun 2012)")
    
    # Filter data berdasarkan pilihan musim dari sidebar
    summer_2012_df = day_df[(day_df['season'] == selected_season) & (day_df['yr'] == 1)]
    
    if summer_2012_df.empty:
        st.warning(f"Data tidak ditemukan untuk musim {selected_season}.")
    else:
        q1_explore = summer_2012_df.groupby('workingday_label')['cnt'].mean().reset_index()
        
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='workingday_label', y='cnt', data=q1_explore, palette=['#D3D3D3', '#1F77B4'], ax=ax1)
        ax1.set_xlabel('Tipe Hari')
        ax1.set_ylabel('Rata-rata Peminjaman')
        st.pyplot(fig1)
        
        st.markdown(f"""
        Pada musim **{selected_season}** tahun 2012, grafik di atas memperlihatkan perbandingan intensitas penyewaan sepeda harian antara hari kerja dan akhir pekan/hari libur berdasarkan parameter yang dipilih.
        """)

with col2:
    st.subheader("Top 5 Jam Puncak Pengguna Casual")
    st.caption(f"Cuaca '{selected_weather}' (Tahun 2011)")
    
    # Filter data berdasarkan kondisi cuaca dari sidebar
    filtered_hour_df = hour_df[(hour_df['weathersit'] == selected_weather) & (hour_df['yr'] == 0)]
    
    if filtered_hour_df.empty:
        st.warning(f"Tidak ada catatan aktivitas untuk kondisi cuaca '{selected_weather}'.")
    else:
        q2_explore = filtered_hour_df.groupby('hr')['casual'].sum().reset_index()
        top_hours = q2_explore.sort_values(by='casual', ascending=False).head(5)
        
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='hr', y='casual', data=top_hours, palette='viridis', ax=ax2)
        ax2.set_xlabel('Jam (0-23)')
        ax2.set_ylabel('Total Pengguna Kasual')
        st.pyplot(fig2)
        
        st.markdown(f"""
        **Penjelasan:**  
        Saat kondisi cuaca **{selected_weather}**, lonjakan penyewaan oleh pengguna kasual terdistribusi pada jam-jam di atas. Informasi ini menjadi acuan waktu siaga armada bagi tim lapangan.
        """)

st.divider()

# BARIS 2: Tren dan Korelasi Lingkungan
col3, col4 = st.columns(2)

with col3:
    st.subheader("Tren Total Peminjaman Sepeda Bulanan")
    st.caption("Perbandingan Year-over-Year (2011 vs 2012)")
    
    if not selected_day_types:
        st.warning("Silakan pilih minimal satu jenis hari pada filter sidebar.")
    else:
        # Filter berdasarkan jenis hari dari multiselect
        filtered_trend_df = day_df[day_df['workingday_label'].isin(selected_day_types)]
        monthly_trend = filtered_trend_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
        monthly_trend['Tahun'] = monthly_trend['yr'].map({0: '2011', 1: '2012'})
        
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.lineplot(x='mnth', y='cnt', hue='Tahun', data=monthly_trend, marker='o', palette=['#FF9999', '#66B2FF'], ax=ax3)
        ax3.set_xticks(range(1, 13))
        ax3.set_xlabel('Bulan')
        ax3.set_ylabel('Total Peminjaman')
        st.pyplot(fig3)
        
        st.markdown("""
        Grafik menunjukkan fluktuasi pertumbuhan bulanan untuk kategori hari terpilih. Tren peminjaman secara konsisten meningkat di pertengahan tahun dan menurun di awal serta akhir tahun.
        """)

with col4:
    st.subheader("Korelasi Suhu Terhadap Peminjaman")
    st.caption("Distribusi Suhu berdasarkan Musim Terpilih")
    
    if not selected_seasons_scatter:
        st.warning("Silakan pilih minimal satu musim pada filter sidebar.")
    else:
        # Filter berdasarkan pilihan musim dari multiselect
        filtered_scatter_df = day_df[day_df['season'].isin(selected_seasons_scatter)]
        
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x='temp', y='cnt', hue='season', data=filtered_scatter_df, palette='Set2', alpha=0.7, ax=ax4)
        ax4.set_xlabel('Suhu Normalisasi (temp)')
        ax4.set_ylabel('Total Peminjaman (cnt)')
        st.pyplot(fig4)
        
        st.markdown("""
        Peningkatan suhu harian memiliki korelasi positif terhadap volume penyewaan sepeda. Titik-titik data memperlihatkan konsentrasi penyewaan tertinggi saat temperatur berada pada rentang hangat.
        """)
