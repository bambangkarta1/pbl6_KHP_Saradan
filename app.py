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
    .chart-control {
        background-color: #f5faf5;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0ece0;
        margin-bottom: 1rem;
    }
    .group-card {
        background-color: #f0f7f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
        height: 100%;
        text-align: center;
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
# 5. SIDEBAR (HANYA NAVIGASI)
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
            "⚙️ Parameter Simulasi",
            "📈 Dashboard Summary"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown('<hr class="divider-custom">', unsafe_allow_html=True)

# ============================================
# 6. FUNGSI KONTROL GRAFIK
# ============================================

COLOR_THEMES = {
    "Greens": px.colors.sequential.Greens_r,
    "Blues": px.colors.sequential.Blues_r,
    "Reds": px.colors.sequential.Reds_r,
    "Viridis": px.colors.sequential.Viridis,
    "Plasma": px.colors.sequential.Plasma,
    "Cividis": px.colors.sequential.Cividis,
    "Turbo": px.colors.sequential.Turbo,
    "Sunset": px.colors.sequential.Sunset,
    "Magenta": px.colors.sequential.Magenta_r,
    "Teal": px.colors.sequential.Teal_r,
    "Oranges": px.colors.sequential.Oranges_r,
    "Purples": px.colors.sequential.Purples_r,
}

def create_chart_controls(chart_type_default="Bar"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox(
            "📊 Tipe Grafik",
            options=["Bar", "Pie", "Line", "Scatter", "Area"],
            index=["Bar", "Pie", "Line", "Scatter", "Area"].index(chart_type_default)
        )
    
    with col2:
        color_theme = st.selectbox(
            "🎨 Tema Warna",
            options=list(COLOR_THEMES.keys()),
            index=0
        )
    
    with col3:
        show_labels = st.checkbox("🏷️ Tampilkan Label", value=True)
        show_grid = st.checkbox("📏 Tampilkan Grid", value=True)
    
    return chart_type, color_theme, show_labels, show_grid

def get_color_theme(theme_name):
    if theme_name in COLOR_THEMES:
        return COLOR_THEMES[theme_name]
    return px.colors.sequential.Greens_r

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

def create_flexible_chart(data, x_col, y_col, chart_type, color_theme,
                          show_labels=True, title="", color_col=None,
                          text_col=None, group_col=None, barmode='group'):
    colors = get_color_theme(color_theme)

    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Data tidak tersedia", showarrow=False)
        return fig

    if chart_type == "Pie":
        fig = px.pie(
            data,
            values=y_col,
            names=x_col if not color_col else color_col,
            title=title,
            color_discrete_sequence=colors,
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label')

    elif chart_type == "Bar":
        if color_col and color_col in data.columns:
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                color_discrete_sequence=colors,
                text=text_col if show_labels and text_col else None,
                barmode=barmode
            )
        else:
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                title=title,
                color_discrete_sequence=colors,
                text=text_col if show_labels and text_col else None
            )

        fig.update_traces(
            width=0.7,
            marker=dict(line=dict(width=1, color='white'))
        )

        if show_labels and text_col:
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')

        fig.update_layout(
            bargap=0.15,
            bargroupgap=0.1
        )

    elif chart_type == "Line":
        fig = go.Figure()

        if color_col and color_col in data.columns and x_col != color_col:
            unique_groups = data[color_col].unique()
            x_labels = sorted(data[x_col].unique().tolist())

            for i, group in enumerate(unique_groups):
                group_data = data[data[color_col] == group].copy()
                if len(group_data) < 2:
                    continue
                color_idx = i % len(colors)
                x_numeric = list(range(len(group_data)))
                y_values = group_data[y_col].tolist()
                x_labels_group = group_data[x_col].tolist()

                fig.add_trace(go.Scatter(
                    x=x_numeric,
                    y=y_values,
                    mode='lines+markers+text' if show_labels else 'lines+markers',
                    name=str(group),
                    line=dict(width=4, color=colors[color_idx]),
                    marker=dict(size=12, color=colors[color_idx], symbol='circle',
                               line=dict(width=2, color='white')),
                    text=[f'{v:,.0f}' for v in y_values] if show_labels else None,
                    textposition='top center',
                ))

                fig.update_layout(
                    xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(len(x_labels_group))),
                        ticktext=x_labels_group
                    )
                )
        else:
            x_numeric = list(range(len(data)))
            x_labels = data[x_col].tolist()
            y_values = data[y_col].tolist()

            fig.add_trace(go.Scatter(
                x=x_numeric,
                y=y_values,
                mode='lines+markers+text' if show_labels else 'lines+markers',
                name=title if title else 'Data',
                line=dict(width=4, color=colors[0]),
                marker=dict(size=12, color=colors[0], symbol='circle',
                           line=dict(width=2, color='white')),
                text=[f'{v:,.0f}' for v in y_values] if show_labels else None,
                textposition='top center',
            ))

            fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=x_numeric,
                    ticktext=x_labels
                )
            )

        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            showlegend=True
        )

    elif chart_type == "Scatter":
        fig = go.Figure()

        if color_col and color_col in data.columns and x_col != color_col:
            unique_groups = data[color_col].unique()

            for i, group in enumerate(unique_groups):
                group_data = data[data[color_col] == group].copy()
                if len(group_data) < 2:
                    continue
                color_idx = i % len(colors)
                x_numeric = list(range(len(group_data)))
                y_values = group_data[y_col].tolist()
                x_labels_group = group_data[x_col].tolist()

                fig.add_trace(go.Scatter(
                    x=x_numeric,
                    y=y_values,
                    mode='lines',
                    name=f"Tren {group}",
                    line=dict(width=3, color=colors[color_idx], dash='solid'),
                    showlegend=False
                ))

                fig.add_trace(go.Scatter(
                    x=x_numeric,
                    y=y_values,
                    mode='markers+text' if show_labels else 'markers',
                    name=str(group),
                    marker=dict(size=18, color=colors[color_idx], symbol='circle',
                               line=dict(width=3, color='white')),
                    text=[f'{v:,.0f}' for v in y_values] if show_labels else None,
                    textposition='top center',
                ))

                fig.update_layout(
                    xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(len(x_labels_group))),
                        ticktext=x_labels_group
                    )
                )
        else:
            x_numeric = list(range(len(data)))
            x_labels = data[x_col].tolist()
            y_values = data[y_col].tolist()

            fig.add_trace(go.Scatter(
                x=x_numeric,
                y=y_values,
                mode='lines',
                name='Tren',
                line=dict(width=3, color=colors[0], dash='solid'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=x_numeric,
                y=y_values,
                mode='markers+text' if show_labels else 'markers',
                name='Data',
                marker=dict(size=18, color=colors[0], symbol='circle',
                           line=dict(width=3, color='white')),
                text=[f'{v:,.0f}' for v in y_values] if show_labels else None,
                textposition='top center',
            ))

            fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=x_numeric,
                    ticktext=x_labels
                )
            )

        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            showlegend=True
        )

    elif chart_type == "Area":
        if color_col and color_col in data.columns:
            fig = px.area(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                color_discrete_sequence=colors,
                line_shape='linear'
            )
        else:
            fig = px.area(
                data,
                x=x_col,
                y=y_col,
                title=title,
                color_discrete_sequence=colors,
                line_shape='linear'
            )

        fig.update_traces(
            line=dict(width=3),
            opacity=0.7,
            marker=dict(size=8)
        )

    else:
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            title=title,
            color_discrete_sequence=colors
        )

    return fig

# ============================================
# 7. KONTEN HALAMAN
# ============================================

# ==================== BERANDA ====================
if menu == "🏠 Beranda":
    st.title("🏠 Selamat Datang di Eco-Forest Valuation")
    st.markdown("---")
    
    # ==========================================
    # IDENTITAS KELOMPOK - DI ATAS BERANDA
    # ==========================================
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
    # FITUR DAN PREVIEW GRAFIK
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Sistem Valuasi Ekonomi Hutan
        
        Dashboard ini menyajikan data KPH Saradan dengan visualisasi interaktif.
        
        **Fitur Interaktif:**
        - 🔍 Zoom & Pan pada grafik
        - 📊 Pilih tipe grafik (Bar/Pie/Line/Scatter/Area)
        - 🎨 Ubah tema warna (12 tema)
        - 📥 Hover untuk melihat detail data
        - 🏷️ Tampilkan/sembunyikan label
        - 📏 Tampilkan/sembunyikan grid
        """)
    
    with col2:
        st.subheader("📈 Preview Grafik Interaktif")
        
        chart_type, color_theme, show_labels, show_grid = create_chart_controls("Pie")
        
        fig = create_flexible_chart(
            forest_data,
            x_col='kelas_umur',
            y_col='luas_ha',
            chart_type=chart_type,
            color_theme=color_theme,
            show_labels=show_labels,
            title='Distribusi Luas (Preview)',
            color_col='kelas_umur' if chart_type in ['Bar', 'Pie'] else None,
            text_col='luas_ha'
        )
        
        fig = apply_chart_settings(fig, show_grid)
        st.plotly_chart(fig, use_container_width=True, key="preview_chart")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌳 Total Luas", "37.934,66 Ha")
    with col2:
        st.metric("🪵 Komoditas", "Jati")
    with col3:
        st.metric("📅 Tahun Data", "2026")
    with col4:
        st.metric("📍 Wilayah", "4 Kabupaten")

# ==================== PROFIL HUTAN ====================
elif menu == "🌳 Profil Hutan":
    st.title("🌳 Profil Hutan KPH Saradan")
    st.markdown("---")
    
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
        kelas_terbesar = forest_data[forest_data['luas_ha'] == luas_terbesar]['kelas_umur'].values[0]
        st.metric("Total Luas", f"{total_luas:,.2f} Ha")
        st.metric("Luas Terbesar", f"{luas_terbesar:,.2f} Ha", f"Kelas {kelas_terbesar}")
    
    st.markdown("---")
    st.subheader("📊 Sebaran Luas Berdasarkan Kelas Umur")
    
    st.markdown('<div class="chart-control">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        min_luas = float(forest_data['luas_ha'].min())
        max_luas = float(forest_data['luas_ha'].max())
        luas_range = st.slider(
            "📏 Filter Rentang Luas (Ha)",
            min_value=0.0,
            max_value=max_luas * 1.2,
            value=(min_luas * 0.8, max_luas * 1.1),
            step=100.0,
            key="luas_range"
        )
    
    with col2:
        chart_type, color_theme, show_labels, show_grid = create_chart_controls("Bar")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    filtered_data = forest_data[
        (forest_data['luas_ha'] >= luas_range[0]) & 
        (forest_data['luas_ha'] <= luas_range[1])
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_flexible_chart(
            filtered_data,
            x_col='kelas_umur',
            y_col='luas_ha',
            chart_type=chart_type,
            color_theme=color_theme,
            show_labels=show_labels,
            title='Luas per Kelas Umur',
            color_col='kelas_umur' if chart_type in ['Bar', 'Pie'] else None,
            text_col='luas_ha'
        )
        fig = apply_chart_settings(fig, show_grid)
        st.plotly_chart(fig, use_container_width=True, key="profil_chart1")
    
    with col2:
        fig2 = create_flexible_chart(
            filtered_data,
            x_col='kelas_umur',
            y_col='persentase',
            chart_type=chart_type,
            color_theme=color_theme,
            show_labels=show_labels,
            title='Persentase per Kelas Umur',
            color_col='kelas_umur' if chart_type in ['Bar', 'Pie'] else None,
            text_col='persentase'
        )
        fig2 = apply_chart_settings(fig2, show_grid)
        st.plotly_chart(fig2, use_container_width=True, key="profil_chart2")
    
    st.markdown("---")
    st.subheader("📋 Data Detail")
    st.dataframe(
        filtered_data.style.format({
            'luas_ha': '{:,.2f}',
            'persentase': '{:.2f}%'
        }),
        use_container_width=True,
        hide_index=True
    )

# ==================== PRODUKSI KAYU ====================
elif menu == "🪵 Produksi Kayu":
    st.title("🪵 Produksi Kayu KPH Saradan")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_2016 = production_data['volume_2016'].sum()
        st.metric("Total Produksi 2016", f"{total_2016:,.2f} m³")
    with col2:
        total_2017 = production_data['volume_2017'].sum()
        st.metric("Total Produksi 2017", f"{total_2017:,.2f} m³")
    with col3:
        perubahan = ((total_2017 / total_2016) - 1) * 100
        st.metric("Perubahan", f"{perubahan:.2f}%", delta=f"{perubahan:.2f}%")
    
    st.markdown("---")
    
    st.markdown('<div class="chart-control">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type, color_theme, show_labels, show_grid = create_chart_controls("Bar")
    
    with col2:
        tahun_filter = st.multiselect(
            "📅 Filter Tahun",
            options=['volume_2016', 'volume_2017'],
            default=['volume_2016', 'volume_2017'],
            format_func=lambda x: x.replace('volume_', '')
        )
    
    with col3:
        jenis_filter = st.multiselect(
            "🪵 Filter Jenis Kayu",
            options=production_data['jenis_kayu'].tolist(),
            default=production_data['jenis_kayu'].tolist()
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    filtered_prod = production_data[production_data['jenis_kayu'].isin(jenis_filter)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if chart_type == "Pie":
            data_pie = filtered_prod.melt(
                id_vars=['jenis_kayu'],
                value_vars=tahun_filter,
                var_name='tahun',
                value_name='volume'
            )
            fig = px.pie(
                data_pie,
                values='volume',
                names='jenis_kayu',
                title='Distribusi Produksi per Jenis Kayu',
                color='jenis_kayu',
                color_discrete_map={'Jati': '#2e7d32', 'Rimba': '#66bb6a'},
                hole=0.3
            )
            fig.update_traces(textinfo='percent+label')
        else:
            prod_melted = filtered_prod.melt(
                id_vars=['jenis_kayu'],
                value_vars=tahun_filter,
                var_name='tahun',
                value_name='volume'
            )
            fig = create_flexible_chart(
                prod_melted,
                x_col='jenis_kayu',
                y_col='volume',
                chart_type=chart_type,
                color_theme=color_theme,
                show_labels=show_labels,
                title='Perbandingan Produksi',
                color_col='tahun' if chart_type != 'Pie' else None,
                text_col='volume'
            )
        
        fig = apply_chart_settings(fig, show_grid)
        st.plotly_chart(fig, use_container_width=True, key="produksi_chart1")
    
    with col2:
        if chart_type == "Line":
            fig2 = go.Figure()

            for kayu in filtered_prod['jenis_kayu'].unique():
                kayu_data = filtered_prod[filtered_prod['jenis_kayu'] == kayu]

                years_label = []
                volumes = []
                for tahun in tahun_filter:
                    years_label.append(tahun.replace('volume_', ''))
                    volumes.append(float(kayu_data[tahun].values[0]))

                x_numeric = list(range(len(years_label)))
                warna = '#2e7d32' if kayu == 'Jati' else '#66bb6a'

                fig2.add_trace(go.Scatter(
                    x=x_numeric,
                    y=volumes,
                    mode='lines+markers+text' if show_labels else 'lines+markers',
                    name=kayu,
                    line=dict(width=4, color=warna),
                    marker=dict(size=14, color=warna, symbol='circle',
                               line=dict(width=2, color='white')),
                    text=[f'{v:,.0f} m³' for v in volumes] if show_labels else None,
                    textposition='top center',
                ))

            fig2.update_layout(
                title='Tren Produksi (Line)',
                xaxis=dict(
                    title='Tahun',
                    tickmode='array',
                    tickvals=list(range(len(tahun_filter))),
                    ticktext=[t.replace('volume_', '') for t in tahun_filter]
                ),
                yaxis_title='Volume (m³)',
                showlegend=True,
                height=400,
                hovermode='x unified'
            )

        elif chart_type == "Scatter":
            fig2 = go.Figure()

            for kayu in filtered_prod['jenis_kayu'].unique():
                kayu_data = filtered_prod[filtered_prod['jenis_kayu'] == kayu]

                years_label = []
                volumes = []
                for tahun in tahun_filter:
                    years_label.append(tahun.replace('volume_', ''))
                    volumes.append(float(kayu_data[tahun].values[0]))

                x_numeric = list(range(len(years_label)))
                warna = '#2e7d32' if kayu == 'Jati' else '#66bb6a'

                fig2.add_trace(go.Scatter(
                    x=x_numeric,
                    y=volumes,
                    mode='lines',
                    name=f"Tren {kayu}",
                    line=dict(width=3, color=warna, dash='solid'),
                    showlegend=False
                ))

                fig2.add_trace(go.Scatter(
                    x=x_numeric,
                    y=volumes,
                    mode='markers+text' if show_labels else 'markers',
                    name=kayu,
                    marker=dict(
                        size=20,
                        color=warna,
                        symbol='circle',
                        line=dict(width=3, color='white')
                    ),
                    text=[f'{v:,.0f} m³' for v in volumes] if show_labels else None,
                    textposition='top center',
                ))

            fig2.update_layout(
                title='Perbandingan Produksi (Scatter)',
                xaxis=dict(
                    title='Tahun',
                    tickmode='array',
                    tickvals=list(range(len(tahun_filter))),
                    ticktext=[t.replace('volume_', '') for t in tahun_filter]
                ),
                yaxis_title='Volume (m³)',
                showlegend=True,
                height=400,
                hovermode='x unified'
            )

        elif chart_type == "Area":
            prod_melted_line = filtered_prod.melt(
                id_vars=['jenis_kayu'],
                value_vars=tahun_filter,
                var_name='tahun',
                value_name='volume'
            )
            prod_melted_line['tahun'] = prod_melted_line['tahun'].str.replace('volume_', '')
            
            fig2 = px.area(
                prod_melted_line,
                x='tahun',
                y='volume',
                color='jenis_kayu',
                title='Tren Produksi (Area)',
                color_discrete_map={'Jati': '#2e7d32', 'Rimba': '#66bb6a'},
                line_shape='linear'
            )
            fig2.update_traces(line=dict(width=3), opacity=0.7, marker=dict(size=8))

        else:
            prod_melted_line = filtered_prod.melt(
                id_vars=['jenis_kayu'],
                value_vars=tahun_filter,
                var_name='tahun',
                value_name='volume'
            )
            prod_melted_line['tahun'] = prod_melted_line['tahun'].str.replace('volume_', '')
            
            fig2 = create_flexible_chart(
                prod_melted_line,
                x_col='tahun',
                y_col='volume',
                chart_type=chart_type,
                color_theme=color_theme,
                show_labels=show_labels,
                title='Tren Produksi',
                color_col='jenis_kayu' if chart_type != 'Pie' else None,
                text_col='volume'
            )
        
        fig2 = apply_chart_settings(fig2, show_grid)
        st.plotly_chart(fig2, use_container_width=True, key="produksi_chart2")
    
    st.markdown("---")
    st.subheader("📋 Detail per Jenis Kayu")
    
    for _, row in filtered_prod.iterrows():
        warna = '🔴' if row['perubahan_persen'] < 0 else '🟢'
        st.markdown(f"""
        ### {row['jenis_kayu']}
        - **Volume 2016**: {row['volume_2016']:,.2f} m³
        - **Volume 2017**: {row['volume_2017']:,.2f} m³
        - **Perubahan**: {warna} {row['perubahan_persen']:.2f}%
        """)

# ==================== MASTER DATA ====================
elif menu == "📋 Master Data":
    st.title("📋 Master Data KPH Saradan")
    st.markdown("---")
    
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
    
    tab1, tab2, tab3 = st.tabs(["🌲 Kelas Umur", "🪵 Produksi Kayu", "💰 Finansial"])
    
    with tab1:
        st.dataframe(
            forest_data.style.format({
                'luas_ha': '{:,.2f}',
                'persentase': '{:.2f}%'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.dataframe(production_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.dataframe(
            financial_data.style.format({
                'skenario_a': '{:,.0f}',
                'skenario_b': '{:,.0f}',
                'selisih': '{:,.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )

# ==================== PARAMETER SIMULASI ====================
elif menu == "⚙️ Parameter Simulasi":
    st.title("⚙️ Parameter Simulasi")
    st.markdown("---")
    
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
    st.subheader("📈 Visualisasi Hasil Simulasi")
    
    chart_type, color_theme, show_labels, show_grid = create_chart_controls("Bar")
    
    sim_data = pd.DataFrame({
        'Skenario': ['Tradisional', 'Hijau Terintegrasi'],
        'NPV (Rp Juta)': [npv/1e6, npv_b/1e6],
        'IRR (%)': [18.0, 20.0],
        'BCR': [1.45, 1.82]
    })
    
    fig = create_flexible_chart(
        sim_data,
        x_col='Skenario',
        y_col='NPV (Rp Juta)',
        chart_type=chart_type,
        color_theme=color_theme,
        show_labels=show_labels,
        title='Perbandingan NPV',
        color_col='Skenario' if chart_type != 'Pie' else None,
        text_col='NPV (Rp Juta)'
    )
    
    if chart_type == "Pie":
        fig.update_traces(marker=dict(colors=['#ff9800', '#2e7d32']))
    
    fig = apply_chart_settings(fig, show_grid)
    st.plotly_chart(fig, use_container_width=True, key="simulasi_chart")

# ==================== DASHBOARD SUMMARY ====================
elif menu == "📈 Dashboard Summary":
    st.title("📈 Dashboard Summary KPH Saradan")
    st.markdown("---")
    
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
    
    st.markdown('<div class="chart-control">', unsafe_allow_html=True)
    chart_type, color_theme, show_labels, show_grid = create_chart_controls("Bar")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_flexible_chart(
            forest_data,
            x_col='kelas_umur',
            y_col='luas_ha',
            chart_type=chart_type,
            color_theme=color_theme,
            show_labels=show_labels,
            title='Distribusi Luas per Kelas Umur',
            color_col='kelas_umur' if chart_type in ['Bar', 'Pie'] else None,
            text_col='luas_ha'
        )
        fig = apply_chart_settings(fig, show_grid, height=350)
        st.plotly_chart(fig, use_container_width=True, key="summary_chart1")
    
    with col2:
        prod_melted = production_data.melt(
            id_vars=['jenis_kayu'],
            value_vars=['volume_2016', 'volume_2017'],
            var_name='tahun',
            value_name='volume'
        )
        
        if chart_type == "Pie":
            data_pie = prod_melted.copy()
            data_pie['label'] = data_pie['jenis_kayu'] + ' ' + data_pie['tahun'].str.replace('volume_', '')
            fig2 = px.pie(
                data_pie,
                values='volume',
                names='label',
                title='Distribusi Produksi',
                color='jenis_kayu',
                color_discrete_map={'Jati': '#2e7d32', 'Rimba': '#66bb6a'},
                hole=0.3
            )
            fig2.update_traces(textinfo='percent+label')
        else:
            fig2 = create_flexible_chart(
                prod_melted,
                x_col='jenis_kayu',
                y_col='volume',
                chart_type=chart_type,
                color_theme=color_theme,
                show_labels=show_labels,
                title='Produksi 2016 vs 2017',
                color_col='tahun' if chart_type != 'Pie' else None,
                text_col='volume'
            )
        
        fig2 = apply_chart_settings(fig2, show_grid, height=350)
        st.plotly_chart(fig2, use_container_width=True, key="summary_chart2")
    
    st.markdown("---")
    st.subheader("💡 Kesimpulan")
    
    kesimpulan_data = pd.DataFrame({
        'Indikator': ['NPV', 'IRR', 'BCR'],
        'Skenario A (Tradisional)': ['Rp 4.078 Juta', '18.00%', '1.45'],
        'Skenario B (Hijau)': ['Rp 7.058 Juta', '20.00%', '1.82'],
        'Status': ['✅ Meningkat 73%', '✅ Melewati batas modal', '✅ Efisiensi biaya naik']
    })
    
    st.dataframe(kesimpulan_data, use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Kesimpulan:** Skenario B (Hijau Terintegrasi) lebih layak secara finansial dengan 
    insentif karbon yang memberikan tambahan keuntungan signifikan.
    """)
    
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