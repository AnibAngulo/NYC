import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

DATA_URL='citibike-tripdata.csv'

#CONFIGURACIÓN DEL SITIO
st.title('Caso de Citibke Trip Data')

#CARGAR DATOS
@st.cache
def load_data(nrows=500):
    data = pd.read_csv(DATA_URL,nrows=nrows)
    
    #Obtener columna de hora de inicio de viajes
    data['started_at']= pd.to_datetime(data['started_at'])
    horas_inicio = []
    fechas_inicio = data['started_at'].to_list()
    for fecha in fechas_inicio:
        hora = fecha.hour
        horas_inicio.append(hora)
    data['started_at_hour'] = horas_inicio

    #Renombrar columnas de start_lat y start_lng a
    #lat y lon respectivamente para mapear más adelante
    data.rename(columns = {'start_lat':'lat', 'start_lng':'lon'}, inplace = True)

    return data

data = load_data(nrows=10000)

#CREAR SIDEBAR
sidebar = st.sidebar

#CHECKBOX PARA MOSTRAR DATOS
#Se hace el slider para seleccionar por hora
hour_select = sidebar.slider(
    "Selecciona la Hora",
    min_value = int(data['started_at_hour'].min()),
    max_value = int(data['started_at_hour'].max()),
    step=1
)
subset_hour = data[(data['started_at_hour']==hour_select)]

#Se implementa la lógica con el checkbox
agree = sidebar.checkbox('Mostrar Datos')
if agree:
    st.write('Datos Mostrados')
    st.dataframe(subset_hour)

#GRÁFICA - NÚMERO DE RECORRIDOS POR HORA

#Funcion para obtener las frecuencias de viaje por hora
def TripsHour(data):
    inicio_horas_viaje = data.started_at_hour.value_counts().rename_axis('Hora').reset_index(name='CantidadViajes')
    inicio_horas_viaje.sort_values(by='Hora',inplace=True)
    return inicio_horas_viaje

inicio_horas_viaje = TripsHour(data)

#Graficar los conteos de viajes por hora
fig1 = px.bar(inicio_horas_viaje, x='Hora', y='CantidadViajes',title='Viajes por Hora (Formato 24hrs)')
fig1.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 1
    )
)

agree2 = sidebar.checkbox('Mostrar Viajes por Hora')
if agree2:
    st.write('Viajes por Hora')
    st.plotly_chart(fig1)


#GRÁFICA MAPA - UBICACIÓN DE RECORRIDOS POR HORA
st.map(subset_hour[['lat','lon']])