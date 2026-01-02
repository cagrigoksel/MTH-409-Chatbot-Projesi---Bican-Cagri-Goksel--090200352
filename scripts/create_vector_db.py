import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Ayarlar
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "data/raw/manual.pdf") 
DB_PATH = os.path.join(BASE_DIR, "data/vector_db")

def create_db():
    print("RAG Hafızası Oluşturuluyor...")

    # 1. Temizlik: Eski veritabanı varsa sil (Çakışma olmasın)
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print("🧹 Eski veritabanı temizlendi.")

    # 2. PDF Kontrolü
    if not os.path.exists(PDF_PATH):
        print(f"HATA: '{PDF_PATH}' bulunamadı!")
        print("Lütfen indirdiğin S25 dosyasının adını 'manual.pdf' yapıp data/raw içine at.")
        return

    # 3. PDF Yükleme ve Parçalama
    print(f"PDF Okunuyor: {os.path.basename(PDF_PATH)}")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    
    # Text Splitter: Metni anlamlı parçalara böler
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    # Her parça 1000 karakter
        chunk_overlap=200   # Parçalar birbirine geçsin (bağlam kopmasın)
    )
    splits = text_splitter.split_documents(docs)
    print(f"Metin {len(splits)} parçaya bölündü.")

    # 4. Embedding ve Kayıt (Google Modeli ile)
    print("Vektörler hesaplanıyor (Bu işlem 1-2 dk sürebilir)...")
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", # Google'ın en iyi embedding modeli
        google_api_key=api_key
    )

    # ChromaDB'ye yazma
    Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )
    
    print(f"BAŞARILI! Vektör Veritabanı şuraya kuruldu: {DB_PATH}")
    print("Artık chatbot S25 Ultra hakkında her şeyi biliyor!")

if __name__ == "__main__":
    create_db()