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

# Fazendo uma cópia do DataFrame Lido
df = base.copy()

df1 = clean_code(df)
#___________________________________________#_________________________________________________#

#===================================================== ### ANÁLISE DOS DADOS ### ================================================================#
#___________________________________________#_________________________________________________#
# 2.0 Countries
## 2.1

#image_path = r'C:\Users\usuario\Documents\projetos\1_CDS\logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width = 120)
st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.sidebar.markdown("""---""")

countries_options = st.sidebar.multiselect(
    'Escolha os Países',
    ['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'Singapure', 'United Arab Emirates', 'India','Indonesia', 'New Zeland','England','Qatar', 'South Africa','Sri Lanka', 'Turkey'],
    default = ['Philippines', 'Brazil', 'Australia', 'United States of America','Canada', 'Singapure', 'United Arab Emirates', 'India','Indonesia', 'New Zeland','England','Qatar', 'South Africa','Sri Lanka', 'Turkey'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Powered By Luiz Zamian')

# Filtro de Transito
linhas_selecionadas = df1['Country Name'].isin(countries_options)
df1 = df1.loc[linhas_selecionadas, :]


st.write(" ## Visão Cidades")

st.markdown("""---""")

with st.container():
    st.markdown('## Top 10 Cidades com mais Restaurantes')
    df_aux = df1.loc[:, ['Restaurant ID', 'City']].groupby('City').count().sort_values('Restaurant ID', ascending=False).reset_index().head(10)#.iloc[0, 0]
    fig = px.bar(df_aux, x='City', y='Restaurant ID')
    st.plotly_chart(fig, use_container_width = True)
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Top Quantidade Restaurantes com melhores médias de avaliações por Cidades')
        df_mean_2 = df1.groupby('City')['Votes'].mean()
        big_4 = df_mean_2[df_mean_2 > 4]
        df_aux_2 = df1.loc[df1['City'].isin(big_4.index), 'City'].value_counts().reset_index().head(7)
        df_aux_2 = df_aux_2.rename(columns={'City': 'Restaurants', 'index': 'City'})
        fig = px.bar(df_aux_2, x='City', y='Restaurants')
        st.plotly_chart(fig, use_container_width = True)
    with col2:
        st.markdown('## Top Quantidade Restaurantes com piores médias de avaliações por Cidades')
        df_mean_3 = df1.groupby('City')['Votes'].mean()
        smaller_4 = df_mean_3[df_mean_3 > 2.5]
        df_aux_3 = df1.loc[df1['City'].isin(smaller_4.index), 'City'].value_counts().reset_index().tail(7)
        df_aux_3 = df_aux_3.rename(columns={'City': 'Restaurants', 'index': 'City'})
        fig = px.bar(df_aux_3, x='City', y='Restaurants')
        st.plotly_chart(fig, use_container_width = True)

with st.container():
    st.markdown('## Top 10 Cidades com mais Restaurantes de tipos de Culinária distinto')
    df_aux = df1.loc[:, ['City', 'Country Name']].groupby('Country Name').count().sort_values('City', ascending=False).reset_index().head(5)#.iloc[0, 0]
    fig = px.bar(df_aux, x='Country Name', y='City')
    st.plotly_chart(fig, use_container_width = True)