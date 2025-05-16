import streamlit as st
import requests
from streamlit_lottie import st_lottie

from forms.contact import contact_form

# Page configuration
st.set_page_config(
    page_title="Contact",
    page_icon="📫",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# Función animación
def load_lottieurl(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()

lottie_coding3 = load_lottieurl("https://lottie.host/c9728df7-44e0-4e2c-962a-33d6447942dd/7wrIUY9tAK.json")


# Header
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
        st_lottie(lottie_coding3, height=300, key="coding1")
    
with col2:
    st.title("¿Quiénes Somos?", anchor=False)
    st.write(
        
"Somos un equipo comprometido con el aprendizaje y la innovación, pertenecientes a la Corporación Unificada Nacional de Educación Superior (CUN). Nuestro objetivo es mostrar las habilidades clave aprendidas que permitan destacar en un entorno tecnológico en constante evolución."
    )
    if st.button("👨🏽‍🔬Contact Me"):
        show_contact_form()
st.write("_____")

# Header
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./img/vida.png", width=230)
with col2:
    st.title("Victor Guzmán-Brand", anchor=False)
    st.write(
        """ 
        - Estudiante de Ingeniería de Sistemas (10 semestre) 
        - Corporación Unificada Nacional de Educación Superior (CUN) 
        - Email: victora.guzman@cun.edu.co
        - https://scholar.google.com/citations?user=a27XGQcAAAAJ&hl=es
        """
    )
        
    
st.write("____")
#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="text-align: center; color: #FF004D;">Insigh Colombia</h1>
            <h4>📊Transforma datos en decisiones de vida🌸</h4>
        </div>
    """, unsafe_allow_html=True)


