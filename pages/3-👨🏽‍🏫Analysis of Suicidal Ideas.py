import streamlit as st
import torch
import speech_recognition as sr
import torch.nn.functional as F
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
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

# Cargar los pesos entrenados y manejar errores
try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    st.success("Modelo cargado exitosamente.")
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")

def classifySentiment(review_text):
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

    with torch.no_grad():
        output = model(input_ids, attention_mask)
        attention_scores = output.attentions[-1] if output.attentions else None

    prediction = torch.argmax(output.logits, dim=1)
    probs = F.softmax(output.logits, dim=1)
    confidence = probs[0][prediction.item()].item() * 100

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
       Este sistema analiza texto y audio para detectar patrones de ideación suicida usando modelos avanzados de NLP.
    """)

    message = ""
    input_option = st.radio("Seleccione una opción de entrada:", ("Texto", "Audio"))

    if input_option == "Texto":
        message = st.text_area("Ingrese el texto:")
    elif input_option == "Audio":
        st.write("Haga clic en el botón para comenzar a grabar.")
        if st.button("Grabar"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("Grabando...")
                audio_data = recognizer.listen(source)
                st.write("¡Grabación completada!")
            try:
                message = recognizer.recognize_google(audio_data)
                st.write("Texto transcrito:", message)
            except sr.UnknownValueError:
                st.error("No se pudo entender el audio.")
            except sr.RequestError as e:
                st.error(f"Error en el reconocimiento de voz: {e}")

    if st.button("Predicción"):
        if message:
            prediction, confidence, attention_scores = classifySentiment(message)
            st.success(f"El modelo clasifica la ideación suicida como: {prediction.upper()}")
            st.info(f"Confianza de la predicción: {confidence:.2f}%")

            tokens = tokenizer.tokenize(message)

    with st.container():
        st.write("Este resultado es una estimación del modelo. Utilizar la información con precaución.")

if __name__ == '__main__':
    main()

st.write("____")
# FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3 style= "color: #FF004D;">🌸Insight Colombia</h3>
        </div>
    """, unsafe_allow_html=True)
