import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Home",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    '<h1 style="text-align: center; font-size: 50px; color: #0b2d43">Una mirada a la Situación</h1>',
    unsafe_allow_html=True
)

# Función animación
def load_lottieurl(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()
  
#BODY
#Primera parte
lottie_coding1 = load_lottieurl("https://lottie.host/09ffa171-b748-418a-90a5-6c0b9f061887/1ZFDNxKkg7.json")

with st.container():
  st.write("---")
  st.write(f'<h6 style="text-align: left; color: #154360;">🌐Analítica de datos e investigación aplicada</h6>',
    unsafe_allow_html=True
)

  # Verifica si la variable de sesión "visit_count" ya existe
  if 'visit_count' not in st.session_state:
      # Si no existe, inicializa el contador a 0
      st.session_state.visit_count = 0

  # Incrementa el contador en cada visita
  st.session_state.visit_count += 1

  # Muestra el número actual de visitas
  st.write(f"Number of visits: {st.session_state.visit_count}")

    
  left_column, right_column = st.columns(2)
  with left_column:
    st.write(
    f'<h2 style="text-align: center; color: #133E87;">Conducta Suicida</h2>',
    unsafe_allow_html=True
    )
    st.write(
      """
       Cada año, alrededor de 703.000 personas mueren por suicidio en todo el mundo, afectando a familias y comunidades de manera devastadora. Este problema no discrimina por edad o ubicación geográfica y es la cuarta causa principal de muerte entre los jóvenes de 15 a 29 años, con más del 77% de los casos ocurriendo en países de ingresos bajos y medios (Organización Mundial de la Salud, 2021). En Colombia, desde 2016, se ha presentado un aumento en los comportamientos suicidas, con un total de 28.615 intentos de suicidio en 2018, lo que equivale a un promedio diario de 78.4 casos (Ministerio de Salud y Protección Social, 2021).

      """
    )
  with right_column:
    st_lottie(lottie_coding1, height=300, key="coding1")

#Segunda parte
lottie_coding2 = load_lottieurl("https://lottie.host/00992b92-d3fa-4f13-bffd-1b9d31c64092/b41QWHKkNx.json")

with st.container():
  
  left_column, right_column = st.columns(2)
  with left_column:
    st_lottie(lottie_coding2, height=300, key="coding2")
  with right_column:
    st.write(
    f'<h2 style="text-align: center; color: #133E87;">Redes Sociales</h2>',
    unsafe_allow_html=True
    )
    st.write(
      """
        Las redes sociales son un espacio complejo donde se mezclan conversaciones sobre el suicidio con ayuda y agresión, lo que puede afectar negativamente a quienes se sienten socialmente aislados. Es importante considerar las redes sociales como herramientas para la detección y prevención del suicidio, ya que permiten identificar a personas en riesgo, difundir información sobre recursos y combatir el estigma (Mendoza-Palma & Mera-Holguín, 2019; Molina & Restrepo, 2018; Arilla-Andres et al., 2022).
      """
    )

#Tercer parte
lottie_coding3 = load_lottieurl("https://lottie.host/fd02cf23-2cbc-48cf-acc6-3ff950acf88c/iu6Jdj5Hat.json")

with st.container():
  st.write("---")
  left_column, right_column = st.columns(2)
  with left_column:
    st.write(
    f'<h2 style="text-align: center; color: #133E87;">Procesamiento del lenguaje natural (PLN)</h2>',
    unsafe_allow_html=True
    )
    st.write(
      """
       El procesamiento del lenguaje natural (PLN) utiliza técnicas de aprendizaje automático para analizar y comprender el texto, permitiendo a las organizaciones extraer información relevante de los textos, como opiniones en redes sociales y interacciones con clientes. Integra lingüística, informática e inteligencia artificial para que las computadoras comprendan, procesen y produzcan lenguaje humano (Giraldo-Forero & Orozco-Duque, 2023).
      """
    )
  with right_column:
    st_lottie(lottie_coding3, height=300, key="coding3")



referencias = """
- **Ministerio de Salud y Protección Social**(2021)Prevención de la Conducta Suicida en Colombia (pp. 1-57). Ministerio de Salud y Protección Social. https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/VS/PP/ENT/estrategia-nacional-conducta-suicida-2021.pdf.
- **Organización Mundial de la Salud**(2021)Suicidio. https://www.who.int/es/news-room/fact-sheets/detail/suicide.
- **Mendoza-Palma, K., & Mera-Holguín, G.**(2019)Adicción a las redes sociales y conducta suicida en los adolescentes de Montecristi. Revista Científica y Arbitrada de Psicología NUNA YACHAY - ISSN: 2697-3588., 2(3), 1-15. https://publicacionescd.uleam.edu.ec/index.php/nuna-yachay/article/view/113.
- **Molina, M., & Restrepo, D.** (2018) Internet y comportamiento suicida en adolescentes: ¿cuál es la conexión? Pediatría, 51(2), Article 2. https://doi.org/10.14295/pediatr.v51i2.109.
- **Arilla-Andres, S., Garcia-Martinez, C., & Lpez-Del Hoyo, Y.**(2022)Detección del riesgo de suicidio a través de las redes sociales. Revista Internacional de Tecnología Ciencia y Sociedad, 5(6), 2-14. https://doi.org/10.37467/revtechno.v11.4384.
- **Google Cloud**(2023)¿Qué es el procesamiento del lenguaje natural? Google Cloud. https://cloud.google.com/learn/what-is-natural-language-processing?hl=es.
- **Giraldo-Forero, A., & Orozco-Duque, A.**(2023) Evolución del procesamiento natural del lenguaje. TecnoLógicas, 26(56), 1-20. https://doi.org/10.22430/22565337.2687.
- **Ministerio de Salud y Protección Social**(2024)Sistema de Vigilancia en Salud Pública.MINSALUD.https://www.minsalud.gov.co/proteccionsocial/Paginas/SIVIGILA.aspx
- **Frolopiaton Palm**(2024)Foto planta de hojas tropicales de lujo y follaje fondo exótico abstracto de botánica.freepik.https://img.freepik.com/fotos-premium/planta-hojas-tropicales-lujo-follaje-fondo-exotico-abstracto-botanica_31965-76935.jpg?w=900
- **Animation - 1709231763757**(2024).lottiefiles.https://lottie.host/embed/c9728df7-44e0-4e2c-962a-33d6447942dd/7wrIUY9tAK.json
- **Animation - 1709249736481**(2024).lottiefiles.https://lottie.host/embed/09ffa171-b748-418a-90a5-6c0b9f061887/1ZFDNxKkg7.json
- **Animation - 1709332817581**(2024).lottiefiles.https://lottie.host/embed/00992b92-d3fa-4f13-bffd-1b9d31c64092/b41QWHKkNx.json
- **Animation - 1709175926206**(2024).lottiefiles.https://lottie.host/embed/0b2ea179-7204-4517-8f9d-c87069824c66/ZKQCRKr0qv.json
- **Streamlit**(2024)Crafting a Dashboard App in Python using Streamlit.Streamlit.https://www.youtube.com/watch?v=asFqpMDSPdM&t=1128s
- **Codificando Bits**(2020).Análisis de sentimientos con BERT en Python (Tutorial).https://www.youtube.com/watch?v=mvh7DV84mr4
- **google-bert**(2019)google-bert/bert-base-cased.Hugging Face.https://huggingface.co/google-bert/bert-base-cased
-**Sistemas Inteligentes**(2022)Detección de emociones en tiempo real | Redes neuronales convolucionales | Face emotion |Tensorflow.https://www.youtube.com/watch?v=Jaai8JLNlIc&t=17s
-**Oheix, J.(2019)Face expression recognition dataset.Kaggle.https://www.kaggle.com/datasets/jonathanoheix/face-expression-recognition-dataset

"""

def stream_data():
    for word in referencias.split():
        yield word + " "
        time.sleep(0.02)


    for word in referencias.split():
        yield word + " "
        time.sleep(0.02)


if st.button("Referencias Bibliográficas"):
    st.write_stream(stream_data)

st.write("---")

#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3 style= "color: #FF004D;">🌸Insigh Colombia</h3>
        </div>
    """, unsafe_allow_html=True)
  
