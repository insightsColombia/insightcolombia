import streamlit as st
import torch
import speech_recognition as sr
import torch.nn.functional as F 
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Análisis Conducta-Suicida",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path del modelo preentrenado
MODEL_PATH = 'modelo_entrenado.pth'



# Cargar el tokenizador y el modelo preentrenado
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', output_attentions=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Cargar los pesos entrenados
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

def classifySentiment(review_text):
    # Configurar el modelo en modo de evaluación
    model.eval()

    encoding_review = tokenizer.encode_plus(
        review_text,
        max_length=200,
        truncation=True,
        add_special_tokens=True,
        return_token_type_ids=False,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt'
    )

    input_ids = encoding_review['input_ids'].to(device)
    attention_mask = encoding_review['attention_mask'].to(device)

    # Desactivar el cálculo de gradientes para la inferencia
    with torch.no_grad():
        output = model(input_ids, attention_mask)
        attention_scores = output.attentions[-1]  

    # Obtener la predicción y calcular la confianza
    prediction = torch.argmax(output.logits, dim=1)
    probs = F.softmax(output.logits, dim=1)
    confidence = probs[0][prediction.item()].item() * 100  

    # Mostrar resultado y confianza
    if prediction.item() == 1:
        return "ALTA", confidence, attention_scores  
    else:
        return "BAJA", confidence, attention_scores  
    


def main():
    st.write(
        f'<h1 style="text-align: center; font-size: 50px; color: #0b2d43;">Sistema de Clasificación de Ideación Suicida en Textos</h1>',
        unsafe_allow_html=True
    )
    st.write(""" 
       Presentamos nuestro servicio de análisis de texto y audio, basado en el modelo preentrenado BERT (Bidirectional Encoder Representations from Transformers), para abordar la preocupante incidencia de ideación suicida. Reconociendo la importancia crítica de detectar tempranamente señales de angustia mental, nuestro sistema utiliza algoritmos avanzados para identificar patrones suicidas en comunicaciones escritas y verbales. Con un enfoque en el procesamiento de lenguaje natural y análisis de sentimientos, esta herramienta ofrece una visión oportuna para profesionales de la salud mental, instituciones educativas y plataformas de redes sociales, potencialmente salvando vidas.
    """)

    # Definir message como una cadena vacía por defecto
    message = ""
    
    # Selección de fuente de entrada
    input_option = st.radio("Seleccione una opción de entrada:", ("Texto", "Audio"))

    if input_option == "Texto":
        message = st.text_area("Ingrese el texto:")
    elif input_option == "Audio":
        st.write("Haga clic en el botón para comenzar a grabar.")
        if st.button("Grabar"):
            # Inicia el reconocimiento de voz
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Grabando...")
                audio_data = recognizer.listen(source)
                st.write("¡Grabación completada!")
            
            # Transcribe el audio a texto
            try:
                message = recognizer.recognize_google(audio_data)
                st.write("Texto transcrito:", message)
            except sr.UnknownValueError:
                st.error("No se pudo entender el audio.")
            except sr.RequestError as e:
                st.error("Error en la solicitud al servicio de reconocimiento de voz; {0}".format(e))
    
    # El botón de predicción se utiliza para iniciar el procesamiento
    if st.button("Predicción"):
        if input_option == "Texto" or input_option == "Audio":
            prediction, confidence, attention_scores = classifySentiment(message)
            st.success(f"El modelo clasifica la ideación suicida como: {prediction.upper()}")
            st.info(f"Confianza de la predicción: {confidence:.2f}%")

            # Obtener los tokens de la entrada
            tokens = tokenizer.tokenize(message)
    
    with st.container():
        st.write("Este resultado es una estimación del modelo. Utilizar la información con precaución.")

if __name__ == '__main__':
    main()

st.write("____")
#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3 style= "color: #FF004D;">🌸Insigh Colombia</h3>
        </div>
    """, unsafe_allow_html=True)
