# 🤖 TechPoint: AI Destekli Teknoloji Asistanı

### Github linki: "https://github.com/cagrigoksel/MTH-409-Chatbot-Projesi---Bican-Cagri-Goksel--090200352"

## MTH-409 Chatbot Geliştirme Temelleri Term Project

**Ders:** MTH-409 Chatbot Geliştirme Temelleri
**Öğrenci Adı:** Bican Çağrı Göksel
**Öğrenci No:** 090200352

---

## 📋 Proje Özeti

Bu proje, **hibrit AI mimarisi** kullanarak gelişmiş bir teknoloji ürünleri chatbot sistemi geliştirmeyi amaçlamaktadır. Sistem, üç farklı büyük dil modelini (Google Gemini, Meta Llama, Alibaba Qwen) entegre ederek kullanıcıların teknolojik ürünler hakkında bilgi almasını, sepet işlemleri yapmasını ve ürün karşılaştırması yapmasını sağlar.

### 🎯 Temel Özellikler
- **Çoklu LLM Desteği:** 3 farklı model sağlayıcısı (ABD/Çin merkezli)
- **RAG Teknolojisi:** PDF belgelerinden bilgi çıkarımı
- **Intent Sınıflandırma:** 10 farklı kullanıcı niyeti analizi
- **Gerçek Zamanlı Chat:** Streamlit tabanlı interaktif arayüz

---

## 🏗️ Sistem Mimarisi

### Ana Bileşenler
```
TechPoint Chatbot
├── 🤖 Model Layer (3 LLM)
│   ├── Google Gemini 2.0 (RAG + Search)
│   ├── Meta Llama 3.3 (Hızlı İşleme)
│   └── Alibaba Qwen 3 (Mantık Odaklı)
├── 🗄️ Bilgi Tabanı (RAG)
│   ├── PDF Doküman İşleme
│   ├── Vektör Veritabanı (ChromaDB)
│   └── Semantic Search
├── 🎯 Intent Analizi
│   ├── 10 Intent Kategorisi
│   └── Entity Extraction
└── 💬 Kullanıcı Arayüzü
    └── Streamlit Web App
```

### Veri Akışı
1. **Kullanıcı Girişi** → Intent Analizi
2. **Niyet Belirleme** → Uygun İşlem Yönlendirme
3. **Bilgi İşleme** → RAG/Search/Rule-based
4. **Yanıt Üretimi** → Kullanıcıya İletim

---

## 📊 Teknik Uygulama

### Intent Kategorileri
| Intent | Açıklama | Örnek |
|--------|----------|--------|
| Greeting | Selamlaşma | "Merhaba" |
| AddToCart | Sepete ekleme | "iPhone 15 al" |
| TechSpecs | Teknik özellik | "Kamera çözünürlüğü?" |
| CompareProducts | Karşılaştırma | "S25 vs iPhone" |
| ViewCart | Sepet görüntüleme | "Sepetimde ne var?" |

---

## 📈 Deneysel Sonuçlar

### Model Performans Karşılaştırması
```
Intent Sınıflandırma F1 Skorları:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Model               Precision    Recall    F1-Score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Google Gemini 2.0      0.96        0.94      0.95
Alibaba Qwen 3         0.93        0.91      0.92
Meta Llama 3.3         0.90        0.88      0.89
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```


---

## 🚀 Kurulum ve Kullanım


### Hızlı Başlatma
```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. API anahtarlarını ayarla (.env dosyası)
GOOGLE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# 3. PDF dosyasını ekle
# data/raw/manual.pdf (S25 Ultra kılavuzu)

# 4. Vektör DB oluştur
python scripts/create_vector_db.py

# 5. Uygulamayı başlat
python main.py
```

### Kullanım Örnekleri
```
Kullanıcı: S25 Ultra ekle
Bot: ✅ Samsung Galaxy S25 Ultra sepete eklendi

Kullanıcı: Su geçirir mi?
Bot: [PDF'den bilgi çıkarır] Hayır, IP68 sertifikası var

Kullanıcı: iPhone 15'le karşılaştır
Bot: [İnternet araması] Fiyat, kamera, performans...
```

---

## 📁 Proje Yapısı

```
MTH-409-Chatbot-Projesi/
├── 📄 README.md              # Proje dokümantasyonu
├── ⚙️ config.yaml            # Sistem ayarları
├── 🚀 main.py                # Ana başlatıcı
├── 📦 requirements.txt       # Python bağımlılıkları
├── app/
│   └── streamlit_app.py      # Web arayüzü
├── models/
│   ├── gemini_model.py       # Google Gemini entegrasyonu
│   ├── llama_model.py        # Meta Llama entegrasyonu
│   └── qwen_model.py         # Alibaba Qwen entegrasyonu
├── scripts/
│   ├── create_vector_db.py   # Vektör DB oluşturma
│   ├── data_generator.py     # Eğitim verisi üretimi
│   └── evaluate_models.py    # Performans testi
└── data/
    ├── raw/                  # PDF belgeler
    ├── processed/            # İşlenmiş veriler
    └── vector_db/            # ChromaDB veritabanı
```

---

## 🔧 Temel Script'ler

### Model Testi
```bash
python scripts/check_models.py
```

### Veri Üretimi
```bash
python scripts/data_generator.py
```

### Performans Değerlendirmesi
```bash
python scripts/evaluate_models.py
```


*Bu proje MTH-409 dersi final ödevi kapsamında geliştirilmiştir.*