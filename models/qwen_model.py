import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QwenModel:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        self.model_name = "qwen/qwen3-32b" 

    def predict_intent(self, user_input):
        system_prompt = """
        GÖREV: Kullanıcı metnini analiz et.
        1. INTENT: [Greeting, Goodbye, AddToCart, RemoveFromCart, ViewCart, Checkout, TechSpecs, CompareProducts, TrackOrder, Refusal]
        2. ENTITY: Ürün adı varsa çıkar. Genel kelimeler (telefon, cihaz) için null döndür.
        
        ÇIKTI (JSON): {"intent": "...", "entity": "...", "reply": "..."}
        """
        try:
            # Qwen JSON formatını çok iyi anlar
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"intent": "Refusal", "entity": None, "reply": "Qwen Hatası"}

    def generate_response(self, query, chat_history=[], context=""):
        messages = [{"role": "system", "content": "Sen TechPoint asistanısın. Zeki ve yardımsever ol."}]
        
        for msg in chat_history[-5:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        messages.append({"role": "user", "content": query})

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.6
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Hata: {e}"