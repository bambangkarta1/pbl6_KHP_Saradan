import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import os

# ============================================
# 1. KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="KPH Saradan - Dashboard Kehutanan",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 2. DATA DASAR (TIDAK BERUBAH)
# ============================================

# Data Kelas Umur (data statis, tidak berubah)
forest_data_base = pd.DataFrame({
    'kelas_umur': ['KU I', 'KU II', 'KU III', 'KU IV', 'KU V', 'KU VI', 'KU VII', 'KU VIII'],
    'kisaran_umur': ['1-10 Tahun', '11-20 Tahun', '21-30 Tahun', '31-40 Tahun', 
                     '41-50 Tahun', '51-60 Tahun', '61-70 Tahun', '71-80 Tahun'],
    'luas_ha': [2875.20, 3157.05, 5897.50, 4226.15, 2035.30, 1210.80, 1048.10, 801.05],
    'persentase': [13.50, 14.83, 27.69, 19.85, 9.56, 5.69, 4.92, 3.76]
})

# Data Produksi Kayu
production_data = pd.DataFrame({
    'jenis_kayu': ['Jati', 'Rimba'],
    'volume_2016': [7303.89, 2407.34],
    'volume_2017': [6101.41, 2313.40],
    'perubahan_persen': [-16.46, -3.90]
})

# ============================================
# 3. CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1a5e3a;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f7f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
        margin: 0.5rem 0;
    }
    .stApp {
        background-color: #f8faf8;
    }
    .sidebar-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .sidebar-title {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a5e3a;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }
    .sidebar-subtitle {
        text-align: center;
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .group-member {
        font-size: 0.9rem;
        padding: 0.3rem 0;
        border-bottom: 1px solid #e8f0e8;
    }
    .group-member:last-child {
        border-bottom: none;
    }
    .course-info {
        background-color: #e8f5e9;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    .divider-custom {
        border: none;
        border-top: 2px solid #c8e6c9;
        margin: 0.8rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. SIDEBAR DENGAN PARAMETER KONTROL
# ============================================
with st.sidebar:
    # --- LOGO UNISBA ---
    try:
        logo_path = "logo-unisba.png"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background-color: #1a5e3a; color: white; border-radius: 0.5rem;">
                <h3 style="color: white; margin: 0;">UNISBA</h3>
                <p style="color: #a5d6a7; margin: 0;">Universitas Islam Bandung</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background-color: #1a5e3a; color: white; border-radius: 0.5rem;">
            <h3 style="color: white; margin: 0;">UNISBA</h3>
            <p style="color: #a5d6a7; margin: 0;">Universitas Islam Bandung</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    
    # --- JUDUL SIDEBAR ---
    st.markdown('<p class="sidebar-title">🌳 KPH Saradan</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">Dashboard Kehutanan</p>', unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    
    # --- IDENTITAS KELOMPOK ---
    st.markdown("### 👥 Kelompok")
    st.markdown("""
    <div class="group-member">👤 Arif Hamdani (10090224008)</div>
    <div class="group-member">👤 Bambang Karta Wijaya (10090224025)</div>
    <div class="group-member">👤 Moh Bayu Mustofa (10090224030)</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    
    # --- MATA KULIAH & DOSEN ---
    st.markdown("""
    <div class="course-info">
        <strong>📚 Mata Kuliah</strong><br>
        Ekonomi Sumber Daya Alam dan Lingkungan
        <br><br>
        <strong>👨‍🏫 Dosen Pengampu</strong><br>
        Yuhka Sundaya, S.E., M.Si.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    
    # ============================================
    # ⚙️ PARAMETER KONTROL (NILAI AKAN DIGUNAKAN)
    # ============================================
    st.markdown("### ⚙️ Parameter Kontrol")
    
    # 1. SLIDER LUAS KAWASAN - akan mengubah metrik luas
    luas_area = st.slider(
        "Luas Kawasan Simulasi (Ha)",
        min_value=1000.0,
        max_value=50000.0,
        value=float(forest_data_base['luas_ha'].sum()),
        step=100.0,
        help="Mengubah total luas kawasan yang disimulasikan"
    )
    
    # 2. SLIDER DAUR TEBANG - akan mengubah proyeksi produksi
    daur_tebang = st.slider(
        "Daur Tebang Jati (Tahun)",
        min_value=40,
        max_value=80,
        value=60,
        step=5,
        help="Mengubah umur optimal tebang habis"
    )
    
    # 3. SLIDER DISCOUNT RATE - akan mengubah NPV, IRR, BCR
    discount_rate = st.slider(
        "Suku Bunga/Discount Rate (%)",
        min_value=5.0,
        max_value=25.0,
        value=15.0,
        step=0.5,
        help="Mengubah tingkat diskonto untuk analisis NPV"
    )
    
    # 4. HARGA KAYU - akan mengubah pendapatan
    harga_kayu = st.number_input(
        "Harga Kayu (Rp/m³)",
        min_value=1000000,
        max_value=10000000,
        value=3500000,
        step=100000,
        format="%d",
        help="Mengubah harga jual kayu per meter kubik"
    )
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)
    st.caption("📊 Data KPH Saradan 2026")
    
    # ============================================
    # TAMPILKAN NILAI PARAMETER YANG SEDANG AKTIF
    # ============================================
    with st.expander("📋 Nilai Parameter Aktif"):
        st.markdown(f"""
        - **Luas Kawasan**: {luas_area:,.0f} Ha
        - **Daur Tebang**: {daur_tebang} Tahun
        - **Discount Rate**: {discount_rate:.1f}%
        - **Harga Kayu**: Rp {harga_kayu:,.0f}/m³
        """)

# ============================================
# 5. DATA YANG BERUBAH SESUAI PARAMETER
# ============================================

# --- DATA LUAS YANG DISESUAIKAN ---
# Skala proporsi berdasarkan luas_area
skala_luas = luas_area / forest_data_base['luas_ha'].sum()
forest_data = forest_data_base.copy()
forest_data['luas_ha'] = forest_data_base['luas_ha'] * skala_luas
forest_data['persentase'] = (forest_data['luas_ha'] / forest_data['luas_ha'].sum()) * 100

# --- DATA PRODUKSI YANG DISESUAIKAN ---
# Produksi dipengaruhi oleh daur_tebang (semakin panjang daur, volume per Ha semakin besar)
faktor_daur = 1 + (daur_tebang - 60) / 200  # 60 tahun = baseline
production_data_adj = production_data.copy()
production_data_adj['volume_2017'] = production_data['volume_2017'] * faktor_daur
production_data_adj['volume_2016'] = production_data['volume_2016'] * faktor_daur

# --- DATA FINANSIAL YANG DISESUAIKAN ---
# NPV dipengaruhi oleh discount_rate dan harga_kayu
total_luas = forest_data['luas_ha'].sum()
volume_per_ha = 120 * faktor_daur  # volume per Ha dipengaruhi daur
total_volume = total_luas * volume_per_ha
total_pendapatan = total_volume * harga_kayu
total_biaya = total_volume * 1500000  # biaya produksi tetap Rp 1.5 Juta/m³
laba_kotor = total_pendapatan - total_biaya

# Skenario A (tradisional)
npv_a = laba_kotor / (1 + discount_rate/100)

# Skenario B (dengan karbon)
serapan_karbon = total_luas * 18.5
nilai_karbon = serapan_karbon * 150000
total_pendapatan_b = total_pendapatan + nilai_karbon
laba_kotor_b = total_pendapatan_b - total_biaya
npv_b = laba_kotor_b / (1 + discount_rate/100)

# IRR dan BCR (perkiraan)
irr_a = 18.0 + (discount_rate - 15) * 0.2  # berubah seiring discount rate
irr_b = 20.0 + (discount_rate - 15) * 0.2
bcr_a = total_pendapatan / total_biaya if total_biaya > 0 else 0
bcr_b = total_pendapatan_b / total_biaya if total_biaya > 0 else 0

financial_data = pd.DataFrame({
    'indikator': ['NPV (Rp Juta)', 'IRR (%)', 'BCR'],
    'skenario_a': [npv_a / 1e6, irr_a, bcr_a],
    'skenario_b': [npv_b / 1e6, irr_b, bcr_b],
    'selisih': [(npv_b - npv_a) / 1e6, irr_b - irr_a, bcr_b - bcr_a]
})

# ============================================
# 6. HEADER UTAMA
# ============================================
st.markdown('<h1 class="main-header">🌳 Dashboard KPH Saradan</h1>', unsafe_allow_html=True)
st.markdown(f"*Kesatuan Pemangkuan Hutan Saradan - Wilayah Kerja: Madiun, Bojonegoro, Ngawi, Nganjuk*")
st.markdown("---")

# ============================================
# 7. METRIK UTAMA (BERUBAH SESUAI PARAMETER)
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Luas Kawasan",
        value=f"{forest_data['luas_ha'].sum():,.2f} Ha",
        delta=f"{((forest_data['luas_ha'].sum() / forest_data_base['luas_ha'].sum()) - 1) * 100:.1f}% dari baseline"
    )

with col2:
    st.metric(
        label="Komoditas Utama",
        value="Jati (Tectona grandis)",
        delta=f"Daur {daur_tebang} Tahun"
    )

with col3:
    total_2017 = production_data_adj['volume_2017'].sum()
    total_2016 = production_data_adj['volume_2016'].sum()
    perubahan = ((total_2017 / total_2016) - 1) * 100
    st.metric(
        label="Total Produksi Kayu 2017",
        value=f"{total_2017:,.2f} m³",
        delta=f"{perubahan:.1f}% (Diskonto {discount_rate:.0f}%)"
    )

with col4:
    st.metric(
        label="NPV Skenario B",
        value=f"Rp {npv_b/1e6:,.0f} Juta",
        delta=f"Rp {(npv_b - npv_a)/1e6:,.0f} Juta lebih tinggi"
    )

# ============================================
# 8. SEBARAN KELAS UMUR (BERUBAH LUASNYA)
# ============================================
st.markdown("---")
st.subheader("📊 Sebaran Luas Berdasarkan Kelas Umur")
st.caption(f"*Total luas: {forest_data['luas_ha'].sum():,.0f} Ha (dari parameter kontrol)*")

tab1, tab2 = st.tabs(["📈 Chart Interaktif", "📋 Data Tabel"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = px.pie(
            forest_data,
            values='luas_ha',
            names='kelas_umur',
            title='Distribusi Luas per Kelas Umur',
            color_discrete_sequence=px.colors.sequential.Greens_r,
            hover_data={'persentase': ':.2f%'}
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(
            forest_data,
            x='kelas_umur',
            y='luas_ha',
            title='Luas Area per Kelas Umur (Ha)',
            color='persentase',
            color_continuous_scale='Greens',
            text='luas_ha'
        )
        fig_bar.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
        fig_bar.update_layout(yaxis_title="Luas (Ha)")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.dataframe(
        forest_data.style.format({
            'luas_ha': '{:,.2f}',
            'persentase': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )

# ============================================
# 9. PRODUKSI KAYU (BERUBAH VOLUMENYA)
# ============================================
st.markdown("---")
st.subheader("🪵 Produksi Kayu (2016 vs 2017)")
st.caption(f"*Daur tebang: {daur_tebang} tahun | Harga kayu: Rp {harga_kayu:,.0f}/m³*")

col1, col2 = st.columns(2)

with col1:
    prod_melted = production_data_adj.melt(
        id_vars=['jenis_kayu'],
        value_vars=['volume_2016', 'volume_2017'],
        var_name='tahun',
        value_name='volume'
    )
    
    fig_prod = px.bar(
        prod_melted,
        x='jenis_kayu',
        y='volume',
        color='tahun',
        barmode='group',
        title='Perbandingan Volume Produksi 2016 vs 2017',
        text='volume',
        color_discrete_map={'volume_2016': '#2e7d32', 'volume_2017': '#66bb6a'}
    )
    fig_prod.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    st.plotly_chart(fig_prod, use_container_width=True)

with col2:
    for _, row in production_data_adj.iterrows():
        perubahan = ((row['volume_2017'] / row['volume_2016']) - 1) * 100
        warna = 'red' if perubahan < 0 else 'green'
        st.markdown(f"""
        <div class="metric-card">
            <h4>{row['jenis_kayu']}</h4>
            <p>2016: {row['volume_2016']:,.2f} m³ | 2017: {row['volume_2017']:,.2f} m³</p>
            <p style="color: {warna}; font-weight: bold;">
                Perubahan: {perubahan:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 10. ANALISIS KARBON & KELAYAKAN (BERUBAH SEMUA)
# ============================================
st.markdown("---")
st.subheader("🌿 Analisis Karbon & Kelayakan Finansial")
st.caption(f"*Discount Rate: {discount_rate:.1f}% | Harga Kayu: Rp {harga_kayu:,.0f}/m³*")

col1, col2 = st.columns(2)

with col1:
    with st.expander("**📊 Parameter Stok Karbon**", expanded=True):
        st.markdown(f"""
        - **Luas Kawasan**: {total_luas:,.0f} Ha
        - **Stok Karbon Minimum**: 348.08 Ton C/Ha
        - **Stok Karbon Maksimum**: 520.46 Ton C/Ha
        - **Serapan Tahunan**: 18.50 tCO2e/Ha/Tahun
        - **Total Serapan**: {total_luas * 18.5:,.0f} tCO2e/tahun
        - **Harga Karbon**: Rp 150,000 / tCO2e (NEK)
        """)
    
    st.markdown("### 🔢 Simulasi Cepat")
    simulasi_luas = st.number_input("Luas untuk Simulasi (Ha)", value=int(total_luas/10), step=100, key="sim_luas")
    serapan = 18.5
    total_serapan = simulasi_luas * serapan
    estimasi_pendapatan = total_serapan * 150000
    
    st.metric(
        label="Estimasi Serapan Karbon per Tahun",
        value=f"{total_serapan:,.0f} tCO2e",
        delta=f"≈ Rp {estimasi_pendapatan:,.0f} / tahun"
    )

with col2:
    st.markdown("### 💰 Kelayakan Finansial")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Skenario A\n(Tradisional)', 'Skenario B\n(Hijau Terintegrasi)'],
        y=[
            financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_a'].values[0],
            financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_b'].values[0]
        ],
        name='NPV (Rp Juta)',
        marker_color=['#ff9800', '#2e7d32'],
        text=[
            f"Rp {financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_a'].values[0]:,.0f} Juta",
            f"Rp {financial_data[financial_data['indikator'] == 'NPV (Rp Juta)']['skenario_b'].values[0]:,.0f} Juta"
        ],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'Perbandingan NPV (Discount Rate: {discount_rate:.1f}%)',
        yaxis_title='NPV (Rp Juta)',
        showlegend=False,
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(
        financial_data.style.format({
            'skenario_a': '{:,.0f}',
            'skenario_b': '{:,.0f}',
            'selisih': '{:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )

# ============================================
# 11. FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🌱 Dashboard KPH Saradan | Data Tahun 2026</p>
    <p>Dibangun untuk Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan</p>
    <p style="font-size: 0.8rem; color: #999;">
        Dosen Pengampu: Yuhka Sundaya, S.E., M.Si.
    </p>
    <hr style="border: none; border-top: 1px solid #ddd; margin: 0.5rem auto; width: 50%;">
    <p style="font-size: 0.8rem; color: #aaa;">
        © 2026 - Kelompok KPH Saradan
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 12. RUN
# ============================================
if __name__ == "__main__":
    pass