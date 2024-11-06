import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

from streamlit_option_menu import option_menu
import json
from urllib.request import urlopen
import altair as alt
import pickle
import datetime as dt
import xgboost as xgb

with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
    counties = json.load(response)

# Configuración de la página
st.set_page_config(page_title="Panel de Control", page_icon=":bar_chart:", layout="wide")

st.markdown(
    '<h1 style="text-align: center; font-size: 50px; color: #0b2d43">Registros de Intentos de Suicidio en Colombia</h1>',
    unsafe_allow_html=True
)


#______________________________________Estilos CSS______________________________________#
# Cargar el archivo CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Llamar el archivo CSS
local_css("style/styleF.css")

#____________________________________ Cargar el archivo y los datos_____________________________________________#


fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])
if fl is not None:
    df = pd.read_csv(fl)
else:
    df = pd.read_csv("data/datos_generales.csv")  
    
#____________________________________Conversión de fecha y filtrado por fechas_____________________________________________#
 
df["FEC_NOT"] = pd.to_datetime(df["FEC_NOT"])
startDate, endDate = df["FEC_NOT"].min(), df["FEC_NOT"].max()

col1, col2 = st.columns(2)
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df_filtered = df[(df["FEC_NOT"] >= date1) & (df["FEC_NOT"] <= date2)].copy()
    
#____________________________________Selección de filtros por Región, Departamento y Municipio_________________________#


st.sidebar.header("Choose your filter:")
region = st.sidebar.multiselect("Pick your Region", df_filtered["Region"].unique())
state = st.sidebar.multiselect("Pick your State", df_filtered["Departamento"].unique())
city = st.sidebar.multiselect("Pick your City", df_filtered["Municipio"].unique())

# Aplicar filtros

filtered_df = df_filtered
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if state:
    filtered_df = filtered_df[filtered_df["Departamento"].isin(state)]
if city:
    filtered_df = filtered_df[filtered_df["Municipio"].isin(city)]

#____________________________________Mostrar los datos filtrados de manera desplegable y descargar_________________________#

with st.expander("🔎View filtered data"):
    st.write(filtered_df)  
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download filter /.csv",
        data=csv,
        file_name='datos_filtrados.csv',
        mime='text/csv'
    )
#_______________________________________________________FIGURA GENERAL_______________________________________________________#
col = st.columns((1.0, 4.5), gap='medium')

with col[0]:
    with st.container():
        st.write(f'<h3 style="text-align: center; color: #0d9ca7;">Estadística General</h3>',
                 unsafe_allow_html=True)

    state_count = filtered_df.shape[0] if 'filtered_df' in locals() else 0
    st.markdown(f'''
        <div class="card-dos">
            <div class="card-header">🗣️Total Casos</div>
            <div class="card-body">
                <h3 style="color: #dd0034;">{state_count:,}</h3>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    edad = filtered_df['EDAD'].mean() if not filtered_df.empty else 0
    edad = round(edad)
    st.markdown(f'''
        <div class="card-dos">
            <div class="card-header">👤Edad Promedio</div>
            <div class="card-body">
                <h3 style="color: #dd0034;">{edad:,} años</h3>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Calcular el sexo con mayor número de casos en el DataFrame filtrado
    sexo_counts = filtered_df.groupby('SEXO').size().reset_index(name='cantidad')
    max_row = sexo_counts.loc[sexo_counts['cantidad'].idxmax()]
    max_sexo = max_row['SEXO']
    max_casos = max_row['cantidad']

    with st.container():
        st.markdown(f'''
            <div class="card-dos">
                <div class="card-header">👥Sexo</div>
                <div class="card-body">
                    <h3 style="color: #dd0034;">{max_sexo} ({max_casos:,})</h3>
                </div>
            </div>
            ''', unsafe_allow_html=True)

    # Calcular el tipo de seguridad social con mayor número de casos
    ss_counts = filtered_df.groupby('TIP_SS').size().reset_index(name='cantidad')
    max_row = ss_counts.loc[ss_counts['cantidad'].idxmax()]
    max_ss = max_row['TIP_SS']
    max_casos = max_row['cantidad']

    with st.container():
        st.markdown(f'''
            <div class="card-dos">
                <div class="card-header">👥Seguridad Social</div>
                <div class="card-body">
                    <h3 style="color: #dd0034;">{max_ss} ({max_casos:,})</h3>
                </div>
            </div>
            ''', unsafe_allow_html=True)

# _______________________________________________________FIGURA MAPA_______________________________________________________#
with col[1]:
    filtered_df_for_map = filtered_df.copy()
    if 'Cantidad' not in filtered_df_for_map.columns:
        filtered_df1 = filtered_df_for_map.groupby('Departamento').size().reset_index(name='Cantidad')

    fig = go.Figure(go.Choroplethmapbox(
        geojson=counties,
        locations=filtered_df1['Departamento'], 
        z=filtered_df1['Cantidad'],
        colorscale="turbo",
        featureidkey="properties.NOMBRE_DPT",
        marker_opacity=0.7,
        marker_line_width=1,
    ))

    if state:
        for dept in state:
            dept_data = filtered_df1[filtered_df1["Departamento"] == dept]
            fig.add_trace(go.Choroplethmapbox(
                geojson=counties,
                locations=dept_data['Departamento'],
                z=dept_data['Cantidad'],
                colorscale="Reds",
                featureidkey="properties.NOMBRE_DPT",
                marker_opacity=0.8,
                marker_line_width=2,
                name=f"Dept: {dept}"
            ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 4.5709, "lon": -74.2973},
        title="Mapa de Departamentos Seleccionados",
        height=900
    )

    st.plotly_chart(fig, use_container_width=True)

#_______________________________________________________FIGURA DE BARRAS/GENERAL_______________________________________________________#
# Función para crear la figura general
def crear_figura_general(dataframe):
    fig = go.Figure()
    agru_ano_df = dataframe.groupby('AÑO').size().reset_index(name='cantidad')

    # Gráfico de barras
    fig.add_trace(go.Bar(
        x=agru_ano_df["AÑO"],
        y=agru_ano_df["cantidad"],
        name="Total"
    ))

    # Línea de tendencia
    fig.add_trace(go.Scatter(
        x=agru_ano_df["AÑO"],
        y=agru_ano_df["cantidad"],
        mode="lines+markers",
        marker=dict(size=5),
        line=dict(dash="dot"),
        name="Tendencia General"
    ))

    fig.update_layout(
        title="Casos por Año (Figura General)",
        xaxis_title="Año",
        yaxis_title="Cantidad de Casos",
        template="seaborn",
        height=400,
    )
    return fig

# Inicializar la figura con o sin filtros
if not (region or state or city):
    # Mostrar la figura general mientras no haya filtros aplicados
    fig = crear_figura_general(df_filtered)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Selecciona una región, departamento o ciudad para ver un desglose específico.")
       
else:
    # Generar la figura con filtros aplicados
    fig = go.Figure()
    color_palette = px.colors.qualitative.Plotly

    # Generar trazos para cada filtro seleccionado
    if region:
        for i, reg in enumerate(region):
            reg_df = filtered_df[filtered_df["Region"] == reg]
            agru_ano_df = reg_df.groupby('AÑO').size().reset_index(name='cantidad')
            fig.add_trace(go.Bar(x=agru_ano_df["AÑO"], y=agru_ano_df["cantidad"], name=f"Región: {reg}",
                                 marker=dict(color=f"rgba({50+i*50}, {100+i*40}, {200-i*30}, 0.7)")))
            # Añadir línea de tendencia
            fig.add_trace(
                        go.Scatter(
                            x=agru_ano_df["AÑO"],
                            y=agru_ano_df["cantidad"],
                            mode="lines+markers",
                            marker=dict(size=5),
                            line=dict(dash="dot"),
                            name=f"Tendencia Dept: {reg}"
                        )
                    )

    if state:
        for i, dp in enumerate(state):
            st_df = filtered_df[filtered_df["Departamento"] == dp]
            agru_ano_df = st_df.groupby('AÑO').size().reset_index(name='cantidad')
            fig.add_trace(go.Bar(x=agru_ano_df["AÑO"], y=agru_ano_df["cantidad"], name=f"Depto: {dp}",
                                 marker=dict(color=f"rgba({150+i*30}, {50+i*40}, {100-i*20}, 0.7)")))
            fig.add_trace(
                        go.Scatter(
                            x=agru_ano_df["AÑO"],
                            y=agru_ano_df["cantidad"],
                            mode="lines+markers",
                            marker=dict(size=5),
                            line=dict(dash="dot"),
                            name=f"Tendencia Dept: {dp}"
                        )
                    )

    if city:
        for i, ct in enumerate(city):
            ct_df = filtered_df[filtered_df["Municipio"] == ct]
            agru_ano_df = ct_df.groupby('AÑO').size().reset_index(name='cantidad')
            fig.add_trace(go.Bar(x=agru_ano_df["AÑO"], y=agru_ano_df["cantidad"], name=f"Ciudad: {ct}",
                                 marker=dict(color=f"rgba({100+i*40}, {150-i*30}, {50+i*20}, 0.7)")))
            fig.add_trace(
                        go.Scatter(
                            x=agru_ano_df["AÑO"],
                            y=agru_ano_df["cantidad"],
                            mode="lines+markers",
                            marker=dict(size=5),
                            line=dict(dash="dot"),
                            name=f"Tendencia Dept: {ct}"
                        )
                    )

    # Configurar y mostrar la figura con los filtros aplicados
    fig.update_layout(
        title="Comparación de Casos por Año",
        xaxis_title="Año",
        yaxis_title="Cantidad de Casos",
        barmode='group',
        template="seaborn",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

st.write("____")

#________________________________________________FIGURA BARRAS ETAPA DESARROLLO________________________________________________#


col1, col2, col3 = st.columns(3)
with col1:
    if not filtered_df.empty:
        # Agrupar y contar los datos por año y etapa de desarrollo
        etapa_counts = filtered_df.groupby(['AÑO', 'Etapa_Desarrollo']).size().reset_index(name='Cantidad')

        # Inicializar la figura
        fig = go.Figure()

        # Colores para cada etapa
        colors = ["#0000ff", "#00ff00", "#80ff00", "#ff8000", "#ffff00", "#ffff80"]
        etapas = etapa_counts['Etapa_Desarrollo'].unique()  # Las etapas únicas de desarrollo

        # Crear un diccionario para almacenar las cantidades acumulativas
        acumulado = pd.Series(0, index=etapa_counts["AÑO"].unique())

        # Crear trazos apilados para cada etapa
        for i, etapa in enumerate(etapas):
            etapa_data = etapa_counts[etapa_counts['Etapa_Desarrollo'] == etapa]
            acumulado += etapa_data.set_index("AÑO")["Cantidad"]  # Sumar la cantidad acumulada

            fig.add_trace(
                go.Scatter(
                    x=etapa_data["AÑO"],
                    y=acumulado,
                    mode='lines',
                    line=dict(width=0.7, color=colors[i]),
                    fill='tonexty',
                    name=etapa,
                )
            )

        # Personalizar el diseño del gráfico
        fig.update_layout(
            title="Distribución de Etapas de Desarrollo por Año",
            xaxis_title="Año",
            yaxis_title="Cantidad",
            template="seaborn",
            showlegend=True,
            legend=dict(title="Etapas de Desarrollo"),
            height=500,
        )

        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar. Seleccione otra combinación de filtros.")
#_______________________________________________________FIGURA SEXO_______________________________________________________#
with col2:
    if not filtered_df.empty:
        # Agrupar y contar los datos por año y sexo
        sexo_counts = filtered_df.groupby(['AÑO', 'SEXO']).size().reset_index(name='Cantidad')

        # Crear el gráfico de barras
        fig = px.bar(sexo_counts, 
                     x='AÑO', 
                     y='Cantidad', 
                     color='SEXO',
                     title="Cantidad de Casos por Tipo",
                     color_discrete_map={'M': 'rgba(0, 0, 255, 0.5)', 'F': 'rgba(255, 0, 0, 0.5)'},  # Colores personalizados
                     barmode='relative')  # Para crear barras apiladas

        # Personalizar el diseño del gráfico
        fig.update_layout(
            xaxis_title="Año",
            yaxis_title="Cantidad",
            template="seaborn",
            height=500,
        )

        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar. Seleccione otra combinación de filtros.")

#_______________________________________________________FIGURA REGION_______________________________________________________#
        
with col3:

    custom_colors = ["rgba(0, 0, 255, 0.5)", "rgba(255, 0, 0, 0.5)", "rgba(0, 255, 0, 0.5)",
                    "rgba(255, 165, 0, 0.5)", "rgba(255, 255, 0, 0.5)", "rgba(240, 240, 240, 0.5)"]

    counts = filtered_df.groupby(['Region']).size().reset_index(name='Cantidad')

    fig = px.pie(counts, values="Cantidad", names="Region", template="plotly_dark",
                color_discrete_sequence=custom_colors, title="Distribución por Región",)

    fig.update_layout(
        title={ 
            'font': {
                'size': 16 
            }
        }
    )

    fig.update_traces(text=counts["Region"], textposition="inside")

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)


st.write("____")


# Cargar los datos
df_reshaped = pd.read_csv('data/intentos-2016-2023.csv')

# Verificar si las columnas necesarias están en el DataFrame
if {'año', 'departamento', 'casos'}.issubset(df_reshaped.columns):
    # Crear el mapa de calor
    heatmap = px.density_heatmap(
        df_reshaped,
        x='año',
        y='departamento',
        z='casos',
        color_continuous_scale="turbo",
        labels={'año': 'Año', 'departamento': 'Departamento', 'casos': 'Cantidad de Casos'},
        title="Mapa de Calor: Casos por Año y Departamento"
    )

    # Configurar el diseño del gráfico
    heatmap.update_layout(
        xaxis_title="Año",
        yaxis_title="Departamento",
        template="seaborn",  # Alineado con el resto del proyecto
        height=500
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(heatmap, use_container_width=True)
else:
    st.warning("El archivo CSV no tiene las columnas necesarias: 'año', 'departamento' y 'casos'.")

st.write("____")
#_______________________________________________________XGBOOST_______________________________________________________#

col = st.columns((4.5, 0.9), gap='medium')

with col[0]:

    # Asegurarse de que la columna de fecha esté en formato datetime
    df['FEC_NOT'] = pd.to_datetime(df['FEC_NOT'])

    # Crear columnas 'year', 'month', etc., en el DataFrame original
    df['year'] = df['FEC_NOT'].dt.year
    df['month'] = df['FEC_NOT'].dt.month

    # Crear atributos temporales adicionales
    def create_attributes(dataframe):
        df = dataframe.copy()
        df['day'] = df['FEC_NOT'].dt.day
        df['dayofweek'] = df['FEC_NOT'].dt.dayofweek
        df['month'] = df['FEC_NOT'].dt.month
        df['quarter'] = df['FEC_NOT'].dt.quarter
        df['year'] = df['FEC_NOT'].dt.year
        df['dayofyear'] = df['FEC_NOT'].dt.dayofyear
        return df

    # Aplicar la función para obtener los datos históricos con todos los atributos
    df2 = create_attributes(df)

    # Cargar el modelo
    with open("xgboost_model.pkl", "rb") as file:
        model = pickle.load(file)

    # Obtener DataFrame filtrado según región, departamento o municipio
    def get_filtered_data(df, region=None, state=None, city=None):
        filtered_df = df.copy()
        if region and 'Region' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Region'].isin(region)]
        elif state and 'Departamento' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Departamento'].isin(state)]
        elif city and 'Municipio' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Municipio'].isin(city)]
        return filtered_df


    # Crear DataFrame con los atributos temporales para las predicciones
    def get_prediction_dates(start_year=2024, end_year=2025):
        future_dates = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='D')
        future_df = pd.DataFrame(future_dates, columns=['FEC_NOT'])
        future_df = create_attributes(future_df)
        return future_df

    # Realizar predicciones usando el modelo cargado
    def get_predictions(model, future_df):
        predictions = model.predict(future_df[['day', 'dayofweek', 'month', 'quarter', 'year', 'dayofyear']])
        future_df['predicted_cases'] = predictions
        return future_df

    # Aplicar los filtros seleccionados por el usuario
    filtered_df = get_filtered_data(df, region, state, city)

    # Convertir las fechas de los datos históricos a nivel mensual
    filtered_df['FEC_NOT'] = pd.to_datetime(filtered_df['FEC_NOT'])
    filtered_df.set_index('FEC_NOT', inplace=True)

    # Agregar los datos históricos por mes y obtener el total de casos en cada mes
    historical_monthly = filtered_df.resample('M').size().reset_index(name='cases')

    # Crear DataFrame con los atributos temporales para las predicciones
    def get_monthly_predictions(model, start_year=2024, end_year=2025, region=None, state=None, city=None):
        future_dates = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='D')
        future_df = pd.DataFrame(future_dates, columns=['FEC_NOT'])
        future_df = create_attributes(future_df)

        # Filtrar el DataFrame de predicciones según región, estado o ciudad
        if region or state or city:
            # Esto asume que los filtros de región, estado, ciudad se aplican a las características de futuro_df
            future_df = get_filtered_data(future_df, region, state, city)

        # Realizar las predicciones
        predictions = model.predict(future_df[['day', 'dayofweek', 'month', 'quarter', 'year', 'dayofyear']])
        future_df['predicted_cases'] = predictions

        # Agregar predicciones a nivel mensual
        future_df.set_index('FEC_NOT', inplace=True)
        monthly_predictions = future_df['predicted_cases'].resample('M').sum().reset_index()
        return monthly_predictions


    # Obtener las predicciones mensuales con los filtros seleccionados
    future_predictions = get_monthly_predictions(model, 2024, 2025, region=region, state=state, city=city)


    # Inicializar la figura
    fig = go.Figure()

    # Añadir los datos históricos a la figura como barras
    fig.add_trace(go.Bar(
        x=historical_monthly['FEC_NOT'],
        y=historical_monthly['cases'],
        name="Casos Históricos",
        marker_color='blue'
    ))

    # Añadir las predicciones como barras en lugar de línea
    fig.add_trace(go.Bar(
        x=future_predictions['FEC_NOT'],
        y=future_predictions['predicted_cases'],
        name="Predicción de Casos",
        marker_color='orange'  # Color de las barras de predicción
    ))

    # Configuración de la figura
    fig.update_layout(
        title="Predicción de Casos por medio de series temporales algoritmo Xgboost / machine learning",
        xaxis_title="Fecha",
        yaxis_title="Número de Casos",
        barmode='group',
        template="plotly_dark",
        height=500,
        legend=dict(font=dict(size=12)),
    )

    st.plotly_chart(fig, use_container_width=True)

with col[1]:
    # Calcula el total de casos predichos para el año 2024
    total_2024 = future_predictions[future_predictions['FEC_NOT'].dt.year == 2024]['predicted_cases'].sum()
    with st.container():
            st.markdown(f'''
                <div class="card-dos">
                    <div class="card-header">👥Predicción[2024]</div>
                    <div class="card-body">
                        <h3 style="color: #dd0034;">{total_2024:,}</h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

#_______________________________________________________FOOTER_______________________________________________________#

with st.expander('🧰Metricas de evaluación', expanded=False):
  st.write(('''
            - Mean Absolute Error (MAE): 1.1486
            - Mean Squared Error (MSE): 2.5180
            - Root Mean Squared Error (RMSE): 1.5868
            - Mean Absolute Percentage Error (MAPE): 0.0153
            - R-squared (R2): 0.9967
            - Prueba de Dickey-Fuller: p-value / 0.007265
            ''')
  )


with st.container():
    st.write('''
            - Data: [Datos Abiertos] [www.datos.gov.co](https://www.datos.gov.co/en/browse?q=Intento%20de%20suicidio&sortBy=relevance)  -  [Sistema Nacional de Vigilancia en Salud Pública -SIVIGILA](https://portalsivigila.ins.gov.co/Paginas/Buscador.aspx#) [Intentos de Suicidio].
            ''')

st.write("____")
#FOOTER
with st.container():
    st.markdown("""
        <div style="text-align: center;">
            <h3 style= "color: #FF004D;">🌸Insigh Colombia</h3>
        </div>
    """, unsafe_allow_html=True)