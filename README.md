# 🤖 TechPoint: AI Destekli Teknoloji Asistanı

Bu proje, **MTH-409** dersi kapsamında geliştirilmiş; kullanıcıların teknolojik ürünler hakkında bilgi alabileceği, sepet işlemleri yapabileceği ve ürün karşılaştırması isteyebileceği gelişmiş bir chatbot uygulamasıdır.

Proje, **Hibrit Mimari (Rule-Based + LLM + RAG)** kullanılarak tasarlanmıştır ve 3 farklı yapay zeka devinin modellerini (Google, Meta, Alibaba) tek çatı altında toplar.

---

## 🚀 Özellikler

- **Çoklu Model Desteği (Multi-LLM):** Kullanıcı, Google Gemini (ABD), Meta Llama (ABD) veya Alibaba Qwen (Çin) modelleri arasında seçim yapabilir.
- **RAG (Retrieval-Augmented Generation):** Samsung S25 Ultra gibi yeni ürünler için PDF kılavuzlarını okuyup veritabanından cevap verir.
- **Canlı İnternet Araması:** Google Gemini modeli, güncel fiyatlar ve bilgiler için interneti tarayabilir.
- **Intent Analizi:** Kullanıcının niyetini (Sepete Ekle, Özellik Sor, Selamlaş vb.) anlayıp ona göre aksiyon alır.

---

## 🧠 Chatbot Akışı (Flow Design)

Chatbotun çalışma mantığı şu şekildedir:

1.  **Girdi:** Kullanıcı mesaj yazar.
2.  **Router (Yönlendirici):** Seçilen LLM (Gemini, Llama veya Qwen), mesajın niyetini (Intent) analiz eder.
    * *Intent Türleri:* `Greeting`, `AddToCart`, `TechSpecs`, `CompareProducts` vb.
3.  **İşlem:**
    * Eğer niyet **Sepet İşlemi** ise -> Python fonksiyonları çalışır (Ekle/Çıkar).
    * Eğer niyet **Bilgi Sorusu** ise -> RAG motoru devreye girer (Vektör DB taranır) veya İnternet araması yapılır.
4.  **Çıktı:** Yanıt kullanıcıya iletilir.

```mermaid
graph TD
    A[Kullanıcı Mesajı] --> B{Model Seçimi?};
    B -- Gemini 2.0 --> C[Intent Analizi];
    B -- Llama 3.3 --> C;
    B -- Qwen 3 --> C;
    C --> D{Niyet Nedir?};
    D -- Sepet İşlemi --> E[Python Fonksiyonu];
    D -- Teknik Bilgi --> F{Veri Kaynağı?};
    F -- PDF Mevcut --> G[RAG (Vektör DB)];
    F -- Genel Soru --> H[Google Arama];
    E --> I[Yanıt];
    G --> I;
    H --> I;