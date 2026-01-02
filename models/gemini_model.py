import os
import json
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from dotenv import load_dotenv

load_dotenv()

class GeminiModel:
    def __init__(self):
        # API Key Kontrolü
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("HATA: GOOGLE_API_KEY bulunamadı!")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash" 

    def predict_intent(self, user_input):
        system_instruction = """
        GÖREV: Kullanıcı metnini analiz et.
        
        1. INTENT (Niyet): [Greeting, Goodbye, AddToCart, RemoveFromCart, ViewCart, Checkout, TechSpecs, CompareProducts, TrackOrder, Refusal]
        
        2. ENTITY (Ürün): 
           - Cümlede geçen ürünün TAM ADINI çıkar.
           - "Telefon", "bunu", "cihaz" gibi genel kelimeleri ASLA entity olarak alma. Entity: null döndür.
        
        ÇIKTI FORMATI (JSON): {"intent": "...", "entity": "...", "reply": "..."}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_instruction}\nInput: {user_input}",
                config={'response_mime_type': 'application/json'}
            )
            
            # JSON Temizliği
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3]
            parsed = json.loads(text)
            if isinstance(parsed, list): parsed = parsed[0]
            # Eğer reply boşsa basit cevaplar ekle
            if not parsed.get("reply"):
                intent = parsed.get("intent")
                if intent == "Greeting": parsed["reply"] = "Merhaba! Size nasıl yardımcı olabilirim?"
                elif intent == "Goodbye": parsed["reply"] = "Görüşmek üzere, iyi günler!"
                else: parsed["reply"] = "Anlaşıldı, hemen ilgileniyorum."
                
            return parsed
            
        except Exception as e:
            print(f"Gemini Intent Hatası: {e}")
            return {"intent": "Refusal", "entity": None, "reply": "Üzgünüm, şu an bağlantıda bir sorun var."}

    def generate_response(self, query, chat_history=[], context=""):
        # Google Arama Aracı
        search_tool = Tool(google_search=GoogleSearch())
        
        # Geçmişi Metne Dök
        history_text = ""
        for msg in chat_history[-5:]:
            history_text += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
        Sen TechPoint asistanısın. Yardımsever ve bilgili ol.
        
        SOHBET GEÇMİŞİ:
        {history_text}
        
        RAG BİLGİSİ (S25 Ultra Kılavuzu):
        {context}
        
        KULLANICI SORUSU: {query}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(tools=[search_tool], response_modalities=["TEXT"])
            )
            
            # Eğer yanıt boş dönerse
            if not response.text:
                return "Arama yaptım ama net bir sonuç bulamadım. Lütfen tekrar sorar mısınız?"
                
            return response.text
            
        except Exception as e:
            return f"Yanıt üretilirken hata oluştu: {e}"