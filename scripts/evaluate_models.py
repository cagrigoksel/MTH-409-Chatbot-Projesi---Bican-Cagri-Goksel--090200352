import sys
import os
import pandas as pd
import time
from sklearn.metrics import classification_report
from tqdm import tqdm

# Modellerin bulunduğu klasörü tanıt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 3 DEV MODELİ İÇERİ ALIYORUZ
from models.gemini_model import GeminiModel
from models.qwen_model import QwenModel
from models.llama_model import LlamaModel

def evaluate():
    print("📊 3 BÜYÜK MODELİN PERFORMANS TESTİ BAŞLIYOR...")
    print("(Google Gemini vs Alibaba Qwen vs Meta Llama)")
    
    # 1. Veri Setini Yükle
    data_path = "data/processed/techpoint_advanced_dataset.xlsx"
    if not os.path.exists(data_path):
        print("❌ Veri seti bulunamadı!")
        return

    df = pd.read_excel(data_path)
    
    # Test için rastgele 50 örnek
    test_df = df.sample(n=50, random_state=42)
    
    print(f"🧪 Test Edilecek Veri Sayısı: {len(test_df)}")

    y_true = test_df['Intent'].tolist()
    
    # Tahmin Listeleri
    y_pred_gemini = []
    y_pred_qwen = []
    y_pred_llama = []

    # Modelleri Başlat
    print("🔧 Modeller yükleniyor...")
    gemini = GeminiModel()
    qwen = QwenModel()
    llama = LlamaModel()

    print("\n🚀 Tahminler yapılıyor (Lütfen bekleyin)...")
    
    # İlerleme çubuğu ile döngü
    for index, row in tqdm(test_df.iterrows(), total=len(test_df)):
        text = row['Sentence']
        
        # --- 1. GOOGLE GEMINI ---
        try:
            res = gemini.predict_intent(text)
            pred = res.get("intent")
        except: pred = "Error"
        # FIX: None gelirse 'Error' yap
        if pred is None: pred = "Error"
        y_pred_gemini.append(pred)
        
        # --- 2. ALIBABA QWEN ---
        try:
            res = qwen.predict_intent(text)
            pred = res.get("intent")
        except: pred = "Error"
        # FIX: None gelirse 'Error' yap
        if pred is None: pred = "Error"
        y_pred_qwen.append(pred)

        # --- 3. META LLAMA ---
        try:
            res = llama.predict_intent(text)
            pred = res.get("intent")
        except: pred = "Error"
        # FIX: None gelirse 'Error' yap
        if pred is None: pred = "Error"
        y_pred_llama.append(pred)
        
        # API'leri çok yormamak için minik bekleme
        time.sleep(0.5)

    # --- RAPORLAMA ---
    
    # 1. GEMINI
    print("\n" + "="*60)
    print("🔵 GOOGLE GEMINI 2.0 FLASH SONUÇLARI")
    print("="*60)
    print(classification_report(y_true, y_pred_gemini, zero_division=0))

    # 2. QWEN
    print("\n" + "="*60)
    print("🟣 ALIBABA QWEN 3 SONUÇLARI")
    print("="*60)
    print(classification_report(y_true, y_pred_qwen, zero_division=0))

    # 3. LLAMA
    print("\n" + "="*60)
    print("🟠 META LLAMA 3.3 SONUÇLARI")
    print("="*60)
    print(classification_report(y_true, y_pred_llama, zero_division=0))

if __name__ == "__main__":
    evaluate()