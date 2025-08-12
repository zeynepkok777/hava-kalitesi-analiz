# Hava Kalitesi Analiz ve Öneri Sistemi

Bu proje, belirli girdiler kullanarak hava kalitesini ölçen ve AI destekli iyileştirme önerileri sunan bir web uygulamasıdır.

## Özellikler

- **Hava Kalitesi Ölçümü**: Sıcaklık, nem, karbondioksit seviyesi, ortam alanı ve kişi sayısına göre hava kalitesi analizi
- **AI Destekli Öneriler**: Makine öğrenmesi ile hava kalitesini iyileştirme önerileri
- **Görselleştirme**: Hava kalitesi verilerinin interaktif grafiklerle gösterimi
- **Gerçek Zamanlı Analiz**: Anlık veri girişi ve analiz

## Girdi Parametreleri

- **Sıcaklık** (°C): Ortam sıcaklığı
- **Nem** (%): Ortam nem oranı
- **Karbondioksit Seviyesi** (ppm): CO2 konsantrasyonu
- **Ortam Alanı** (m²): Mekanın toplam alanı
- **Kişi Sayısı**: Ortamdaki kişi sayısı

## Kurulum

1. Projeyi klonlayın:
```bash
git clone <repository-url>
cd hava-kalitesi-projesi
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## Kullanım

1. Web tarayıcınızda `http://localhost:8501` adresine gidin
2. Girdi parametrelerini girin
3. "Analiz Et" butonuna tıklayın
4. Hava kalitesi skorunu ve önerileri görüntüleyin

## Proje Yapısı

```
hava-kalitesi-projesi/
├── app.py                 # Ana Streamlit uygulaması
├── air_quality_model.py   # AI modeli ve analiz fonksiyonları
├── data_processor.py      # Veri işleme fonksiyonları
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Proje dokümantasyonu
└── .gitignore           # Git ignore dosyası
```

## Teknolojiler

- **Streamlit**: Web uygulaması framework'ü
- **Scikit-learn**: Makine öğrenmesi
- **Pandas & NumPy**: Veri işleme
- **Plotly**: İnteraktif grafikler

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
