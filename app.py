import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from air_quality_model import AirQualityAI
import time

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Hava Kalitesi Analiz Sistemi",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .priority-critical {
        border-left: 4px solid #ff4444;
    }
    .priority-high {
        border-left: 4px solid #ff8800;
    }
    .priority-medium {
        border-left: 4px solid #ffcc00;
    }
    .priority-low {
        border-left: 4px solid #00cc00;
    }
    .score-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# AI modelini yükle
@st.cache_resource
def load_ai_model():
    return AirQualityAI()

ai_model = load_ai_model()

# Ana başlık
st.markdown('<h1 class="main-header">🌬️ Hava Kalitesi Analiz ve Öneri Sistemi</h1>', unsafe_allow_html=True)

# Sidebar - Girdi parametreleri
st.sidebar.header("📊 Girdi Parametreleri")

# Girdi alanları
temperature = st.sidebar.slider(
    "🌡️ Sıcaklık (°C)",
    min_value=-10.0,
    max_value=50.0,
    value=22.0,
    step=0.5,
    help="Ortam sıcaklığını girin"
)

humidity = st.sidebar.slider(
    "💧 Nem (%)",
    min_value=0.0,
    max_value=100.0,
    value=45.0,
    step=1.0,
    help="Ortam nem oranını girin"
)

co2 = st.sidebar.slider(
    "🌿 Karbondioksit Seviyesi (ppm)",
    min_value=300,
    max_value=5000,
    value=600,
    step=50,
    help="CO2 konsantrasyonunu girin"
)

area = st.sidebar.number_input(
    "🏠 Ortam Alanı (m²)",
    min_value=1.0,
    max_value=1000.0,
    value=100.0,
    step=1.0,
    help="Mekanın toplam alanını girin"
)

occupancy = st.sidebar.number_input(
    "👥 Kişi Sayısı",
    min_value=0,
    max_value=200,
    value=10,
    step=1,
    help="Ortamdaki kişi sayısını girin"
)

# Analiz butonu
analyze_button = st.sidebar.button("🔍 Analiz Et", type="primary", use_container_width=True)

# Ana içerik alanı
if analyze_button:
    # Girdi verilerini topla
    inputs = {
        'temperature': temperature,
        'humidity': humidity,
        'co2': co2,
        'area': area,
        'occupancy': occupancy
    }
    
    # Progress bar
    with st.spinner("Hava kalitesi analiz ediliyor..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # AI analizi
        results = ai_model.analyze_air_quality(inputs)
    
    if results['success']:
        # Sonuçları göster
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Hava kalitesi skoru
            score_percentage = results['score'] * 100
            color_map = {
                'green': '#00ff00',
                'lightgreen': '#90ee90',
                'orange': '#ffa500',
                'red': '#ff0000',
                'darkred': '#8b0000'
            }
            
            st.markdown(f"""
            <div class="score-display" style="background-color: {color_map.get(results['color'], '#1f77b4')}; color: white;">
                {score_percentage:.1f}%
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='text-align: center; color: {color_map.get(results['color'], '#1f77b4')};'>{results['category']}</h3>", unsafe_allow_html=True)
        
        # Detaylı analiz
        st.subheader("📈 Detaylı Analiz")
        
        # Metrikler
        col1, col2, col3, col4, col5 = st.columns(5)
        
        detailed = results['detailed_analysis']
        
        with col1:
            st.metric(
                "🌡️ Sıcaklık",
                f"{detailed['temperature']['value']}{detailed['temperature']['unit']}",
                f"Skor: {detailed['temperature']['score']:.2f}",
                delta_color="normal" if detailed['temperature']['status'] == 'Optimal' else "inverse"
            )
        
        with col2:
            st.metric(
                "💧 Nem",
                f"{detailed['humidity']['value']}{detailed['humidity']['unit']}",
                f"Skor: {detailed['humidity']['score']:.2f}",
                delta_color="normal" if detailed['humidity']['status'] == 'Optimal' else "inverse"
            )
        
        with col3:
            st.metric(
                "🌿 CO2",
                f"{detailed['co2']['value']}{detailed['co2']['unit']}",
                f"Skor: {detailed['co2']['score']:.2f}",
                delta_color="normal" if detailed['co2']['status'] == 'Optimal' else "inverse"
            )
        
        with col4:
            st.metric(
                "🏠 Alan/Kişi",
                f"{detailed['area_per_person']['value']:.1f}{detailed['area_per_person']['unit']}",
                f"Skor: {detailed['area_per_person']['score']:.2f}",
                delta_color="normal" if detailed['area_per_person']['status'] == 'Optimal' else "inverse"
            )
        
        with col5:
            st.metric(
                "👥 Kişi Sayısı",
                f"{detailed['occupancy']['value']}{detailed['occupancy']['unit']}",
                detailed['occupancy']['status'],
                delta_color="normal" if detailed['occupancy']['status'] == 'Normal' else "inverse"
            )
        
        # Radar chart
        st.subheader("📊 Parametre Karşılaştırması")
        
        # Radar chart verisi
        categories = ['Sıcaklık', 'Nem', 'CO2', 'Alan/Kişi']
        values = [
            detailed['temperature']['score'],
            detailed['humidity']['score'],
            detailed['co2']['score'],
            detailed['area_per_person']['score']
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Mevcut Durum',
            line_color='#1f77b4'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Hava Kalitesi Parametreleri"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Önerileri
        st.subheader("🤖 AI Destekli Öneriler")
        
        if results['recommendations']:
            for i, rec in enumerate(results['recommendations']):
                priority_class = f"priority-{rec['priority']}"
                
                st.markdown(f"""
                <div class="recommendation-card {priority_class}">
                    <h4>🔧 {rec['title']}</h4>
                    <p><strong>Öncelik:</strong> {rec['priority'].title()}</p>
                    <p>{rec['description']}</p>
                    <ul>
                        {''.join([f'<li>{action}</li>' for action in rec['actions']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 Tebrikler! Hava kalitesi optimal seviyede. Herhangi bir iyileştirme önerisi bulunmuyor.")
        
        # İyileştirme simülasyonu
        st.subheader("🎯 İyileştirme Simülasyonu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Mevcut durumunuzu iyileştirmek için önerilen değişiklikler:**")
            
            improvements = {}
            
            if detailed['temperature']['status'] != 'Optimal':
                if temperature < 18:
                    improvements['temperature'] = 4
                elif temperature > 26:
                    improvements['temperature'] = -4
            
            if detailed['humidity']['status'] != 'Optimal':
                if humidity < 30:
                    improvements['humidity'] = 15
                elif humidity > 60:
                    improvements['humidity'] = -15
            
            if detailed['co2']['status'] != 'Optimal':
                improvements['co2'] = -200
            
            if detailed['area_per_person']['status'] != 'Optimal':
                improvements['area_per_person'] = 5
            
            for param, improvement in improvements.items():
                if param == 'temperature':
                    st.write(f"🌡️ Sıcaklık: {temperature}°C → {temperature + improvement}°C")
                elif param == 'humidity':
                    st.write(f"💧 Nem: {humidity}% → {humidity + improvement}%")
                elif param == 'co2':
                    st.write(f"🌿 CO2: {co2} ppm → {co2 + improvement} ppm")
                elif param == 'area_per_person':
                    st.write(f"🏠 Alan/Kişi: {detailed['area_per_person']['value']:.1f} m² → {detailed['area_per_person']['value'] + improvement:.1f} m²")
        
        with col2:
            if improvements:
                # İyileştirme tahmini
                prediction = ai_model.get_improvement_predictions(inputs, improvements)
                
                st.metric(
                    "📈 Tahmini İyileştirme",
                    f"{prediction['improved_score']*100:.1f}%",
                    f"+{prediction['improvement_percentage']:.1f}%",
                    delta_color="normal"
                )
                
                st.write(f"**Mevcut Skor:** {prediction['current_score']*100:.1f}%")
                st.write(f"**İyileştirilmiş Skor:** {prediction['improved_score']*100:.1f}%")
            else:
                st.info("Tüm parametreler optimal seviyede! 🎉")
    
    else:
        st.error("❌ Girdi verilerinde hata bulundu:")
        for error in results['errors']:
            st.write(f"• {error}")

# Bilgi paneli
else:
    st.info("👈 Sol taraftaki parametreleri girin ve 'Analiz Et' butonuna tıklayın.")
    
    # Örnek değerler
    st.subheader("📋 Örnek Değerler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Optimal Değerler:**")
        st.write("• Sıcaklık: 20-24°C")
        st.write("• Nem: 40-50%")
        st.write("• CO2: 400-800 ppm")
        st.write("• Alan/Kişi: ≥20 m²")
        st.write("• Kişi Sayısı: ≤50")
    
    with col2:
        st.write("**Kritik Değerler:**")
        st.write("• Sıcaklık: <18°C veya >26°C")
        st.write("• Nem: <30% veya >60%")
        st.write("• CO2: >1000 ppm")
        st.write("• Alan/Kişi: <15 m²")
        st.write("• Kişi Sayısı: >100")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌬️ Hava Kalitesi Analiz ve Öneri Sistemi | AI Destekli Çözümler</p>
    <p>Geliştirici: Hava Kalitesi Uzmanı</p>
</div>
""", unsafe_allow_html=True)
