import streamlit as st
import pandas as pd
from auth import verificar_autenticacao, exibir_header_usuario

# Configuração da página
st.set_page_config(
    page_title="Outside TC - Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação - OBRIGATÓRIO no início de cada página
verificar_autenticacao()

# Header com informações do usuário
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Outside TC - Total Accounts Page")
    st.subheader("Visualização de dados fora do perímetro TC")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Conteúdo da nova página
st.write("Esta página contém dados de contas fora do perímetro TC.")