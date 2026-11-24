import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

print(f"🔑 Probando token AQ: {api_key[:6]}...{api_key[-4:]}")
print(f"🎯 Usando modelo: {model_name}")

client = genai.Client(api_key=api_key)

try:
    res = client.models.generate_content(
        model=model_name,
        contents="Hola, confirma si estas activo."
    )
    print("✅ Conexión exitosa a la API:")
    print(f"Respuesta: {res.text}")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
