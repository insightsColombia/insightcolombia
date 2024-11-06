import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests
from langchain_experimental.agents import create_pandas_dataframe_agent
from groq import Groq
from langchain_groq import ChatGroq
import time

# Configuración inicial de la página
st.set_page_config(page_title="Assistant", page_icon=":speech_balloon:")

# Función para cargar animaciones
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cargar animación Lottie
lottie_coding5 = load_lottieurl("https://lottie.host/ad0698ce-797f-48d6-9394-bc820a12b0fd/QRcLyP3iLD.json")

# Mostrar el encabezado del chat
st.markdown(
    '<h1 style="text-align: center; color: #0b2d43">¡Bienvenid@ a tu Asistente de Apoyo!</h1>',
    unsafe_allow_html=True
)
st.write("---")

# Header
with st.container():
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <h3 style="text-align: center; color: #10375C;">❤️Descubre apoyo emocional y 📈datos clave al instante: 🤖tu asistente personal te 🧏🏻escucha y te 🤗guía.</h3>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st_lottie(lottie_coding5, height=250, key="coding1")

#______________________________________AGENTE______________________________________#

# Cargar ambos datasets
data_general = pd.read_csv('data/datos_generales.csv')
data_salud_mental = pd.read_csv('data/salud_mental.csv')

# Inicializar el modelo
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=st.secrets["general"]["GROQ_API"]
)

# Crear agentes independientes para cada dataset
agent_general = create_pandas_dataframe_agent(llm, data_general, allow_dangerous_code=True, handle_parsing_errors=True)
agent_salud_mental = create_pandas_dataframe_agent(
    llm, 
    data_salud_mental, 
    allow_dangerous_code=True, 
    handle_parsing_errors=True,  # Manejo de errores de parsing
    handle_error=lambda e: "Error en la respuesta. Por favor, intenta reformular tu pregunta."  # Mensaje en caso de error
)



# Prompt del sistema para el agente general
prompt_sistema_general = (
    "Vas a actuar como un analista de datos experto en el ámbito de la salud mental. "
    "Tu objetivo es proporcionar respuestas claras, concisas y útiles en idioma español, "
    "respetando siempre la sensibilidad de los temas tratados. "
    "Cuando se te soliciten tablas o listas, asegúrate de generarlas en formato Markdown. "
    "Prioriza la empatía y la claridad en tus respuestas, ofreciendo información basada en datos "
    "y recursos relevantes que apoyen a quienes buscan ayuda. "
    "Si el usuario menciona aspectos emocionales o de crisis, responde de manera comprensiva y "
    "dirige hacia recursos de apoyo adecuados."
)

# Prompt del sistema para el agente de apoyo emocional
prompt_sistema_salud_mental = (
    "Vas a actuar como un asesor de apoyo emocional que responde con empatía y cuidado a preguntas sobre salud mental. "
    "Ofrece siempre orientación y apoyo seguro."
)

# Inicialización del historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Prompt inicial del sistema
    st.session_state.messages.append({"role": "system", "content": prompt_sistema_general})

# Botón para resetear el historial de chat
with st.sidebar:
    st.subheader('Parámetros')
    parUsarMemoria = st.checkbox("Recordar la conversación", value=True, key="memory_checkbox")
    
    # Agregar botón de reset
    if st.button("Borrar historial de chat", key="reset_button"):
        st.session_state.messages = []  # Reiniciar el historial de mensajes
        # Reagregar el prompt inicial del sistema
        st.session_state.messages.append({"role": "system", "content": prompt_sistema_general})
        st.success("Historial de chat reiniciado.")

# Función para detectar si el mensaje contiene palabras sensibles
def is_sensitive_prompt(prompt):
    sensitive_keywords = ["suicidio", "autolesiones", "matarme", "quitarme la vida", "daño a sí mismo", "sin esperanzas", "ideas suicidas", "planes suicidas"]
    return any(keyword in prompt.lower() for keyword in sensitive_keywords)

# Campo de entrada para el usuario
prompt = st.chat_input("¡Hola! ¿Qué quieres saber en razón a los datos o apoyo emocional?")

# Procesamiento del mensaje del usuario
if prompt:
    # Agregar el mensaje del usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Selección de agente según el contenido del mensaje y filtrado de temas sensibles
    if is_sensitive_prompt(prompt):
        # Mensaje de apoyo predefinido para temas sensibles
        respuesta = (
            "Si estás pasando por un momento difícil, te recomendamos contactar a un profesional de salud mental o acudir a una línea de apoyo. Aquí tienes algunos recursos de ayuda:\n\n"
            "- **Línea Nacional de Prevención del Suicidio** (106) Línea telefónica gratuita: 018000 112 439\n"
            "- **Crisis Text Line**: Envía un mensaje (Chat por WhatsApp: 300-7548933)\n"
            "- Habla con un terapeuta, un ser querido, o acude a tu centro de salud más cercano.\n\n"
            "Recuerda que no estás solo, y hay personas que desean ayudarte en este momento difícil."
        )
    else:
        # Determinar el agente a usar según el tipo de consulta
        if "salud mental" in prompt.lower() or "emocional" in prompt.lower():
            # Usar el agente de apoyo emocional
            selected_agent = agent_salud_mental
            st.session_state.messages[0] = {"role": "system", "content": prompt_sistema_salud_mental}
        else:
            # Usar el agente de datos generales
            selected_agent = agent_general
            st.session_state.messages[0] = {"role": "system", "content": prompt_sistema_general}

        # Preparar el historial de mensajes según la configuración de memoria
        if parUsarMemoria:
            messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        else:
            # Solo sistema y último mensaje del usuario
            messages = [st.session_state.messages[0], st.session_state.messages[-1]]

        # Generar respuesta del agente seleccionado
        try:
            respuesta = selected_agent.run(messages)
        except ValueError:
            respuesta = (
                "Ha ocurrido un error al procesar tu solicitud. Por favor, intenta reformular tu pregunta o contactar soporte si el problema persiste."
            )

    # Mostrar y almacenar la respuesta
    with st.chat_message("assistant"):
        st.write(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})


# Código HTML y JavaScript para el efecto de escritura
html_code = """
<div style="text-align: center; color: #FF004D; font-size: 32px; font-family: sans-serif; font-weight: bold;">
    <span id="text"></span>
</div>
<script>
    const text = "🌸 Insight Colombia";
    let index = 0;
    function typeWriter() {
        if (index < text.length) {
            document.getElementById("text").innerHTML += text.charAt(index);
            index++;
            setTimeout(typeWriter, 100); // Velocidad de escritura (en milisegundos)
        }
    }
    typeWriter();
</script>
"""

# Incluir el HTML en Streamlit
st.components.v1.html(html_code, height=100)


