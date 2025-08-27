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
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .priority-critical {
        border-left: 4px solid #ff4444;
        background-color: #fff5f5;
    }
    .priority-high {
        border-left: 4px solid #ff8800;
        background-color: #fff8f0;
    }
    .priority-medium {
        border-left: 4px solid #ffcc00;
        background-color: #fffef0;
    }
    .priority-low {
        border-left: 4px solid #00cc00;
        background-color: #f0fff0;
    }
    .score-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .debug-info {
        background-color: #f0f8ff;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border-left: 3px solid #0066cc;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# AI modelini yükle
@st.cache_resource
def load_ai_model():
    return AirQualityAI()

ai_model = load_ai_model()

# Ana başlık
st.markdown('<h1 class="main-header">🏭 Fabrika Hava Kalitesi Analiz ve Öneri Sistemi</h1>', unsafe_allow_html=True)

# Sidebar - Girdi parametreleri
st.sidebar.header("🏭 Fabrika Parametreleri")

# Girdi alanları
temperature = st.sidebar.slider(
    "🌡️ Fabrika Sıcaklığı (°C)",
    min_value=-10.0,
    max_value=50.0,
    value=22.0,
    step=0.5,
    help="Fabrika üretim alanı sıcaklığını girin"
)

humidity = st.sidebar.slider(
    "💧 Fabrika Nem Oranı (%)",
    min_value=0.0,
    max_value=100.0,
    value=45.0,
    step=1.0,
    help="Fabrika üretim alanı nem oranını girin"
)

co2 = st.sidebar.slider(
    "🌿 Fabrika CO2 Seviyesi (ppm)",
    min_value=300,
    max_value=5000,
    value=600,
    step=50,
    help="Fabrika üretim alanı CO2 konsantrasyonunu girin"
)

area = st.sidebar.number_input(
    "🏭 Üretim Alanı (m²)",
    min_value=1.0,
    max_value=1000.0,
    value=100.0,
    step=1.0,
    help="Fabrika üretim alanının toplam büyüklüğünü girin"
)

occupancy = st.sidebar.number_input(
    "👥 Çalışan Sayısı",
    min_value=0,
    max_value=200,
    value=10,
    step=1,
    help="Fabrika üretim alanındaki çalışan sayısını girin"
)

# Analiz butonu
analyze_button = st.sidebar.button("🏭 Fabrika Analizi", type="primary", use_container_width=True)

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
    with st.spinner("Fabrika hava kalitesi analiz ediliyor..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # AI analizi
        results = ai_model.analyze_air_quality(inputs)
        
        # Debug: Sonuçları kontrol et
        st.write(f"**Debug - Analiz Sonucu:** Başarılı: {results['success']}")
        if results['success']:
            st.write(f"**Debug - Öneri Sayısı:** {len(results['recommendations'])}")
            st.write(f"**Debug - Öneriler:** {[rec['title'] for rec in results['recommendations']]}")
    
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
        st.subheader("🏭 Fabrika Detaylı Analizi")
        
        # Metrikler
        col1, col2, col3, col4, col5 = st.columns(5)
        
        detailed = results['detailed_analysis']
        
        with col1:
            st.metric(
                "🌡️ Fabrika Sıcaklığı",
                f"{detailed['temperature']['value']}{detailed['temperature']['unit']}",
                f"Skor: {detailed['temperature']['score']:.2f}",
                delta_color="normal" if detailed['temperature']['status'] == 'Optimal' else "inverse"
            )
        
        with col2:
            st.metric(
                "💧 Fabrika Nem Oranı",
                f"{detailed['humidity']['value']}{detailed['humidity']['unit']}",
                f"Skor: {detailed['humidity']['score']:.2f}",
                delta_color="normal" if detailed['humidity']['status'] == 'Optimal' else "inverse"
            )
        
        with col3:
            st.metric(
                "🌿 Fabrika CO2 Seviyesi",
                f"{detailed['co2']['value']}{detailed['co2']['unit']}",
                f"Skor: {detailed['co2']['score']:.2f}",
                delta_color="normal" if detailed['co2']['status'] == 'Optimal' else "inverse"
            )
        
        with col4:
            st.metric(
                "🏭 Alan/Çalışan",
                f"{detailed['area_per_person']['value']:.1f}{detailed['area_per_person']['unit']}",
                f"Skor: {detailed['area_per_person']['score']:.2f}",
                delta_color="normal" if detailed['area_per_person']['status'] == 'Optimal' else "inverse"
            )
        
        with col5:
            st.metric(
                "👥 Çalışan Sayısı",
                f"{detailed['occupancy']['value']}{detailed['occupancy']['unit']}",
                detailed['occupancy']['status'],
                delta_color="normal" if detailed['occupancy']['status'] == 'Normal' else "inverse"
            )
        
        # Radar chart
        st.subheader("📊 Fabrika Parametre Karşılaştırması")
        
        # Radar chart verisi
        categories = ['Fabrika Sıcaklığı', 'Fabrika Nem Oranı', 'Fabrika CO2 Seviyesi', 'Alan/Çalışan']
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
            title="Fabrika Hava Kalitesi Parametreleri"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Önerileri
        st.subheader("🤖 AI Destekli Fabrika Önerileri")
        
        # Debug bilgisi
        st.info(f"🔍 Debug: Toplam {len(results['recommendations'])} öneri bulundu")
        
        if results['recommendations']:
            for i, rec in enumerate(results['recommendations']):
                # Basit öneri gösterimi
                st.write(f"### 🔧 {rec['title']}")
                st.write(f"**Öncelik:** {rec['priority'].title()}")
                st.write(f"**Açıklama:** {rec['description']}")
                
                st.write("**Önerilen Aksiyonlar:**")
                for j, action in enumerate(rec['actions'], 1):
                    st.write(f"{j}. {action}")
                
                st.markdown("---")
        else:
            st.success("🎉 Tebrikler! Fabrika hava kalitesi optimal seviyede. Herhangi bir iyileştirme önerisi bulunmuyor.")
        
        # İyileştirme simülasyonu
        st.subheader("🏭 Fabrika İyileştirme Simülasyonu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Fabrika ortamınızı iyileştirmek için önerilen endüstriyel değişiklikler:**")
            
            improvements = {}
            current_area_per_person = detailed['area_per_person']['value']
            
            if detailed['temperature']['status'] != 'Optimal':
                if temperature < 18:
                    improvements['temperature'] = 4
                    st.write("🌡️ **Sıcaklık İyileştirmesi:**")
                    st.write(f"   Mevcut: {temperature}°C → Hedef: {temperature + 4}°C")
                    st.write("   • Fabrika ısıtma sistemini ayarlayın")
                    st.write("   • Üretim alanlarında ek ısıtıcılar yerleştirin")
                elif temperature > 26:
                    improvements['temperature'] = -4
                    st.write("🌡️ **Sıcaklık İyileştirmesi:**")
                    st.write(f"   Mevcut: {temperature}°C → Hedef: {temperature - 4}°C")
                    st.write("   • Endüstriyel klima sistemini çalıştırın")
                    st.write("   • Üretim makinelerinin ısı çıkışını azaltın")
            
            if detailed['humidity']['status'] != 'Optimal':
                if humidity < 30:
                    improvements['humidity'] = 15
                    st.write("💧 **Nem İyileştirmesi:**")
                    st.write(f"   Mevcut: {humidity}% → Hedef: {humidity + 15}%")
                    st.write("   • Endüstriyel nemlendirme sistemini aktif edin")
                    st.write("   • Su püskürtme sistemlerini çalıştırın")
                elif humidity > 60:
                    improvements['humidity'] = -15
                    st.write("💧 **Nem İyileştirmesi:**")
                    st.write(f"   Mevcut: {humidity}% → Hedef: {humidity - 15}%")
                    st.write("   • Endüstriyel nem alma cihazlarını çalıştırın")
                    st.write("   • Havalandırmayı artırın")
            
            if detailed['co2']['status'] != 'Optimal':
                improvements['co2'] = -200
                st.write("🌿 **CO2 İyileştirmesi:**")
                st.write(f"   Mevcut: {co2} ppm → Hedef: {co2 - 200} ppm")
                st.write("   • Endüstriyel havalandırma sistemlerini maksimuma çıkarın")
                st.write("   • CO2 sensörlerini tüm üretim alanlarına yerleştirin")
                st.write("   • Vardiya sistemini uygulayarak yoğunluğu azaltın")
            
            if detailed['area_per_person']['status'] != 'Optimal':
                improvements['area_per_person'] = 5
                st.write("🏭 **Çalışma Alanı İyileştirmesi:**")
                st.write(f"   Mevcut: {current_area_per_person:.1f} m²/kişi → Hedef: {current_area_per_person + 5:.1f} m²/kişi")
                st.write("   • Üretim alanlarını genişletin")
                st.write("   • Vardiya sistemini uygulayın")
                st.write("   • Çalışma alanlarını yeniden düzenleyin")
        
        with col2:
            if improvements:
                # İyileştirme tahmini
                prediction = ai_model.get_improvement_predictions(inputs, improvements)
                
                st.metric(
                    "📈 Fabrika Hava Kalitesi İyileştirmesi",
                    f"{prediction['improved_score']*100:.1f}%",
                    f"+{prediction['improvement_percentage']:.1f}%",
                    delta_color="normal"
                )
                
                st.write(f"**Mevcut Fabrika Skoru:** {prediction['current_score']*100:.1f}%")
                st.write(f"**İyileştirilmiş Fabrika Skoru:** {prediction['improved_score']*100:.1f}%")
                
                # İyileştirme etkisi
                if prediction['improvement_percentage'] > 20:
                    st.success("🎉 **Büyük İyileştirme:** Bu değişiklikler fabrika hava kalitesini önemli ölçüde artıracak!")
                elif prediction['improvement_percentage'] > 10:
                    st.info("📈 **Orta İyileştirme:** Bu değişiklikler fabrika hava kalitesini iyileştirecek.")
                else:
                    st.warning("⚠️ **Küçük İyileştirme:** Daha fazla önlem gerekebilir.")
            else:
                st.success("🎉 **Mükemmel!** Fabrika hava kalitesi optimal seviyede! Tüm parametreler ideal değerlerde.")
    
    else:
        st.error("❌ Girdi verilerinde hata bulundu:")
        for error in results['errors']:
            st.write(f"• {error}")

# Bilgi paneli
else:
    st.info("👈 Sol taraftaki fabrika parametrelerini girin ve 'Fabrika Analizi' butonuna tıklayın.")
    
    # Örnek değerler
    st.subheader("📋 Fabrika Referans Değerleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Optimal Fabrika Değerleri:**")
        st.write("• Sıcaklık: 20-24°C")
        st.write("• Nem: 40-50%")
        st.write("• CO2: 400-800 ppm")
        st.write("• Alan/Çalışan: ≥20 m²")
        st.write("• Çalışan Sayısı: ≤50")
    
    with col2:
        st.write("**Kritik Fabrika Değerleri:**")
        st.write("• Sıcaklık: <18°C veya >26°C")
        st.write("• Nem: <30% veya >60%")
        st.write("• CO2: >1000 ppm")
        st.write("• Alan/Çalışan: <15 m²")
        st.write("• Çalışan Sayısı: >100")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏭 Fabrika Hava Kalitesi Analiz ve Öneri Sistemi | AI Destekli Endüstriyel Çözümler</p>
    <p>Geliştirici: Endüstriyel Hava Kalitesi Uzmanı</p>
</div>
""", unsafe_allow_html=True)
