import os
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno desde .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No se encontró la variable GEMINI_API_KEY en el entorno.")
    exit(1)

# Inicializar cliente oficial de Gemini
client = genai.Client(api_key=api_key)

print(f"🔑 Verificando modelos disponibles para la API Key: {api_key[:6]}...\n")

try:
    # Listar todos los modelos disponibles
    models = client.models.list()
    
    print("📋 Modelos disponibles:")
    print("-" * 50)
    for model in models:
        # Filtrar o mostrar detalles clave del modelo
        print(f"• Name: {model.name}")
        if hasattr(model, 'display_name') and model.display_name:
            print(f"  Display Name: {model.display_name}")
        if hasattr(model, 'supported_generation_methods') and model.supported_generation_methods:
            print(f"  Methods: {', '.join(model.supported_generation_methods)}")
        print("-" * 50)
        
except Exception as e:
    print(f"❌ Error al consultar la lista de modelos: {e}")
