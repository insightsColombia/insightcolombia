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

image_path = "img/qr.png" 

col1, col2= st.columns([4.5, 1.8])
with col1:
    st.markdown("""


    InSight Colombia es más que una aplicación; es una herramienta esencial para tu vida. 
    
    Proporcionamos:

    ¡Bienvenido a tu espacio seguro de bienestar emocional! En este sitio encontrarás un asistente virtual 
    dedicado a brindarte apoyo emocional en tiempo real, diseñado para acompañarte en tu camino hacia una 
    mejor salud mental. Sin importar lo que estés atravesando, estamos aquí para escucharte, comprenderte y 
    ofrecerte herramientas personalizadas que te ayuden a manejar tus emociones, reducir el estrés y encontrar 
    alivio en momentos de dificultad. Tu bienestar importa, y no tienes que enfrentar tus retos emocionales solo.
    
    Juntos, en InSight Colombia, estamos comprometidos a marcar la diferencia en el apoyo emocional.

    """
    )
with col2:
  st.image(image_path, use_column_width=True)


st.write("---")

#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h5>🌎2025</h5>
        </div>
    """, unsafe_allow_html=True)
