import os
import datetime
import streamlit as st
from google import genai
from google.genai import types
from database import init_db, registrar_gasto, consultar_gastos_totales

# Inicializar Base de Datos
init_db()

# Configurar Cliente de Gemini API
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACK_MODEL = "gemini-3.5-flash"

def generate_content_with_fallback(contents, config):
    """
    Intenta generar contenido con el modelo principal.
    Si falla por sobrecarga (503 / UNAVAILABLE), intenta con el modelo de respaldo.
    """
    try:
        return client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=contents,
            config=config
        )
    except Exception as e:
        err_msg = str(e)
        if "503" in err_msg or "UNAVAILABLE" in err_msg:
            # Reintentar con el modelo de respaldo
            return client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=contents,
                config=config
            )
        raise e

st.set_page_config(page_title="AI Expense Agent", page_icon="💰")
st.title("🤖 AI Expense Agent & Assistant")
st.write("Registra tus gastos en lenguaje natural o consulta tu presupuesto.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Ejemplo: Hoy gasté 160 soles en el paseo rumipampa")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    hoy = datetime.date.today().strftime("%Y-%m-%d")
    sys_instruction = f"""
    Eres un asistente financiero personal inteligente. La fecha de hoy es {hoy}.
    Asiste al usuario registrando o consultando sus gastos en la base de datos.

    1. Para REGISTRAR un gasto:
       - Deduce Categoria, Subcategoria y Tipo.
       - Si el usuario no menciona fecha, usa la fecha de hoy ({hoy}).
       - Ejecuta la herramienta `registrar_gasto`.

    2. Para CONSULTAR o BUSCAR gastos:
       - Ejecuta la herramienta `consultar_gastos_totales`.
       - Presenta los datos recibidos en una TABLA MARKDOWN con las columnas: Fecha | Descripción | Categoría | Subcategoría | Tipo | Monto (S/).
    """

    config = types.GenerateContentConfig(
        system_instruction=sys_instruction,
        tools=[registrar_gasto, consultar_gastos_totales],
        temperature=0.1
    )

    bot_reply = ""
    try:
        # Primer llamado con fallback automático
        response = generate_content_with_fallback(prompt, config)

        if response.function_calls:
            messages_contents = [
                types.Content(role="user", parts=[types.Part.from_text(text=prompt)]),
                response.candidates[0].content
            ]

            tool_response_parts = []
            for call in response.function_calls:
                if call.name == "registrar_gasto":
                    result = registrar_gasto(**call.args)
                elif call.name == "consultar_gastos_totales":
                    result = consultar_gastos_totales(**call.args)
                else:
                    result = "Función no ejecutada"

                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result}
                    )
                )

            messages_contents.append(types.Content(role="user", parts=tool_response_parts))

            # Segundo llamado (retorno del tool) con fallback automático
            second_response = generate_content_with_fallback(messages_contents, config)
            bot_reply = second_response.text if second_response.text else "Operación completada."
        elif response.text:
            bot_reply = response.text
        else:
            bot_reply = "Sin respuesta."

    except Exception as e:
        bot_reply = f"Error al procesar la solicitud: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
