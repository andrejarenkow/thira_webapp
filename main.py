# Webapp THIRA

#Importação das bibliotecas
import numpy as np
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout, Heatmap
import plotly.graph_objs as go
import streamlit as st
import matplotlib

# Configurações da página
st.set_page_config(
    page_title="THIRA CDC",
    page_icon="	:rotating_light:",
    layout="wide",
    initial_sidebar_state='collapsed'
) 
col1, col2, col3 = st.columns([2,12,1])

col1.image('CDC_THIRA/marca RS23 cor vertical saude_RGB.png', width=200)
col2.title('THIRA')
col3.image('CDC_THIRA/US_CDC_logo.svg.png', width=100)

#Aquisição dos dados
dados = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTuoMf8l-MlrVDCnklOQeLZ2OILF1GHjJxlLwW_ZiJAeGd5hMtxrRdhIgAlme0JDGVG-T8N2Ul6Fvso/pub?gid=550571158&single=true&output=csv')
dados.columns = ['Carimbo de data/hora', 'Nome',
       'Probabilidade','Morbidade','Mortalidade','Inst. Social','Imp. Econômico','Saúde']
dados['subtotal'] = dados[['Morbidade','Mortalidade','Inst. Social','Imp. Econômico','Saúde']].sum(axis=1)
dados = dados[['Nome','Morbidade','Mortalidade','Inst. Social','Imp. Econômico','Saúde', 'subtotal', 'Probabilidade']]

#Definindo a funcao para criar o fundo
def sigmoid(x, y, angle=-90):
    '''Define a sigmoid function aligned on the 50/50 line
       to be used as background for the scatter plot '''
    # Calculate the angle in radians
    angle_radians = np.radians(angle)

    # Rotate the coordinates by the specified angle
    x_rotated = x * np.cos(angle_radians) - y * np.sin(angle_radians)
    y_rotated = x * np.sin(angle_radians) + y * np.cos(angle_radians)

    # Apply the sigmoid function to the rotated coordinates
    return 1.0 / (20 + np.exp(0.1 * (+x_rotated - y_rotated)))

# Define limits
rangex = np.linspace(0, 30)
rangey = np.linspace(0, 30)

# Calculate sigmoid function on a meshgrid
x, y = np.meshgrid(rangex, rangey)
background = sigmoid(x, y)

# Create a trace containing the scatter plot
scatter = go.Scatter(x = dados['subtotal'], y = dados['Probabilidade'], mode = 'markers+text', 
                   marker= dict(size= 10, color = 'rgba(0, 0, 0, 0.8)',
                   line = dict(width = 1, color = 'rgb(255, 255, 255)')),
                   text = dados['Nome'], textposition='top center',
                   textfont=dict(size=25),
                   hovertemplate =
                      '<br><b>%{text}</b><br>'+
                      'Probabilidade: %{y}'+
                      '<br>Subtotal: %{x}<br>',
                    hoverinfo='text',
                     )

# Create a trace containing the background heatmap
heatmap = go.Heatmap(z=background, x=rangex, y=rangey, colorscale='RdYlGn',
                    showscale=False, hoverinfo='skip')

# Combine traces
data = [scatter, heatmap]

# Edit the layout
layout = dict(title = 'Diagrama THIRA',
              xaxis = dict(title = 'Subtotal'),
              yaxis = dict(title = 'Probabilidade'),
              #hovermode = 'closest',
              width=700,
              height=700
              )

# Define the figure
fig = dict(data=data, layout=layout)

diagrama = go.Figure(fig)

diagrama.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)

col1, col2, col3 = st.columns([1,5,2])
with col2:
  diagrama


col3.subheader('QR Code para o formulário')
col3.image('CDC_THIRA\qrcode_form.png', width=300)

   

dados_tabela = dados.copy()
dados_tabela = dados_tabela.set_index('Nome')
dados_tabela['Total'] = dados_tabela['Probabilidade']+dados_tabela['subtotal']

#Criando estilização do dataframe

col1, col2, col3 = st.columns([3,10,2])
with col2:
  st.dataframe(dados_tabela.style.background_gradient(cmap='RdYlGn_r',
                                                       subset=['Morbidade','Mortalidade','Inst. Social','Imp. Econômico','Saúde'],
                                                       vmin=0,
                                                       vmax=5) \
                 .background_gradient(cmap='RdYlGn_r', subset=['Probabilidade'], vmin=0, vmax=30)\
                  .background_gradient(cmap='RdYlGn_r', subset=['subtotal'], vmin=0, vmax=25),
                use_container_width=True,
                column_config={
                "Total": st.column_config.ProgressColumn(
                    "Total",
                    help="Soma de todos atributos",
                    format="%f",
                    min_value=0,
                    max_value=55,
                    width='medium'
                ),
                'subtotal': st.column_config.NumberColumn(
                   'Subtotal'
                ),
                'Imp. Econômico': st.column_config.NumberColumn(
                   'Imp. Econ.'
                )
                })

title_alignment= """
<style>
#thira {
  text-align: center
}


</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)