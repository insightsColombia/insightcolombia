import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Page configuration
st.set_page_config(
    page_title="InSight-Colombia",
    page_icon="👨🏽‍💻",
    layout="wide",
    initial_sidebar_state="expanded")

st.logo(
    "img/sistema-informatico.png",
    size="large",
)

# Cargar el archivo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Llamar el archivo CSS
local_css("style/styleF.css")

# Función animación
def load_lottieurl(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()

#Segunda parte
lottie_coding3 = load_lottieurl("https://lottie.host/d8b13abd-07bb-4315-a969-b0420a41b1c5/xR87YNsrin.json")

with st.container():
    st_lottie(lottie_coding3, height=350, key="coding1")
    st.write(
        f'<h1 style="font-size: 100px; color: #FF004D;">InSight Colombia</h1>',
        unsafe_allow_html=True
        )
    st.write(
        f'<h5 style="font-size: 30px;">🌸Transforma datos en decisiones de vida🌸</h5>',
        unsafe_allow_html=True
        )


st.write("---")

st.markdown("""

    Bienvenido a tu guía integral para la prevención del suicidio.

    InSight Colombia es más que una aplicación; es una herramienta esencial en la lucha contra el suicidio. 
    
    Proporcionamos:

    - **Comprensión Inicial**: exploramos la problemática del suicidio y conceptos relevantes.
    - **Datos y Análisis**: presentamos datos interactivos de intentos de suicidio entre 2016 y 2023.
    - **Tecnología Avanzada**: utilizamos Deep Learning para analizar texto y audio, identificando la expresión de la ideación suicida.
    - **Asistencia Personalizada**: un asistente virtual está disponible para primeros auxilios psicológicos.
    - **Comunidad Participativa**: invitamos a compartir sugerencias y experiencias para mejorar nuestros servicios.
    
    Juntos, en InSight Colombia, estamos comprometidos a marcar la diferencia en la prevención del suicidio.

    """
)

st.write("---")

#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h5>🌎2024</h5>
        </div>
    """, unsafe_allow_html=True)