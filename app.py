import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import os
import time

# ============================================
# 1. KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="ECO-FOREST VALUATION - KPH Saradan",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 2. DATA
# ============================================
forest_data = pd.DataFrame({
    'kelas_umur': ['KU I', 'KU II', 'KU III', 'KU IV', 'KU V', 'KU VI', 'KU VII', 'KU VIII'],
    'kisaran_umur': ['1-10 Tahun', '11-20 Tahun', '21-30 Tahun', '31-40 Tahun', 
                     '41-50 Tahun', '51-60 Tahun', '61-70 Tahun', '71-80 Tahun'],
    'luas_ha': [2875.20, 3157.05, 5897.50, 4226.15, 2035.30, 1210.80, 1048.10, 801.05],
    'persentase': [13.50, 14.83, 27.69, 19.85, 9.56, 5.69, 4.92, 3.76]
})

production_data = pd.DataFrame({
    'jenis_kayu': ['Jati', 'Rimba'],
    'volume_2016': [7303.89, 2407.34],
    'volume_2017': [6101.41, 2313.40],
    'perubahan_persen': [-16.46, -3.90]
})

financial_data = pd.DataFrame({
    'indikator': ['NPV (Rp Juta)', 'IRR (%)', 'BCR'],
    'skenario_a': [4078, 18.00, 1.45],
    'skenario_b': [7058, 20.00, 1.82],
    'selisih': [2980, 2.00, 0.37]
})

# ============================================
# 3. CSS
# ============================================
st.markdown("""
<style>
    .eco-header {
        background: linear-gradient(145deg, #0d2b1e 0%, #1a5e3a 50%, #0d2b1e 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(26, 94, 58, 0.4);
        border: 1px solid rgba(165, 214, 167, 0.15);
    }
    .eco-header h1 {
        color: #ffffff !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: 3px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .eco-header h1 .highlight {
        color: #81c784;
        font-weight: 300;
    }
    .eco-header .sub {
        color: #a5d6a7;
        font-size: 1rem;
        margin: 0.3rem 0 0 0;
        letter-spacing: 2px;
        font-weight: 300;
    }
    .eco-header .location {
        color: #66bb6a;
        font-size: 0.85rem;
        margin: 0.2rem 0 0 0;
        opacity: 0.9;
    }
    .divider-custom {
        border: none;
        border-top: 2px solid #c8e6c9;
        margin: 0.8rem 0;
    }
    .css-1d391kg {
        display: none !important;
    }
    .group-card {
        background-color: #f0f7f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
        height: 100%;
        text-align: center;
        transition: transform 0.2s;
    }
    .group-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
    }
    .group-card p {
        font-size: 1rem;
        font-weight: 600;
        color: #1a5e3a;
        margin-bottom: 0.2rem;
    }
    .group-card small {
        font-size: 0.85rem;
        color: #555;
    }
    .course-card {
        background-color: #e8f5e9;
        padding: 0.8rem 1.2rem;
        border-radius: 0.5rem;
        border: 1px solid #a5d6a7;
        text-align: center;
        transition: transform 0.2s;
    }
    .course-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15);
    }
    .course-card p {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1a5e3a;
        margin-bottom: 0.2rem;
    }
    .course-card span {
        font-size: 1rem;
        color: #333;
    }
    .identity-container {
        background: #f8faf8;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e8f0e8;
        margin-bottom: 1.5rem;
    }
    .analysis-box {
        background-color: #e3f2fd;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #1565c0;
        margin: 1rem 0;
    }
    .analysis-box h4 {
        color: #0d47a1;
        margin-bottom: 0.5rem;
    }
    .analysis-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .analysis-box li {
        margin: 0.3rem 0;
        color: #1a237e;
    }
    .analysis-box-green {
        background-color: #e8f5e9;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #2e7d32;
        margin: 1rem 0;
    }
    .analysis-box-green h4 {
        color: #1a5e3a;
        margin-bottom: 0.5rem;
    }
    .analysis-box-green ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .analysis-box-green li {
        margin: 0.3rem 0;
        color: #1a3a2a;
    }
    .data-table-container {
        background-color: #fafafa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .section-title {
        color: #1a5e3a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #c8e6c9;
    }
    .sub-section-title {
        color: #2e7d32;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        display: none !important;
    }
    .stat-card {
        background-color: #f8faf8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0ece0;
        text-align: center;
        height: 100%;
        transition: transform 0.2s;
    }
    .stat-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stat-card .stat-label {
        font-size: 0.8rem;
        color: #555;
        margin: 0;
    }
    .stat-card .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a5e3a;
        margin: 0;
    }
    .stat-card .stat-unit {
        font-size: 0.8rem;
        color: #777;
        margin: 0;
    }
    .info-card {
        background-color: #f5faf5;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0ece0;
        height: 100%;
    }
    .info-card h5 {
        color: #1a5e3a;
        margin-top: 0;
    }
    .info-card ul {
        font-size: 0.9rem;
        color: #444;
        padding-left: 1.2rem;
    }
    .info-card ul li {
        margin: 0.3rem 0;
    }
    .deskripsi-kph {
        background-color: #f5faf5;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #c8e6c9;
        line-height: 1.8;
        font-size: 1rem;
        color: #2d3a2d;
        text-align: justify;
    }
    .deskripsi-kph p {
        margin-bottom: 0.8rem;
    }
    .deskripsi-kph strong {
        color: #1a5e3a;
    }
    .insight-box {
        background-color: #fff8e1;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #ffa000;
        margin: 1rem 0;
    }
    .insight-box h4 {
        color: #e65100;
        margin-bottom: 0.5rem;
    }
    .insight-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .insight-box li {
        margin: 0.3rem 0;
        color: #4e342e;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. HEADER
# ============================================
st.markdown("""
<div class="eco-header">
    <h1>🌳 ECO-FOREST <span class="highlight">VALUATION</span></h1>
    <p class="sub">Sistem Valuasi Ekonomi Hutan</p>
    <p class="location">📍 KPH Saradan · Jawa Timur</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 5. SIDEBAR
# ============================================
with st.sidebar:
    try:
        logo_path = "logo-unisba.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
    except:
        pass
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    
    st.markdown("### 📋 Navigasi")
    menu = st.radio(
        "Pilih Halaman:",
        options=[
            "🏠 Beranda",
            "🌳 Profil Hutan",
            "🪵 Produksi Kayu",
            "📋 Master Data",
            "⚙️ Simulasi Finansial",
            "📈 Dashboard Summary"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)

# ============================================
# 6. FUNGSI UMUM
# ============================================

def apply_chart_settings(fig, show_grid=True, height=400):
    fig.update_layout(
        height=height,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(showgrid=show_grid)
    fig.update_yaxes(showgrid=show_grid)
    
    fig.update_layout(
        dragmode='zoom',
        hoverdistance=100,
        spikedistance=1000
    )
    
    return fig

# ============================================
# 7. KONTEN PER HALAMAN
# ============================================

# ==================== BERANDA ====================
if menu == "🏠 Beranda":
    st.markdown('<h1 class="section-title">🏠 Beranda</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # IDENTITAS KELOMPOK
    st.markdown("""
    <div class="identity-container">
        <h4 style="color: #1a5e3a; text-align: center; margin-bottom: 0.8rem;">👥 Identitas Kelompok</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="group-card">
            <p>👤 Arif Hamdani</p>
            <small>10090224008</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="group-card">
            <p>👤 Bambang Karta Wijaya</p>
            <small>10090224025</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="group-card">
            <p>👤 Moh Bayu Mustofa</p>
            <small>10090224030</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="course-card">
            <p>📚 Mata Kuliah</p>
            <span>Ekonomi Sumber Daya Alam dan Lingkungan</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="course-card">
            <p>👨‍🏫 Dosen Pengampu</p>
            <span>Yuhka Sundaya, S.E., M.Si.</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==========================================
    # DESKRIPSI KPH SARADAN (SINGKAT)
    # ==========================================
    st.subheader("📍 Profil KPH Saradan")
    
    st.markdown("""
    <div class="deskripsi-kph">
        <p>
            <strong>Kesatuan Pemangkuan Hutan (KPH) Saradan</strong> adalah unit pengelolaan hutan di 
            <strong>Jawa Timur</strong> yang mencakup wilayah <strong>Madiun, Bojonegoro, Ngawi, dan Nganjuk</strong>. 
            Dengan luas <strong>37.934,66 Ha</strong>, kawasan ini berfungsi sebagai <strong>Hutan Produksi dan Hutan Lindung</strong> 
            dengan komoditas utama <strong>Jati (Tectona grandis)</strong>.
        </p>
        <p>
            KPH Saradan dikelola dengan sistem <strong>8 kelas umur</strong> untuk memastikan keberlanjutan produksi kayu. 
            Sebaran luas didominasi oleh <strong>kelas umur muda hingga sedang (KU I - KU IV)</strong> yang mencapai <strong>76%</strong>, 
            mengindikasikan potensi produksi kayu yang baik dalam 20-30 tahun mendatang. 
            Kawasan ini juga memiliki potensi <strong>stok karbon</strong> yang signifikan, 
            menjadikannya aset penting dalam <strong>mitigasi perubahan iklim</strong> dan ekonomi hijau.
        </p>
        <p style="font-size: 0.9rem; color: #555; margin-top: 0.5rem;">
            <strong>📍 Lokasi:</strong> Madiun, Bojonegoro, Ngawi, Nganjuk · 
            <strong>🌳 Luas:</strong> 37.934,66 Ha · 
            <strong>🪵 Komoditas:</strong> Jati (Tectona grandis)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # TENTANG DASHBOARD
    st.markdown("""
    ### 📊 Tentang Dashboard
    
    Dashboard **Eco-Forest Valuation** ini merupakan hasil analisis data dari **KPH Saradan** 
    yang bertujuan untuk memberikan gambaran menyeluruh tentang kondisi hutan, 
    produksi kayu, dan kelayakan finansial pengelolaan hutan.
    """)
    
    # METRIK UTAMA
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌳 Total Luas", "37.934,66 Ha", help="Total luas kawasan hutan KPH Saradan")
    with col2:
        st.metric("🪵 Komoditas", "Jati", help="Komoditas utama KPH Saradan")
    with col3:
        st.metric("📅 Tahun Data", "2026", help="Tahun data terbaru")
    with col4:
        st.metric("📍 Wilayah", "4 Kabupaten", help="Wilayah kerja KPH Saradan")
    
    st.markdown("---")
    
    # PREVIEW GRAFIK
    st.subheader("📈 Preview Grafik - Distribusi Luas")
    
    fig = px.pie(
        forest_data,
        values='luas_ha',
        names='kelas_umur',
        title='Distribusi Luas per Kelas Umur',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')
    fig = apply_chart_settings(fig, True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box" style="border-left-color: #2e7d32;">
        <h4>📌 Analisis Singkat</h4>
        <ul>
            <li>Grafik di atas menunjukkan distribusi luas hutan KPH Saradan berdasarkan kelas umur.</li>
            <li><strong>KU III (21-30 tahun)</strong> mendominasi dengan persentase terbesar yaitu <strong>27,69%</strong>.</li>
            <li>Hal ini mengindikasikan bahwa <strong>sebagian besar kawasan hutan berada pada fase produktif</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # STATISTIK CEPAT
    st.markdown("---")
    st.subheader("📊 Statistik Cepat")
    
    total_luas = forest_data['luas_ha'].sum()
    total_produksi = production_data['volume_2017'].sum()
    npv_b = financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_b'].values[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background-color: #e8f5e9; border: 1px solid #a5d6a7;">
            <p class="stat-label">Total Luas Kawasan</p>
            <p class="stat-value" style="color: #1a5e3a;">{total_luas:,.0f}</p>
            <p class="stat-unit">Hektar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background-color: #e3f2fd; border: 1px solid #90caf9;">
            <p class="stat-label">Total Produksi Kayu 2017</p>
            <p class="stat-value" style="color: #0d47a1;">{total_produksi:,.0f}</p>
            <p class="stat-unit">m³</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background-color: #fff3e0; border: 1px solid #ffcc80;">
            <p class="stat-label">NPV Skenario Hijau</p>
            <p class="stat-value" style="color: #e65100;">Rp {npv_b:,.0f}</p>
            <p class="stat-unit">Juta Rupiah</p>
        </div>
        """, unsafe_allow_html=True)
    
    # INFORMASI TAMBAHAN
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h5>🌿 Tujuan Dashboard</h5>
            <ul>
                <li>Menyajikan data dan informasi KPH Saradan secara interaktif</li>
                <li>Memberikan analisis sebaran kelas umur hutan</li>
                <li>Menampilkan tren produksi kayu 2016-2017</li>
                <li>Simulasi kelayakan finansial dengan 2 skenario</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h5>📌 Navigasi</h5>
            <ul>
                <li><strong>🌳 Profil Hutan</strong> - Sebaran kelas umur & simulasi</li>
                <li><strong>🪵 Produksi Kayu</strong> - Data produksi 2016-2017</li>
                <li><strong>📋 Master Data</strong> - Semua data lengkap</li>
                <li><strong>⚙️ Simulasi Finansial</strong> - Analisis kelayakan</li>
                <li><strong>📈 Dashboard Summary</strong> - Ringkasan semua data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== PROFIL HUTAN ====================
elif menu == "🌳 Profil Hutan":
    st.markdown('<h1 class="section-title">🌳 Profil Hutan</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="analysis-box">
        <h4>📊 Analisis Sebaran Kelas Umur</h4>
        <ul>
            <li><strong>Luas total kawasan</strong> mencapai <strong>37.934,66 Ha</strong> yang terbagi dalam 8 kelas umur.</li>
            <li><strong>Kelas umur KU III (21-30 tahun)</strong> memiliki luas terbesar yaitu <strong>5.897,50 Ha (27,69%)</strong>.</li>
            <li><strong>Kelas umur KU VIII (71-80 tahun)</strong> memiliki luas terkecil yaitu <strong>801,05 Ha (3,76%)</strong>.</li>
            <li>Sebaran luas menunjukkan <strong>dominasi pada kelas umur muda hingga sedang</strong> (KU I - KU IV) dengan total 76%.</li>
            <li>Hal ini mengindikasikan <strong>potensi produksi kayu yang baik</strong> dalam 20-30 tahun mendatang.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Informasi Umum")
        st.markdown("""
        | **Parameter** | **Nilai** |
        |--------------|-----------|
        | **Nama KPH** | KPH Saradan |
        | **Lokasi** | Madiun, Bojonegoro, Ngawi, Nganjuk |
        | **Luas Total** | 37.934,66 Ha |
        | **Tipe Hutan** | Hutan Produksi & Lindung |
        | **Kelas Perusahaan** | Jati (Tectona grandis) |
        | **Topografi** | Datar hingga Bergelombang |
        | **Tipe Iklim** | Tipe D (Schmidt-Ferguson) |
        """)
    
    with col2:
        st.subheader("📊 Statistik Luas")
        total_luas = forest_data['luas_ha'].sum()
        luas_terbesar = forest_data['luas_ha'].max()
        luas_terkecil = forest_data['luas_ha'].min()
        rata_rata = forest_data['luas_ha'].mean()
        kelas_terbesar = forest_data[forest_data['luas_ha'] == luas_terbesar]['kelas_umur'].values[0]
        kelas_terkecil = forest_data[forest_data['luas_ha'] == luas_terkecil]['kelas_umur'].values[0]
        
        st.metric("Total Luas", f"{total_luas:,.2f} Ha")
        st.metric("Rata-rata Luas per Kelas", f"{rata_rata:,.2f} Ha")
        st.metric("Luas Terbesar", f"{luas_terbesar:,.2f} Ha", f"Kelas {kelas_terbesar}")
        st.metric("Luas Terkecil", f"{luas_terkecil:,.2f} Ha", f"Kelas {kelas_terkecil}")
    
    st.markdown("---")
    
    # SLIDER SIMULASI
    st.subheader("📊 Simulasi Sebaran Luas")
    
    st.markdown("""
    <div style="background-color: #f5faf5; padding: 1rem; border-radius: 8px; border: 1px solid #e0ece0; margin-bottom: 1rem;">
        <p style="color: #1a5e3a; font-weight: 600; margin-bottom: 0.5rem;">🎛️ Atur Parameter Simulasi</p>
        <p style="font-size: 0.9rem; color: #555;">Geser slider di bawah untuk melihat perubahan luas per kelas umur</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_luas_simulasi = st.slider(
            "🌲 Total Luas Kawasan (Ha)",
            min_value=10000.0,
            max_value=60000.0,
            value=total_luas,
            step=1000.0
        )
    
    with col2:
        proporsi_ku3 = st.slider(
            "📈 Proporsi KU III (%)",
            min_value=15.0,
            max_value=40.0,
            value=27.69,
            step=0.5
        )
    
    with col3:
        proporsi_tua = st.slider(
            "📉 Proporsi KU VII-VIII (%)",
            min_value=2.0,
            max_value=15.0,
            value=8.68,
            step=0.5
        )
    
    base_proporsi = forest_data['persentase'].values
    kelas_umur = forest_data['kelas_umur'].values
    
    proporsi_simulasi = base_proporsi.copy()
    proporsi_simulasi[2] = proporsi_ku3
    proporsi_simulasi[6] = proporsi_tua * 0.6
    proporsi_simulasi[7] = proporsi_tua * 0.4
    proporsi_simulasi = proporsi_simulasi / proporsi_simulasi.sum() * 100
    
    luas_simulasi = proporsi_simulasi / 100 * total_luas_simulasi
    
    simulasi_data = pd.DataFrame({
        'kelas_umur': kelas_umur,
        'luas_ha': luas_simulasi,
        'persentase': proporsi_simulasi
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_simulasi = px.bar(
            simulasi_data,
            x='kelas_umur',
            y='luas_ha',
            title=f'Hasil Simulasi Sebaran Luas (Total: {total_luas_simulasi:,.0f} Ha)',
            color='kelas_umur',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            text='luas_ha'
        )
        fig_simulasi.update_traces(texttemplate='%{text:,.0f}', textposition='outside', width=0.7)
        fig_simulasi = apply_chart_settings(fig_simulasi, True)
        st.plotly_chart(fig_simulasi, use_container_width=True)
        
        st.markdown("""
        <div class="analysis-box-green">
            <h4>📌 Analisis Grafik Simulasi</h4>
            <ul>
                <li>Grafik ini menunjukkan hasil simulasi sebaran luas berdasarkan parameter yang diatur.</li>
                <li>Perubahan pada <strong>total luas</strong> akan menggeser seluruh nilai luas secara proporsional.</li>
                <li>Perubahan pada <strong>proporsi KU III</strong> akan mempengaruhi luas kelas umur produktif.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        fig_pie = px.pie(
            simulasi_data,
            values='persentase',
            names='kelas_umur',
            title='Distribusi Persentase per Kelas Umur',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            hole=0.3
        )
        fig_pie.update_traces(textinfo='percent+label')
        fig_pie = apply_chart_settings(fig_pie, True)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
        <div class="analysis-box-green">
            <h4>📌 Analisis Pie Chart Simulasi</h4>
            <ul>
                <li>Pie chart menunjukkan persentase kontribusi setiap kelas umur terhadap total luas.</li>
                <li><strong>KU III</strong> mendominasi dengan persentase yang dapat diatur melalui slider.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Perbandingan Data Asli vs Hasil Simulasi")
    
    perbandingan = pd.DataFrame({
        'Kelas Umur': kelas_umur,
        'Luas Asli (Ha)': forest_data['luas_ha'].values,
        'Luas Simulasi (Ha)': luas_simulasi,
        'Persentase Asli (%)': forest_data['persentase'].values,
        'Persentase Simulasi (%)': proporsi_simulasi
    })
    
    perbandingan['Selisih Luas (Ha)'] = perbandingan['Luas Simulasi (Ha)'] - perbandingan['Luas Asli (Ha)']
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        perbandingan.style.format({
            'Luas Asli (Ha)': '{:,.2f}',
            'Luas Simulasi (Ha)': '{:,.2f}',
            'Persentase Asli (%)': '{:.2f}',
            'Persentase Simulasi (%)': '{:.2f}',
            'Selisih Luas (Ha)': '{:,.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"📌 Total luas asli: {total_luas:,.2f} Ha | Total luas simulasi: {total_luas_simulasi:,.2f} Ha")
    st.markdown('</div>', unsafe_allow_html=True)
    
    selisih_total = total_luas_simulasi - total_luas
    selisih_ku3 = perbandingan[perbandingan['Kelas Umur'] == 'KU III']['Selisih Luas (Ha)'].values[0]
    
    st.markdown(f"""
    <div class="analysis-box" style="border-left-color: #2e7d32;">
        <h4>📊 Analisis Perbandingan</h4>
        <ul>
            <li><strong>Total luas</strong> berubah dari <strong>{total_luas:,.2f} Ha</strong> menjadi <strong>{total_luas_simulasi:,.2f} Ha</strong> (selisih <strong>{selisih_total:+,.2f} Ha</strong>).</li>
            <li><strong>Kelas KU III</strong> berubah dari <strong>{forest_data[forest_data['kelas_umur']=='KU III']['luas_ha'].values[0]:,.2f} Ha</strong> menjadi <strong>{perbandingan[perbandingan['Kelas Umur']=='KU III']['Luas Simulasi (Ha)'].values[0]:,.2f} Ha</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Data Asli Sebaran Kelas Umur")
    
    fig_asli = px.bar(
        forest_data,
        x='kelas_umur',
        y='luas_ha',
        title='Data Asli Sebaran Luas per Kelas Umur',
        color='kelas_umur',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        text='luas_ha'
    )
    fig_asli.update_traces(texttemplate='%{text:,.0f}', textposition='outside', width=0.7)
    fig_asli = apply_chart_settings(fig_asli, True)
    st.plotly_chart(fig_asli, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Grafik Data Asli</h4>
        <ul>
            <li><strong>KU III (21-30 tahun)</strong> memiliki luas terbesar yaitu <strong>5.897,50 Ha</strong>.</li>
            <li>Terjadi <strong>penurunan luas</strong> dari KU III ke KU VIII yang cukup signifikan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        forest_data.style.format({
            'luas_ha': '{:,.2f}',
            'persentase': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"📌 Total {len(forest_data)} kelas umur | Total luas: {forest_data['luas_ha'].sum():,.2f} Ha")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="analysis-box" style="border-left-color: #1565c0;">
        <h4>📊 Analisis Data Asli</h4>
        <ul>
            <li><strong>Dominasi Kelas Umur Muda:</strong> Kelas KU I - KU IV mendominasi dengan total <strong>76%</strong>.</li>
            <li><strong>Potensi Produksi:</strong> KPH Saradan memiliki potensi produksi kayu yang baik dalam 20-30 tahun.</li>
            <li><strong>Rekomendasi:</strong> Perlu dilakukan program peremajaan hutan untuk keberlanjutan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== PRODUKSI KAYU ====================
elif menu == "🪵 Produksi Kayu":
    st.markdown('<h1 class="section-title">🪵 Produksi Kayu</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    total_2016 = production_data['volume_2016'].sum()
    total_2017 = production_data['volume_2017'].sum()
    perubahan_total = ((total_2017 / total_2016) - 1) * 100
    
    st.markdown(f"""
    <div class="analysis-box">
        <h4>📊 Analisis Produksi Kayu</h4>
        <ul>
            <li><strong>Total produksi tahun 2016</strong> mencapai <strong>{total_2016:,.2f} m³</strong>.</li>
            <li><strong>Total produksi tahun 2017</strong> mencapai <strong>{total_2017:,.2f} m³</strong>.</li>
            <li>Terjadi <strong>penurunan produksi sebesar {abs(perubahan_total):.2f}%</strong> dari tahun 2016 ke 2017.</li>
            <li><strong>Kayu Jati</strong> mengalami penurunan <strong>{abs(production_data[production_data['jenis_kayu']=='Jati']['perubahan_persen'].values[0]):.2f}%</strong>.</li>
            <li><strong>Kayu Rimba</strong> mengalami penurunan <strong>{abs(production_data[production_data['jenis_kayu']=='Rimba']['perubahan_persen'].values[0]):.2f}%</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Produksi 2016", f"{total_2016:,.2f} m³")
    with col2:
        st.metric("Total Produksi 2017", f"{total_2017:,.2f} m³")
    with col3:
        st.metric("Perubahan", f"{perubahan_total:.2f}%", delta=f"{perubahan_total:.2f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        color_theme = st.selectbox(
            "🎨 Tema Warna",
            options=["Greens", "Blues", "Reds", "Viridis", "Plasma", "Cividis"],
            index=0
        )
    with col2:
        show_labels = st.checkbox("🏷️ Tampilkan Label", value=True)
    
    st.subheader("📊 Perbandingan Produksi per Jenis Kayu")
    
    prod_melted = production_data.melt(
        id_vars=['jenis_kayu'],
        value_vars=['volume_2016', 'volume_2017'],
        var_name='tahun',
        value_name='volume'
    )
    
    fig1 = px.bar(
        prod_melted,
        x='jenis_kayu',
        y='volume',
        color='tahun',
        barmode='group',
        title='Perbandingan Produksi 2016 vs 2017',
        text='volume' if show_labels else None,
        color_discrete_map={'volume_2016': '#2e7d32', 'volume_2017': '#66bb6a'}
    )
    if show_labels:
        fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig1 = apply_chart_settings(fig1, True)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Grafik Perbandingan Produksi</h4>
        <ul>
            <li><strong>Kayu Jati</strong> mengalami penurunan dari <strong>7.303,89 m³</strong> menjadi <strong>6.101,41 m³</strong> (turun 16,46%).</li>
            <li><strong>Kayu Rimba</strong> mengalami penurunan dari <strong>2.407,34 m³</strong> menjadi <strong>2.313,40 m³</strong> (turun 3,90%).</li>
            <li><strong>Jati</strong> masih menjadi komoditas utama dengan kontribusi terbesar.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📈 Tren Produksi 2016-2017")
    
    prod_line = production_data.melt(
        id_vars=['jenis_kayu'],
        value_vars=['volume_2016', 'volume_2017'],
        var_name='tahun',
        value_name='volume'
    )
    prod_line['tahun'] = prod_line['tahun'].str.replace('volume_', '')
    
    fig2 = px.line(
        prod_line,
        x='tahun',
        y='volume',
        color='jenis_kayu',
        title='Tren Produksi',
        markers=True,
        color_discrete_map={'Jati': '#2e7d32', 'Rimba': '#66bb6a'}
    )
    fig2.update_traces(line=dict(width=3), marker=dict(size=12))
    fig2 = apply_chart_settings(fig2, True)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Grafik Tren Produksi</h4>
        <ul>
            <li>Tren produksi menunjukkan <strong>penurunan yang konsisten</strong> dari 2016 ke 2017.</li>
            <li>Penurunan <strong>Kayu Jati</strong> lebih tajam dibandingkan <strong>Kayu Rimba</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Tabel Data Lengkap")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    st.markdown("**📊 Data Produksi per Jenis Kayu**")
    st.dataframe(
        production_data.style.format({
            'volume_2016': '{:,.2f}',
            'volume_2017': '{:,.2f}',
            'perubahan_persen': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    fig_detail = px.bar(
        production_data,
        x='jenis_kayu',
        y=['volume_2016', 'volume_2017'],
        barmode='group',
        title='Detail Produksi per Jenis Kayu',
        labels={'value': 'Volume (m³)', 'variable': 'Tahun'},
        color_discrete_map={'volume_2016': '#2e7d32', 'volume_2017': '#66bb6a'}
    )
    fig_detail.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    fig_detail = apply_chart_settings(fig_detail, True, 350)
    st.plotly_chart(fig_detail, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box" style="border-left-color: #1565c0;">
        <h4>📌 Analisis Data Produksi</h4>
        <ul>
            <li><strong>Jati</strong> mendominasi produksi dengan kontribusi <strong>70-75%</strong> dari total produksi.</li>
            <li>Rekomendasi: <strong>Rehabilitasi tegakan jati</strong> dan peningkatan <strong>silvikultur</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**📊 Ringkasan Produksi**")
    summary_prod = pd.DataFrame({
        'Keterangan': ['Total Produksi 2016', 'Total Produksi 2017', 'Perubahan Produksi'],
        'Nilai': [
            f"{total_2016:,.2f} m³",
            f"{total_2017:,.2f} m³",
            f"{perubahan_total:.2f}%"
        ]
    })
    st.dataframe(summary_prod, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <h4>💡 Insight Penting</h4>
        <ul>
            <li>Total produksi kayu mengalami <strong>penurunan sebesar 13,35%</strong> dalam satu tahun.</li>
            <li><strong>Kayu Jati</strong> yang merupakan komoditas unggulan mengalami penurunan lebih besar.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== MASTER DATA ====================
elif menu == "📋 Master Data":
    st.markdown('<h1 class="section-title">📋 Master Data</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="analysis-box">
        <h4>📊 Ringkasan Data</h4>
        <ul>
            <li>Halaman ini menyajikan <strong>seluruh data</strong> KPH Saradan secara lengkap.</li>
            <li>Data terdiri dari <strong>3 kategori</strong>: Kelas Umur, Produksi Kayu, dan Finansial.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🏢 Informasi Umum KPH")
    st.markdown("""
    | **Parameter** | **Nilai / Deskripsi** |
    |--------------|----------------------|
    | **Nama KPH** | KPH Saradan |
    | **Lokasi** | Madiun, Bojonegoro, Ngawi, Nganjuk |
    | **Luas Total** | 37.934,66 Ha |
    | **Tipe Hutan** | Hutan Produksi & Lindung |
    | **Kelas Perusahaan** | Jati (Tectona grandis) |
    | **Topografi** | Datar hingga Bergelombang (15% – 25%) |
    | **Tipe Iklim** | Tipe D (Schmidt-Ferguson) |
    """)
    
    st.markdown("---")
    
    st.subheader("🌲 Data Sebaran Kelas Umur")
    
    fig_kelas = px.bar(
        forest_data,
        x='kelas_umur',
        y='luas_ha',
        title='Sebaran Luas per Kelas Umur',
        color='kelas_umur',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        text='luas_ha'
    )
    fig_kelas.update_traces(texttemplate='%{text:,.0f}', textposition='outside', width=0.7)
    fig_kelas = apply_chart_settings(fig_kelas, True, 350)
    st.plotly_chart(fig_kelas, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Sebaran Kelas Umur</h4>
        <ul>
            <li><strong>KU III (21-30 tahun)</strong> mendominasi dengan luas <strong>5.897,50 Ha</strong>.</li>
            <li>Kelas umur tua (KU VI-VIII) memiliki luas yang <strong>cenderung menurun</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        forest_data.style.format({
            'luas_ha': '{:,.2f}',
            'persentase': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"📌 Total {len(forest_data)} kelas umur | Total luas: {forest_data['luas_ha'].sum():,.2f} Ha")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🪵 Data Produksi Kayu")
    
    fig_prod = px.bar(
        production_data,
        x='jenis_kayu',
        y=['volume_2016', 'volume_2017'],
        barmode='group',
        title='Data Produksi per Jenis Kayu',
        labels={'value': 'Volume (m³)', 'variable': 'Tahun'},
        color_discrete_map={'volume_2016': '#2e7d32', 'volume_2017': '#66bb6a'}
    )
    fig_prod.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    fig_prod = apply_chart_settings(fig_prod, True, 350)
    st.plotly_chart(fig_prod, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Produksi Kayu</h4>
        <ul>
            <li><strong>Jati</strong> adalah komoditas utama dengan volume produksi terbesar.</li>
            <li>Total produksi 2017: <strong>8.414,81 m³</strong> (turun 13,35% dari 2016).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        production_data.style.format({
            'volume_2016': '{:,.2f}',
            'volume_2017': '{:,.2f}',
            'perubahan_persen': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"📌 Total 2 jenis kayu | Total produksi 2017: {production_data['volume_2017'].sum():,.2f} m³")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("💰 Data Kelayakan Finansial")
    
    fig_fin = px.bar(
        financial_data,
        x='indikator',
        y=['skenario_a', 'skenario_b'],
        barmode='group',
        title='Perbandingan Skenario A vs B',
        labels={'value': 'Nilai', 'variable': 'Skenario'},
        color_discrete_map={'skenario_a': '#ff9800', 'skenario_b': '#2e7d32'}
    )
    fig_fin.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    fig_fin = apply_chart_settings(fig_fin, True, 350)
    st.plotly_chart(fig_fin, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Kelayakan Finansial</h4>
        <ul>
            <li><strong>Skenario B (Hijau)</strong> lebih unggul di semua indikator.</li>
            <li><strong>NPV</strong> meningkat dari <strong>Rp 4.078 Juta</strong> menjadi <strong>Rp 7.058 Juta</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        financial_data.style.format({
            'skenario_a': '{:,.0f}',
            'skenario_b': '{:,.0f}',
            'selisih': '{:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption("📌 Perbandingan skenario A (Tradisional) vs skenario B (Hijau Terintegrasi)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <h4>💡 Insight Penting</h4>
        <ul>
            <li><strong>Skenario B (Hijau Terintegrasi)</strong> lebih layak secara finansial.</li>
            <li>NPV meningkat <strong>73,07%</strong> dengan skenario hijau.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== SIMULASI FINANSIAL ====================
elif menu == "⚙️ Simulasi Finansial":
    st.markdown('<h1 class="section-title">⚙️ Simulasi Finansial</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="analysis-box">
        <h4>📊 Analisis Simulasi Finansial</h4>
        <ul>
            <li>Simulasi ini membandingkan <strong>2 skenario</strong>: Tradisional vs Hijau Terintegrasi.</li>
            <li><strong>Skenario A (Tradisional)</strong>: Hanya mengandalkan penjualan kayu.</li>
            <li><strong>Skenario B (Hijau Terintegrasi)</strong>: Penjualan kayu + insentif karbon.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎛️ Kontrol Parameter Simulasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Parameter Utama")
        luas_area = st.slider(
            "Luas Kawasan Simulasi (Ha)",
            min_value=1000.0,
            max_value=50000.0,
            value=float(forest_data['luas_ha'].sum()),
            step=100.0
        )
        daur_tebang = st.slider(
            "Daur Tebang Jati (Tahun)",
            min_value=40,
            max_value=80,
            value=60,
            step=5
        )
        discount_rate = st.slider(
            "Suku Bunga/Discount Rate (%)",
            min_value=5.0,
            max_value=25.0,
            value=15.0,
            step=0.5
        )
    
    with col2:
        st.subheader("💰 Parameter Ekonomi")
        harga_kayu = st.number_input(
            "Harga Jual Log Kayu Jati (Rp/m³)",
            min_value=1000000,
            max_value=10000000,
            value=3500000,
            step=100000,
            format="%d"
        )
        biaya_produksi = st.number_input(
            "Biaya Produksi (Rp/m³)",
            min_value=500000,
            max_value=5000000,
            value=1500000,
            step=50000,
            format="%d"
        )
        harga_karbon = st.selectbox(
            "Harga Karbon (Rp/tCO2e)",
            options=[50000, 100000, 150000, 200000, 250000],
            index=2
        )
    
    st.markdown("---")
    st.subheader("📊 Hasil Simulasi")
    
    with st.spinner("⏳ Menghitung simulasi..."):
        time.sleep(0.3)
        total_luas = luas_area
        volume_per_ha = 120 * (1 + (daur_tebang - 60) / 200)
        total_volume = total_luas * volume_per_ha
        total_pendapatan = total_volume * harga_kayu
        total_biaya = total_volume * biaya_produksi
        laba_kotor = total_pendapatan - total_biaya
        npv = laba_kotor / (1 + discount_rate/100)
        serapan = total_luas * 18.5
        nilai_karbon = serapan * harga_karbon
        total_pendapatan_b = total_pendapatan + nilai_karbon
        laba_kotor_b = total_pendapatan_b - total_biaya
        npv_b = laba_kotor_b / (1 + discount_rate/100)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Luas", f"{total_luas:,.0f} Ha")
    with col2:
        st.metric("Total Volume", f"{total_volume:,.0f} m³")
    with col3:
        st.metric("NPV (Tanpa Karbon)", f"Rp {npv/1e6:,.0f} Juta")
    with col4:
        st.metric("NPV (Dengan Karbon)", f"Rp {npv_b/1e6:,.0f} Juta",
                  delta=f"+Rp {(npv_b-npv)/1e6:,.0f} Juta")
    
    st.markdown("---")
    st.subheader("📈 Visualisasi Perbandingan NPV")
    
    sim_data = pd.DataFrame({
        'Skenario': ['Tradisional', 'Hijau Terintegrasi'],
        'NPV (Rp Juta)': [npv/1e6, npv_b/1e6]
    })
    
    fig = px.bar(
        sim_data,
        x='Skenario',
        y='NPV (Rp Juta)',
        title='Perbandingan NPV',
        color='Skenario',
        color_discrete_map={'Tradisional': '#ff9800', 'Hijau Terintegrasi': '#2e7d32'},
        text='NPV (Rp Juta)'
    )
    fig.update_traces(texttemplate='Rp %{text:,.0f} Juta', textposition='outside', width=0.5)
    fig = apply_chart_settings(fig, True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Grafik Perbandingan NPV</h4>
        <ul>
            <li><strong>Skenario B (Hijau)</strong> memiliki NPV lebih tinggi dari skenario A.</li>
            <li>Selisih NPV antara kedua skenario adalah <strong>Rp {(npv_b-npv)/1e6:,.0f} Juta</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Tabel Data Hasil Simulasi")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    hasil_simulasi = pd.DataFrame({
        'Parameter': ['Total Luas', 'Total Volume', 'NPV Tanpa Karbon', 'NPV Dengan Karbon'],
        'Nilai': [
            f"{total_luas:,.0f} Ha",
            f"{total_volume:,.0f} m³",
            f"Rp {npv/1e6:,.0f} Juta",
            f"Rp {npv_b/1e6:,.0f} Juta"
        ]
    })
    st.dataframe(hasil_simulasi, use_container_width=True, hide_index=True)
    
    st.markdown("**📊 Perbandingan Skenario**")
    perbandingan = pd.DataFrame({
        'Indikator': ['NPV (Rp Juta)', 'IRR (%)', 'BCR'],
        'Skenario A (Tradisional)': [
            f"{npv/1e6:,.0f}",
            f"{18.0:.2f}",
            f"{1.45:.2f}"
        ],
        'Skenario B (Hijau)': [
            f"{npv_b/1e6:,.0f}",
            f"{20.0:.2f}",
            f"{1.82:.2f}"
        ]
    })
    st.dataframe(perbandingan, use_container_width=True, hide_index=True)
    
    st.caption("📌 Skenario B (Hijau Terintegrasi) memberikan nilai NPV yang lebih tinggi")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <h4>💡 Kesimpulan Simulasi</h4>
        <ul>
            <li><strong>Skenario B (Hijau Terintegrasi)</strong> lebih layak secara finansial.</li>
            <li>NPV meningkat <strong>73,07%</strong> dengan skenario hijau.</li>
            <li>BCR meningkat dari <strong>1,45</strong> menjadi <strong>1,82</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Simulasi selesai!")

# ==================== DASHBOARD SUMMARY ====================
elif menu == "📈 Dashboard Summary":
    st.markdown('<h1 class="section-title">📈 Dashboard Summary</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class="analysis-box">
        <h4>📊 Ringkasan Keseluruhan Dashboard</h4>
        <ul>
            <li><strong>KPH Saradan</strong> memiliki luas total <strong>37.934,66 Ha</strong> dengan komoditas utama <strong>Jati</strong>.</li>
            <li>Sebaran luas <strong>didominasi oleh kelas umur KU III</strong> dengan luas 5.897,50 Ha.</li>
            <li>Produksi kayu mengalami <strong>penurunan sebesar 13,35%</strong> dari tahun 2016 ke 2017.</li>
            <li><strong>Skenario B (Hijau Terintegrasi)</strong> memberikan keuntungan <strong>Rp 2.980 Juta lebih tinggi</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Ringkasan Metrik Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌳 Total Luas", f"{forest_data['luas_ha'].sum():,.2f} Ha")
    with col2:
        st.metric("🪵 Produksi 2017", f"{production_data['volume_2017'].sum():,.2f} m³")
    with col3:
        npv_a = financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_a'].values[0]
        st.metric("💵 NPV Tradisional", f"Rp {npv_a:,.0f} Juta")
    with col4:
        npv_b = financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_b'].values[0]
        st.metric("🌿 NPV Hijau", f"Rp {npv_b:,.0f} Juta", delta=f"+Rp {npv_b-npv_a:,.0f} Juta")
    
    st.markdown("---")
    
    st.subheader("📊 Distribusi Luas per Kelas Umur")
    
    fig1 = px.pie(
        forest_data,
        values='luas_ha',
        names='kelas_umur',
        title='Distribusi Luas per Kelas Umur',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        hole=0.3
    )
    fig1.update_traces(textinfo='percent+label')
    fig1 = apply_chart_settings(fig1, True, 400)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Distribusi Luas</h4>
        <ul>
            <li><strong>KU III (21-30 tahun)</strong> mendominasi dengan <strong>27,69%</strong> dari total luas.</li>
            <li>KU I - KU IV menguasai <strong>76%</strong> dari total kawasan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Produksi 2016 vs 2017")
    
    prod_melted = production_data.melt(
        id_vars=['jenis_kayu'],
        value_vars=['volume_2016', 'volume_2017'],
        var_name='tahun',
        value_name='volume'
    )
    
    fig2 = px.bar(
        prod_melted,
        x='jenis_kayu',
        y='volume',
        color='tahun',
        barmode='group',
        title='Perbandingan Produksi 2016 vs 2017',
        text='volume',
        color_discrete_map={'volume_2016': '#2e7d32', 'volume_2017': '#66bb6a'}
    )
    fig2.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig2 = apply_chart_settings(fig2, True, 400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class="analysis-box-green">
        <h4>📌 Analisis Produksi</h4>
        <ul>
            <li><strong>Jati</strong> tetap menjadi komoditas utama.</li>
            <li>Terjadi <strong>penurunan produksi</strong> pada tahun 2017.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Tabel Data Lengkap")
    
    st.markdown("### 🌲 Data Kelas Umur")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        forest_data.style.format({
            'luas_ha': '{:,.2f}',
            'persentase': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"📌 Total {len(forest_data)} kelas umur")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🪵 Data Produksi Kayu")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        production_data.style.format({
            'volume_2016': '{:,.2f}',
            'volume_2017': '{:,.2f}',
            'perubahan_persen': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption("📌 Data produksi 2016-2017")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 💰 Data Kelayakan Finansial")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    st.dataframe(
        financial_data.style.format({
            'skenario_a': '{:,.0f}',
            'skenario_b': '{:,.0f}',
            'selisih': '{:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    st.caption("📌 Perbandingan skenario A dan B")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("💡 Kesimpulan Akhir")
    
    kesimpulan_data = pd.DataFrame({
        'Indikator': ['NPV', 'IRR', 'BCR'],
        'Skenario A (Tradisional)': ['Rp 4.078 Juta', '18.00%', '1.45'],
        'Skenario B (Hijau)': ['Rp 7.058 Juta', '20.00%', '1.82'],
        'Status': ['✅ Meningkat 73%', '✅ Melewati batas modal', '✅ Efisiensi biaya naik']
    })
    
    st.dataframe(kesimpulan_data, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="analysis-box" style="border-left-color: #2e7d32;">
        <h4>📊 Kesimpulan Akhir</h4>
        <ul>
            <li><strong>Skenario B (Hijau Terintegrasi)</strong> lebih layak secara finansial.</li>
            <li>Insentif karbon memberikan <strong>tambahan keuntungan signifikan</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Dashboard KPH Saradan siap digunakan untuk analisis dan simulasi!")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>🌱 Dashboard KPH Saradan | Data Tahun 2026</p>
    <p>Dibangun untuk Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan</p>
    <p style="font-size: 0.7rem; color: #999;">© 2026 - Kelompok KPH Saradan</p>
</div>
""", unsafe_allow_html=True)