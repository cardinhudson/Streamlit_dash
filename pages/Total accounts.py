import streamlit as st
import pandas as pd

# Título da nova página
st.title("Nova Página do Dashboard")

# Formatar a exibição do streamlit para o tamanho da tela grande
st.set_page_config(layout="wide")

# Conteúdo da nova página
st.write("Esta página contem o somatório de todas as contas do centro de lucro 02S, exceto as contas D_B!")

# Caminho do arquivo parquet
arquivo_parquet = r"C:\user\U235107\GitHub\streamlit_dash_deploy\KE5Z\KE5Z.parquet"

# Ler o arquivo parquet
df_total = pd.read_parquet(arquivo_parquet)

# Criar uma tabela dinâmica (pivot table) para somar os valores por 'Nº conta' incluindo a coluna por 'Período'
tabela_somada = pd.pivot_table(df_total, values='Valor', index=['Nº conta'], columns=['Período'], aggfunc='sum', fill_value=0, margins=True, margins_name='Total Geral')
# Exibir a tabela somada na página com os numeros formatados como moeda brasileira
tabela_somada = tabela_somada.style.format("R$ {:,.2f}", decimal=",", thousands=".")
st.dataframe(tabela_somada)