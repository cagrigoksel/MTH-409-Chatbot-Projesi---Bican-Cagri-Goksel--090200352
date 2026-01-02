import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

def check_all_models():
    print("MODEL KONTROLÜ BAŞLIYOR...\n")
    
    # 1. GOOGLE GEMINI
    try:
        print("GOOGLE GEMINI (2.0 Flash):")
        api_key = os.getenv("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)
        client.models.generate_content(model="gemini-2.0-flash", contents="Test")
        print("BAŞARILI!\n")
    except Exception as e: print(f"Hata: {e}\n")

    # GROQ MODELLERİ İÇİN CLIENT
    groq_key = os.getenv("GROQ_API_KEY")
    groq_client = Groq(api_key=groq_key)

    # 2. META LLAMA 3.3
    try:
        print("META LLAMA 3.3 (Groq):")
        groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role":"user","content":"Test"}]
        )
        print("✅ BAŞARILI!\n")
    except Exception as e: print(f"Hata: {e}\n")

    # 3. ALIBABA QWEN 3
    try:
        print("ALIBABA QWEN 3 (Groq):")
        groq_client.chat.completions.create(
            model="qwen/qwen3-32b", 
            messages=[{"role":"user","content":"Test"}]
        )
        print("BAŞARILI!\n")
    except Exception as e: print(f"Hata: {e}\n")

if __name__ == "__main__":
    check_all_models()