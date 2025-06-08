import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('MS_Financial Sample.csv', sep=';')

st.set_page_config(page_title="Dashboard - Prova do Julio",
                    layout="wide",
                    page_icon=":globe_with_meridians::",)

st.title("DASHBOARD - Prova do Julião :globe_with_meridians:")

grafico = ['Country', 'Sales']

fig_bar = px.bar(df, x='Country', y='Sales', title='Vendas por Pais')

# definimos a altura
fig_bar.update_layout(
    height=500
)

# exibe o gráfico no site
st.plotly_chart(fig_bar, use_container_width=False, key="graf_barra")

#
