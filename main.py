import os
import sys
import time
import subprocess
from dotenv import load_dotenv

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[*] {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠️ {message}{Colors.ENDC}")

def check_env():
    """API Anahtarlarını Kontrol Et"""
    print_step("Sistem Kontrolleri Yapılıyor...")
    load_dotenv()
    
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not google_key or not groq_key:
        print(f"{Colors.FAIL} HATA: .env dosyasında API Key'ler eksik!{Colors.ENDC}")
        sys.exit(1)
    
    print_success("API Anahtarları doğrulandı.")

def setup_rag():
    """Vektör Veritabanını Kontrol Et ve Gerekirse Kur"""
    print_step("RAG (Retrieval-Augmented Generation) Hafızası Kontrol Ediliyor...")
    
    db_path = "data/vector_db"
    
    # Klasör var mı ve içi dolu mu kontrolü
    if os.path.exists(db_path) and len(os.listdir(db_path)) > 0:
        print_success("Vektör Veritabanı zaten mevcut. Kurulum atlanıyor.")
    else:
        print_warning("Veritabanı bulunamadı. PDF'ler işleniyor...")
        try:
            # create_vector_db.py scriptini çalıştır
            subprocess.run([sys.executable, "scripts/create_vector_db.py"], check=True)
            print_success("Veritabanı başarıyla oluşturuldu!")
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}PDF işlenirken hata oluştu!{Colors.ENDC}")

def run_evaluation():
    print_step("Model Performans Testi ")
    
    choice = input(f"{Colors.BOLD}Modelleri (Gemini vs LLama vs Qwen) karşılarştırıp başarı metrriklerini görmek ister misiniz? (y/n): {Colors.ENDC}").lower()
    
    if choice == 'y':
        print("\nBenchmark Başlıyor... (Bu işlem 1-2 dakika sürebilir)")
        try:
            subprocess.run([sys.executable, "scripts/evaluate_models.py"], check=True)
            input(f"\n{Colors.BLUE}Devam etmek için Enter'a basın...{Colors.ENDC}")
        except:
            print("Test sırasında hata oluştu, ama uygulama çalışabilir.")
    else:
        print("Skipping evaluation...")

def launch_app():
    """Streamlit Uygulamasını Başlat"""
    print_step("🚀 TechPoint Asistanı Başlatılıyor...")
    print(f"{Colors.GREEN}Uygulama tarayıcıda açılacak...{Colors.ENDC}\n")
    
    # Streamlit'i başlat
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py"])

if __name__ == "__main__":
    print(f"""{Colors.HEADER}
    =========================================
       TECHPOINT AI - PROJE BAŞLATICI v1.0
    =========================================
    {Colors.ENDC}""")
    
    # 1. Kontroller
    check_env()
    
    # 2. RAG Kurulumu (Eksikse kurar)
    setup_rag()
    
    # 3. Performans Raporu (İsteğe bağlı)
    run_evaluation()
    
    # 4. Uygulamayı Başlat
    launch_app()