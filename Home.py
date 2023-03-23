#======================================================= ### CABEÇALHO ### ===================================================================#
#___________________________________________#_________________________________________________#
# Bibliotecas

# IMPORTANDO LIVROS/BIBLIOTECAS
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
import folium
import numpy as np
import streamlit as st
from PIL import Image
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
#___________________________________________#_________________________________________________#
# Funções

# Funções responsáveis por limpeza dos dados
def clean_code(df1):
    # Remover espaço do inicio e fim dos dados das colunas string
    df1.loc[:,'Restaurant Name'] = df.loc[:,'Restaurant Name'].str.strip()
    df1.loc[:,'City'] = df.loc[:,'City'].str.strip()
    df1.loc[:,'Address'] = df.loc[:,'Address'].str.strip()
    df1.loc[:,'Locality'] = df.loc[:,'Locality'].str.strip()
    df1.loc[:,'Locality Verbose'] = df.loc[:,'Locality Verbose'].str.strip()
    df1.loc[:,'Cuisines'] = df.loc[:,'Cuisines'].str.strip()
    df1.loc[:,'Currency'] = df.loc[:,'Currency'].str.strip()
    df1.loc[:,'Rating color'] = df.loc[:,'Rating color'].str.strip()
    df1.loc[:,'Rating text'] = df.loc[:,'Rating text'].str.strip()

    # Converter os tipos de dados das colunas:
    df1['Restaurant ID'] = df1['Restaurant ID'].astype(int)
    df1['Restaurant Name'] = df1['Restaurant Name'].astype(str)
    df1['Country Code'] = df1['Country Code'].astype(int)
    df1['City'] = df1['City'].astype(str)
    df1['Address'] = df1['Address'].astype(str)
    df1['Locality'] = df1['Locality'].astype(str)
    df1['Locality Verbose'] = df1['Locality Verbose'].astype(str)
    df1['Longitude'] = df1['Longitude'].astype(int)
    df1['Latitude'] = df1['Latitude'].astype(int)
    df1['Cuisines'] = df1['Cuisines'].astype(str)
    df1['Average Cost for two'] = df1['Average Cost for two'].astype(float)
    df1['Currency'] = df1['Currency'].astype(str)
    df1['Has Table booking'] = df1['Has Table booking'].astype(int)
    df1['Has Online delivery'] = df1['Has Online delivery'].astype(int)
    df1['Is delivering now'] = df1['Is delivering now'].astype(int)
    df1['Switch to order menu'] = df1['Switch to order menu'].astype(int)
    df1['Price range'] = df1['Price range'].astype(int)
    df1['Aggregate rating'] = df1['Aggregate rating'].astype(float)
    df1['Rating color'] = df1['Rating color'].astype(str)
    df1['Rating text'] = df1['Rating text'].astype(str)
    df1['Votes'] = df1['Votes'].astype(int)

    # Preenchimento do nome dos países
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    }

    df1["Country Name"] = df["Country Code"].map(COUNTRIES)

    # Criação do Tipo de Categoria de Comida
    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"

    # Criação do nome das Cores
    COLORS = {"3F7E00": "darkgreen", "5BA829": "green", "9ACD32": "lightgreen", "CDD614": "orange", "FFBA00": "red", "CBCBC8": "darkred", "FF7800": "darkred",}
    def color_name(color_code):
        return COLORS[color_code]

    #Renomear as colunas do DataFrame
    def rename_columns(df1):
        df1 = df1.copy()
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df

    # Categorizando todos os restaurantes somente por um tipo de culinária
    df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    return df1
#___________________________________________#_________________________________________________#
# Importando Dataframe

# Realizando importação do Dataframe + utilização de Função para limpeza dos dados

# Lendo Dataframe
base = pd.read_csv('zomato.csv')

#r"C:\Users\usuario\Desktop\PEN\1. Pessoal\c. Estudo\6. DS\0. Cursos e Capacitações\CDS\0. Ciclo Inicialização\3. Análise de Dados em Python - Da Lógica a Análise\i. Projeto do Aluno\zomato.csv"

# Fazendo uma cópia do DataFrame Lido
df = base.copy()

df1 = clean_code(df)
#___________________________________________#_________________________________________________#

#===================================================== ### ANÁLISE DOS DADOS ### ================================================================#
#___________________________________________#_________________________________________________#
# 1.0 Geral
## 1.1
st.set_page_config(page_title = 'Fome Zero')

#image_path = r'C:\Users\usuario\Documents\projetos\1_CDS\logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width = 120)
st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Powered By Luiz Zamian')

st.write(" ## FOME ZERO! O Melhor lugar para encontrar seu mais novo restaurante favorito!")

st.markdown("""---""")

with st.container():
        st.title('Temos as seguintes marcas dentro da nossa plataforma:')
        col1, col2, col3, col4, col5 = st.columns(5, gap='large')
        with col1:
            quest_01 = df1.loc[:, 'Restaurant ID'].nunique()
            col1.metric('Restaurantes Cadastrados', quest_01)
        with col2:
            quest_02 = df1.loc[:, 'Country Code'].nunique()
            col2.metric('Países Cadastrados', quest_02)
        with col3:
            quest_03 = df1.loc[:, 'City'].nunique()
            col3.metric('Cidades Cadastradas', quest_03)
        with col4:
            quest_04 = df1.loc[:, 'Rating text'].count()
            col4.metric('Avaliações', quest_04)
        with col5:
            quest_05 = df1.loc[:, 'Rating text'].nunique()
            col5.metric('Tipos de Culinária', quest_05)

st.markdown("""---""")

# Seleciona as coordenadas do centro do mapa
lat_center = df1['Latitude'].mean()
lon_center = df1['Longitude'].mean()

# Cria o mapa centrado em uma coordenada específica
mapa = folium.Map(location=[lat_center, lon_center], zoom_start=2)

# Cria o objeto MarkerCluster
marker_cluster = MarkerCluster()

# Adiciona marcadores ao MarkerCluster
for index, row in df1.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']]).add_to(marker_cluster)

# Adiciona o MarkerCluster ao mapa
marker_cluster.add_to(mapa)

# Mostra o mapa
st.markdown("### Veja em quais lugares do mundo contam com nossa cobertura:")
folium_static(mapa, width = 1024, height = 600)

#___________________________________________#_________________________________________________#

