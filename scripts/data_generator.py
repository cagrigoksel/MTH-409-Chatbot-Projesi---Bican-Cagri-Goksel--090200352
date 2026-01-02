import pandas as pd
import time
import os
import yaml
from dotenv import load_dotenv
from google import genai
from google.genai import types 

# --- 1. AYARLARI YÜKLE ---
load_dotenv() 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# --- 2. CLIENT ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")

client = genai.Client(api_key=api_key)
output_path = os.path.join(BASE_DIR, config["paths"]["processed_data"])
os.makedirs(os.path.dirname(output_path), exist_ok=True)

def generate_with_retry(intent, description, count):
    """
    Bu fonksiyon 429 hatası alırsa otomatik bekler ve tekrar dener.
    """
    prompt = f"""
    {config["system_context"]}
    GÖREV: Aşağıdaki Intent (Niyet) için {count} adet Türkçe eğitim verisi üret.
    INTENT: {intent}
    AÇIKLAMA: {description}
    KURALLAR:
    1. Cümlelerin %20'si yazım hatalı, %30'u kısa, %50'si normal olsun.
    2. Sadece cümleleri alt alta yaz. Madde işareti (-) kullanma.
    """
    
    max_retries = 5
    attempt = 0
    
    while attempt < max_retries:
        try:
            response = client.models.generate_content(
                model=config["model_name"],
                contents=prompt
            )
            
            if response.text:
                lines = response.text.strip().split("\n")
                return [l.strip().lstrip("-*123456789. ") for l in lines if l.strip()]
            return []

        except Exception as e:
            error_msg = str(e)
            
            # Eğer hata 429 (Too Many Requests) ise
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = 30 + (attempt * 10) # Her denemede süreyi artır (30s, 40s, 50s...)
                print(f"\nKota aşıldı ({intent}). {wait_time} saniye bekleniyor... (Deneme {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                attempt += 1
            
            # Eğer model bulunamadıysa (404)
            elif "404" in error_msg or "NOT_FOUND" in error_msg:
                print(f"\nHATA: Model '{config['model_name']}' bulunamadı. config.yaml'ı kontrol et.")
                exit()
            
            else:
                print(f"Beklenmeyen Hata: {e}")
                return []
    
    print(f"{intent} için veri üretilemedi (Tüm denemeler başarısız).")
    return []

# --- 3. ANA DÖNGÜ ---
all_data = []
target_count = config["generation_settings"]["target_per_intent"]
batch_size = config["generation_settings"]["batch_size"]

print(f"{config['project_name']} Veri Üretimi Başlıyor...")
print(f"Model: {config['model_name']}")

for intent, desc in config["intents"].items():
    print(f"İşleniyor: {intent}...")
    collected = 0
    
    while collected < target_count:
        # Retry fonksiyonunu çağırıyoruz
        sentences = generate_with_retry(intent, desc, batch_size)
        
        if not sentences:
            # Eğer hiç veri gelmediyse döngüyü kırma, tekrar dene veya pas geç
            print("   -> Boş veri döndü, pas geçiliyor.")
            time.sleep(2)
            continue

        for s in sentences:
            all_data.append({"Intent": intent, "Sentence": s})
        
        collected += len(sentences)
        print(f"   -> {collected}/{target_count}")
        
        # Her başarılı istekten sonra kısa mola (API'yi boğmamak için)
        time.sleep(2)

# --- 4. KAYDET ---
df = pd.DataFrame(all_data)
# Fazlalıkları kırp
if len(df) > 1500: df = df.head(1500) 

df = df.sample(frac=1).reset_index(drop=True)
df.to_excel(output_path, index=False)

print(f"\nBAŞARILI! Dosya kaydedildi: {output_path}")
print(f"Toplam Satır: {len(df)}")