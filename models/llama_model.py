import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LlamaModel:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # ESKİ: self.model_name = "llama3-70b-8192"
        # YENİ (En güncel ve güçlü sürüm):
        self.model_name = "llama-3.3-70b-versatile"

    def predict_intent(self, user_input):
        system_prompt = """
        Sen bir sınıflandırma botusun.
        Kategoriler: [Greeting, Goodbye, AddToCart, RemoveFromCart, ViewCart, Checkout, TechSpecs, CompareProducts, TrackOrder, Refusal]
        Sadece JSON formatında cevap ver: {"intent": "..."}
        Başka hiçbir şey yazma.
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0, # Tutarlılık için 0 yapıyoruz
                response_format={"type": "json_object"} # Groq JSON modunu destekler
            )
            
            # Yanıtı al ve parse et
            response_content = completion.choices[0].message.content
            return json.loads(response_content)
        except Exception as e:
            print(f"Llama Error: {e}")
            return {"intent": "Error"}