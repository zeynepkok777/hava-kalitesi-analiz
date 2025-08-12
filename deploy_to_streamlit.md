# Streamlit'e Deploy Etme Talimatları

Bu dosya, hava kalitesi analiz uygulamasını Streamlit Cloud'a deploy etme adımlarını içerir.

## 1. GitHub'a Yükleme

### Git Repository Oluşturma
```bash
# Git repository'yi başlat
git init

# Dosyaları ekle
git add .

# İlk commit'i yap
git commit -m "Initial commit: Hava Kalitesi Analiz Sistemi"

# GitHub'da yeni repository oluştur (manuel olarak)
# Sonra remote'u ekle
git remote add origin https://github.com/KULLANICI_ADIN/hava-kalitesi-projesi.git

# Push yap
git push -u origin main
```

## 2. Streamlit Cloud'a Deploy Etme

### Adım 1: Streamlit Cloud'a Git
1. [share.streamlit.io](https://share.streamlit.io) adresine git
2. GitHub hesabınla giriş yap

### Adım 2: Repository Seçimi
1. "New app" butonuna tıkla
2. Repository'ni seç: `KULLANICI_ADIN/hava-kalitesi-projesi`
3. Branch: `main`
4. Main file path: `app.py`

### Adım 3: Deploy Ayarları
1. **App URL**: `hava-kalitesi-analiz` (veya istediğin bir isim)
2. **Python version**: 3.9 veya 3.10
3. **Requirements file**: `requirements.txt`

### Adım 4: Deploy
1. "Deploy!" butonuna tıkla
2. Deploy işleminin tamamlanmasını bekle (2-3 dakika)

## 3. Deploy Sonrası Kontrol

### Uygulama URL'si
Deploy tamamlandıktan sonra şu formatta bir URL alacaksın:
```
https://hava-kalitesi-analiz-KULLANICI_ADIN.streamlit.app
```

### Test Etme
1. URL'yi tarayıcında aç
2. Tüm özelliklerin çalıştığını kontrol et:
   - Girdi parametreleri
   - Analiz butonu
   - Sonuçların gösterimi
   - Grafikler
   - Öneriler

## 4. Sorun Giderme

### Yaygın Sorunlar

#### 1. Import Hatası
```
ModuleNotFoundError: No module named 'air_quality_model'
```
**Çözüm**: Dosya yollarını kontrol et, `__init__.py` dosyası ekle

#### 2. Streamlit Cache Hatası
```
StreamlitAPIException: st.cache_resource is deprecated
```
**Çözüm**: `@st.cache_resource` yerine `@st.cache_data` kullan

#### 3. Plotly Hatası
```
ImportError: No module named 'plotly'
```
**Çözüm**: `requirements.txt` dosyasında plotly'nin olduğundan emin ol

### Log Kontrolü
1. Streamlit Cloud dashboard'unda "Logs" sekmesine git
2. Hata mesajlarını kontrol et
3. Gerekirse requirements.txt'yi güncelle

## 5. Güncelleme

### Kod Güncellemesi
```bash
# Değişiklikleri yap
git add .
git commit -m "Update: Yeni özellik eklendi"
git push origin main
```

Streamlit Cloud otomatik olarak güncellemeleri algılar ve yeniden deploy eder.

### Requirements Güncellemesi
`requirements.txt` dosyasını güncelledikten sonra:
1. GitHub'a push yap
2. Streamlit Cloud'da "Redeploy" butonuna tıkla

## 6. Özelleştirme

### App İkonu
`app.py` dosyasında:
```python
st.set_page_config(
    page_icon="🌬️",  # Burayı değiştir
    ...
)
```

### Renk Teması
CSS stillerini `app.py` dosyasında güncelle:
```css
.main-header {
    color: #1f77b4;  /* Burayı değiştir */
}
```

## 7. Performans Optimizasyonu

### Cache Kullanımı
```python
@st.cache_data
def expensive_function():
    # Ağır hesaplamalar
    pass
```

### Lazy Loading
```python
if st.button("Analiz Et"):
    # Sadece butona tıklandığında çalıştır
    results = analyze_data()
```

## 8. Güvenlik

### API Key'ler
Eğer API key kullanıyorsan:
1. Streamlit Cloud'da "Secrets" sekmesine git
2. API key'ini ekle
3. Kodda şu şekilde kullan:
```python
api_key = st.secrets["api_key"]
```

## 9. Monitoring

### Kullanım İstatistikleri
Streamlit Cloud dashboard'unda:
- Günlük ziyaretçi sayısı
- Uygulama performansı
- Hata oranları

### Log Analizi
- Hata loglarını düzenli kontrol et
- Performans sorunlarını tespit et
- Kullanıcı geri bildirimlerini takip et

## 10. Yedekleme

### GitHub Backup
Tüm kod GitHub'da güvenli, ama ek yedekleme için:
```bash
# Tüm projeyi zip'le
zip -r hava-kalitesi-backup.zip . -x "*.git*" "*.pyc" "__pycache__/*"
```

Bu talimatları takip ederek uygulamanı başarıyla Streamlit Cloud'a deploy edebilirsin!
