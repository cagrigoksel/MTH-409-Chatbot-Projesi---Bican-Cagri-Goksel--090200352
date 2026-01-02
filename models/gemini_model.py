import os
import json
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from dotenv import load_dotenv

load_dotenv()

class GeminiModel:
    def __init__(self):
        
        api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.0-flash" 

    def predict_intent(self, user_input):
        system_instruction = """
        GÖREV: Kullanıcı metnini analiz et.
        
        1. INTENT (Niyet): [Greeting, Goodbye, AddToCart, RemoveFromCart, ViewCart, Checkout, TechSpecs, CompareProducts, TrackOrder, Refusal]
        
        2. ENTITY (Ürün): 
           - Cümlede geçen SPESİFİK MARKA/MODEL ismini çıkar (Örn: "iPhone 15", "Samsung S25", "Dyson V15").
           - DİKKAT: "Telefon", "cihaz", "bunu", "şunu", "bir tane" gibi genel kelimeleri ASLA entity olarak alma. Bu durumda entity: null döndür.
           - Örnek: "Telefon almak istiyorum" -> intent: "AddToCart", entity: null, reply: "Hangi modeli istersiniz?"
           - Örnek: "S25 Ultra ekle" -> intent: "AddToCart", entity: "Samsung S25 Ultra", reply: null
        
        ÇIKTI FORMATI (JSON): {"intent": "...", "entity": "...", "reply": "..."}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_instruction}\nInput: {user_input}",
                config={'response_mime_type': 'application/json'}
            )
            # Güvenli Parse İşlemi
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3]
            parsed = json.loads(text)
            if isinstance(parsed, list): parsed = parsed[0]
            return parsed
        except:
            return {"intent": "Refusal", "entity": None, "reply": "Anlaşılamadı."}

    def generate_response(self, query, chat_history=[], context=""):
        search_tool = Tool(google_search=GoogleSearch())
        
        history_text = ""
        for msg in chat_history[-5:]:
            history_text += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
        Sen TechPoint asistanısın.
        GEÇMİŞ: {history_text}
        BAĞLAM (RAG): {context}
        SORU: {query}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(tools=[search_tool], response_modalities=["TEXT"])
            )
            return response.text
        except Exception as e:
            return f"Hata: {e}"