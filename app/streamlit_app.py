import streamlit as st
import sys
import os

# Ana dizini path'e ekle ki 'models' klasörünü görebilsin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.gemini_model import GeminiModel
from models.llama_model import LlamaModel
from models.qwen_model import QwenModel

# Sayfa Ayarları
st.set_page_config(page_title="TechPoint AI", layout="wide")

# CSS
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; padding: 10px; border: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (AYARLAR) ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    
    # Model Seçimi
    selected_model_name = st.radio(
        "Yapay Zeka Modeli Seç:",
        (
            "Google Gemini 2.0 (Search + RAG)", 
            "Meta Llama 3.3 (ABD - Hız)", 
            "Alibaba Qwen 3 (Çin - Mantık)"  # YENİ
        )
    )
    
    # Obje oluşturma kısmı:
    if "Google" in selected_model_name:
        current_model = GeminiModel()
        st.info("ℹ️ İnternet erişimi ve Canlı Arama aktif.")
        
    elif "Alibaba" in selected_model_name:
        current_model = QwenModel()
        st.success("🐲 Qwen 3: Alibaba'nın geliştirdiği çok güçlü mantık modeli.")
        
    else:
        current_model = LlamaModel()
        st.warning("⚡ Llama 3.3: Meta'nın en son sürümü.")
        
    st.divider()
    st.write("🛒 **Sepetim**")
    if "cart" not in st.session_state:
        st.session_state.cart = []
    
    if st.session_state.cart:
        for item in st.session_state.cart:
            st.success(f"- {item}")
        if st.button("Sepeti Temizle"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.caption("Sepet boş.")

# --- CHAT EKRANI ---
st.title("🤖 TechPoint Asistan")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben TechPoint. S25 Ultra veya diğer ürünler hakkında bana sorabilirsiniz."}]

# Geçmiş mesajlar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Kullanıcı Girdisi
if prompt := st.chat_input("Mesajınızı yazın..."):
    # 1. Ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. İşleme
    with st.status("🧠 Düşünüyor...", expanded=False) as status:
        # A. Intent Analizi
        analysis = current_model.predict_intent(prompt)
        intent = analysis.get("intent", "Refusal")
        entity = analysis.get("entity")
        
        st.write(f"Tespit: **{intent}** | Ürün: **{entity}**")
        
        response_text = ""
        
        # B. Aksiyon Yönlendirmesi
        if intent in ["TechSpecs", "CompareProducts", "TrackOrder"]:
            # Sadece Gemini'de generate_response var (RAG/Search için)
            if hasattr(current_model, 'generate_response'):
                st.write("📚 Bilgi Bankası ve İnternet taranıyor...")
                response_text = current_model.generate_response(
                    prompt, 
                    chat_history=st.session_state.messages, 
                    context="S25 Ultra Kılavuzu..."
                )
            else:
                response_text = f"Llama 3 Modeli: '{intent}' niyetini tespit ettim ancak RAG yeteneğim kapalı. Gemini'ye geçerseniz cevaplayabilirim."
        
        elif intent == "AddToCart" and entity:
            st.session_state.cart.append(entity)
            response_text = f"✅ **{entity}** sepete eklendi."
            
        elif intent == "ViewCart":
            items = ", ".join(st.session_state.cart) if st.session_state.cart else "boş"
            response_text = f"🛒 Sepetiniz: {items}"
            
        elif intent == "RemoveFromCart" and entity:
            if entity in st.session_state.cart:
                st.session_state.cart.remove(entity)
                response_text = f"❌ {entity} sepetten çıkarıldı."
            else:
                response_text = "Bu ürün sepetinizde yok."
        
        else:
            # Greeting, Goodbye veya Refusal durumu
            response_text = analysis.get("reply", "Nasıl yardımcı olabilirim?")
            
        status.update(label="Tamamlandı!", state="complete")

    # 3. Cevabı Yaz
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    if intent in ["AddToCart", "RemoveFromCart"]:
        st.rerun()