import pandas as pd
import streamlit as st
import plotly.express as px
from joblib import Memory

cachedir = './cache'
memory = Memory(cachedir, verbose=0)

@memory.cache
def carregar_dataframes():
    print("Lendo os CSVs novamente...")
    df_p = pd.read_csv('https://datapii3de.blob.core.windows.net/datapii/processos_seletivos_pii_none.csv', low_memory=False)
    df_a = pd.read_csv('https://datapii3de.blob.core.windows.net/datapii/alunos_pii_none.csv', low_memory=False)
    df_m = pd.read_csv('https://datapii3de.blob.core.windows.net/datapii/Matriculas_pii_none.csv', low_memory=False)
    return df_p, df_a, df_m

# Uso
df_p, df_a, df_m = carregar_dataframes()

# preenchendo valores faltantes da coluna 'Aluno' com 0 e convertendo para inteiro (necessário para o merge)
df_p['Aluno'] = df_p['Aluno'].fillna(0)
df_p['Aluno'] = df_p['Aluno'].astype('int64')

# unindo duas tabelas em um único dataframe. Thanks Julio.
df1 = df_p.rename(columns={"Id": "Id_aluno"})  # renomeia a coluna 'Id' para evitar conflito no merge
df2 = df_a
df_merge_difkey = pd.merge(df1, df2, left_on='Aluno', right_on='Id')  # faz o merge entre processo seletivo e alunos

# limpando colunas do dataframe que sejam totalmente vazias em todas as linhas
colunas_todas_vazias = df_merge_difkey.columns[df_merge_difkey.isna().all()].tolist()
df_merge_difkey.drop(columns=colunas_todas_vazias, inplace=True)

# retorna média por coluna com dado de 0 a 1 (sendo 1, completamente vazia)
faltantes = df_merge_difkey.isna().mean()

# limpando aquelas colunas que contêm mais de 80% de linhas com dado faltando
colunas_com_muita_falta = faltantes[faltantes > 0.8].index.tolist()
df_merge_difkey.drop(columns=colunas_com_muita_falta, inplace=True)

# limpa o dataframe de matrículas (df_m)
faltantes2 = df_m.isna().mean()
colunas_com_muita_falta1 = faltantes2[faltantes2 > 0.8].index.tolist()
df_m.drop(columns=colunas_com_muita_falta1, inplace=True)

# alocando os dataframes em novas variáveis para uso posterior
df3 = df_m
df4 = df_merge_difkey

# correspondendo nome de coluna entre os dois dataframes
df3.rename(columns={'Proprietário do Matrícula': 'Proprietário do Processo Seletivo'}, inplace=True)

# removido: comparação entre sets que era exibida na interface
_ = set(df3['Proprietário do Processo Seletivo']) - set(df4['Proprietário do Processo Seletivo'])

# removido: verificação final que também imprimia na interface
_ = set(df3['Proprietário do Processo Seletivo']) == set(df4['Proprietário do Processo Seletivo'])




st.set_page_config(page_title="Dashboard - Escola da Nuvem",
                    layout="wide",
                    page_icon=":cloud:",)

st.title("DASHBOARD - ESCOLA DA NUVEM :cloud:")
# --- GRÁFICO 1 --- 

# Criar coluna booleana indicando se está empregado
# armazena em um df quantas vezes cada estado aparece
alunos_por_estado = df4['Estado_y'].value_counts().reset_index()

# renomeando as colunas do df criado
alunos_por_estado.columns = ['Estado', 'Número de Alunos']

# cria o gráfico
fig_bar = px.bar(
    alunos_por_estado,
    x='Estado',
    y='Número de Alunos',
    title='Quantidade de Alunos por Estado'
)

# definimos a altura
fig_bar.update_layout(
    height=500
)

# exibe o gráfico no site
st.plotly_chart(fig_bar, use_container_width=False, key="graf_bar_estado")

# Criar coluna booleana sobre em quais linhas aparece a palavra empregado formatando-as como letras minúsculas
df4['Empregado'] = df4['Situação de Emprego Atual'].str.lower().str.contains('empregado')

# armazena em um df a proporção de empregados por estado agrupando os números por estado
proporcao_emprego_estado = df4.groupby('Estado_y')['Empregado'].mean().reset_index()

# renomeando as colunas do df criado
proporcao_emprego_estado.columns = ['Estado', 'Proporção de Empregados']

# Gerar o gráfico de barras by chatGPT
fig_empregabilidade = px.bar(
    proporcao_emprego_estado,
    x='Estado',
    y='Proporção de Empregados',
    title='Proporção de Alunos Empregados por Estado',
    text=proporcao_emprego_estado['Proporção de Empregados'].apply(lambda x: f"{x:.1%}"),
    labels={'Proporção de Empregados': 'Proporção'}
)

# Adiciona os valores como texto acima das barras
fig_empregabilidade.update_traces(textposition='outside')

# exibe o gráfico no site
st.plotly_chart(fig_empregabilidade, use_container_width=False, key="graf_empregabilidade_estado")

# KPIs
st.markdown("### Indicadores")

# Exemplo de indicador
df4['Empregado'] = df4['Situação de Emprego Atual'].str.lower().str.contains('empregado')
proporcao_empregados = df4['Empregado'].mean()

met1, met2, met3 = st.columns(3)

# Métrica: Proporção de alunos empregados
proporcao_empregados = df4['Empregado'].mean()
met1.metric("Proporção de Alunos Empregados", f"{proporcao_empregados:.1%}")

# Métrica: Total de alunos
met2.metric("Total de Alunos", f"{len(df4)}")

# Métrica: Total de Estados Representados
total_estados = df4['Estado_y'].nunique()
met3.metric("Estados Representados", total_estados)


