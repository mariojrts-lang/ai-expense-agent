# 🤖 AI Expense Agent & Assistant

Un agente de inteligencia artificial para la gestión y control de gastos personales mediante procesamiento de lenguaje natural. La aplicación utiliza el **SDK oficial de Google GenAI (Gemini 2.5 Flash)** con capacidades de **Function Calling** para interpretar comandos en español, deducir categorías y montos, y registrar o consultar transacciones en una base de datos MySQL desplegada en contenedores Docker.

---

## 🏗️ Arquitectura del Sistema

La solución está construida sobre una arquitectura modular basada en microservicios contenerizados:


+-----------------------------------------------------------------------+
|                          Docker Environment                           |
|                                                                       |
|  +---------------------------+        +----------------------------+  |
|  |     web (Streamlit)       |        |        db (MySQL 8.0)       |  |
|  |                           |        |                            |  |
|  |  • UI / Chat Interface    |        |  • Database: expenses_db   |  |
|  |  • Python google-genai    |        |  • Table: expenses         |  |
|  |  • Function Calling       |        |  • Persistent Volume       |  |
|  +-------------+-------------+        +-------------+--------------+  |
|                |                                    ^                 |
|                +------------------------------------+                 |
|                        MySQL Connector (3306)                         |
+-----------------------------------------------------------------------+
|
v
Google Gemini API 2.5


### Componentes Clave

1. **Frontend / Agent (`web`)**: Desarrollado con **Streamlit** y Python. Encargado de la interfaz de chat en tiempo real, el procesamiento del prompt del usuario y la orquestación del agente mediante el SDK `google-genai`.
2. **LLM Engine**: **Gemini 2.5 Flash** (`models/gemini-2.5-flash`), optimizado para baja latencia y extracción estructurada vía *Function Calling* (`registrar_gasto`, `consultar_gastos_totales`).
3. **Persistencia de Datos (`db`)**: Contenedor **MySQL 8.0** que almacena el historial detallado de transacciones (fecha, descripción, categoría, subcategoría, tipo y monto).

---

## 📋 Prerrequisitos

Antes de iniciar el despliegue, asegúrate de contar con lo siguiente en tu entorno (Linux, WSL2 o MacOS):

* **Docker** (v20.10 o superior)
* **Docker Compose** (v2.0 o superior)
* **Clave de API de Google Gemini** (Obtenla en [Google AI Studio](https://aistudio.google.com/))
* **Git**

---

## 🚀 Instrucciones de Despliegue

1. Clonar el repositorio

git clone [https://github.com/mariojrts-lang/ai-expense-agent.git](https://github.com/mariojrts-lang/ai-expense-agent.git)
cd ai-expense-agent


2. Configurar las variables de entorno

Copia el archivo de plantilla .env.example para crear tu archivo .env de entorno local:

cp .env.example .env


Edita el archivo .env e ingresa tu API Key real de Gemini y tus credenciales de MySQL:

GEMINI_API_KEY=tu_api_key_aqui
GEMINI_MODEL=gemini-2.5-flash

DB_HOST=db
DB_USER=expense_user
DB_PASSWORD=expense_secret_pass
DB_NAME=expenses_db
MYSQL_ROOT_PASSWORD=root_secret_pass


3. Levantar los servicios con Docker Compose

docker compose up -d --build


4. Acceder a la aplicación

👉 http://localhost:8501 (o la IP de tu servidor local)



💬 Ejemplos de Uso en la Aplicación

El agente procesa el lenguaje natural y deduce automáticamente la información relevante.

Registrar gastos
"Hoy gasté 160 soles en el paseo rumipampa"

"Ayer compré pan por 3 soles y carne por 25 soles"

"Pagué 18 soles de la academia de fútbol de mi hijo"

Consultar gastos
"Muéstrame todos mis gastos a la fecha en una tabla"

"¿Cuánto he gastado en la categoría alimentos?"

"Dame los gastos registrados desde el 23 de noviembre"


🛠️ Comandos de Administración y Diagnóstico

** Ver los logs del contenedor web en tiempo real

docker compose logs -f web


** Probar la conexión con la API de Gemini desde el contenedor

docker compose exec web python app/test_api.py


** Conectarse a la consola de MySQL dentro del contenedor

docker compose exec db mysql -u expense_user -pexpense_secret_pass expenses_db

** Reiniciar el servicio web tras realizar cambios

docker compose restart web

📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Libre para uso educativo y profesional.
