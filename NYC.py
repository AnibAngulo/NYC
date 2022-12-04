#Anibal Jose Angulo Cardoza
#A01654684

import streamlit as st
import pandas as pd
import plotly.express as px

DATA_URL='citibike-tripdata.csv'

st.title('Caso de Citibke Trip Data')
st.subheader("Anibal Angulo - A01654684")

@st.cache
def load_data(nrows=500):
    data = pd.read_csv(DATA_URL,nrows=nrows)
    data['started_at']= pd.to_datetime(data['started_at'])
    horas_inicio = []
    fechas_inicio = data['started_at'].to_list()
    for fecha in fechas_inicio:
        hora = fecha.hour
        horas_inicio.append(hora)
    data['started_at_hour'] = horas_inicio
    data.rename(columns = {'start_lat':'lat', 'start_lng':'lon'}, inplace = True)

    return data

data = load_data(nrows=10000)

sidebar = st.sidebar

hour_select = sidebar.slider(
    "Selecciona la Hora",
    min_value = int(data['started_at_hour'].min()),
    max_value = int(data['started_at_hour'].max()),
    step=1
)
subset_hour = data[(data['started_at_hour']==hour_select)]

agree = sidebar.checkbox('Mostrar Datos')
if agree:
    st.write('Datos Mostrados')
    st.dataframe(subset_hour)

def TripsHour(data):
    inicio_horas_viaje = data.started_at_hour.value_counts().rename_axis('Hora').reset_index(name='CantidadViajes')
    inicio_horas_viaje.sort_values(by='Hora',inplace=True)
    return inicio_horas_viaje

inicio_horas_viaje = TripsHour(data)

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

st.map(subset_hour[['lat','lon']])