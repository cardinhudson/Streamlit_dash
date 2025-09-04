import streamlit as st
import pandas as pd



# Formatar a exibição do streamlit para o tamanho da tela grande
st.set_page_config(layout="wide")

# Conteúdo da nova página
st.write("Esta página contem o somatório de todas as contas do centro de lucro 02S, exceto as contas D_B!")

# Caminho do arquivo parquet
arquivo_parquet = r"KE5Z\KE5Z.parquet"

# Ler o arquivo parquet
df_principal = pd.read_parquet(arquivo_parquet)

# Filtros para o DataFrame
st.sidebar.title("Filtros")

# Filtro 1: USINA - Filtrar pela coluna 'USI' todas as opções inclusive as vazias ou na. Selecione a opção "Todos" para todas as USINAS
usina_opcoes = ["Todos"] + df_principal['USI'].fillna('Vazio').unique().tolist()
usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=["Todos"])




# Filtrar o DataFrame com base na USI
if "Todos" in usina_selecionada or not usina_selecionada:  # Se "Todos" for selecionado ou nada for selecionado
    df_filtrado = df_principal.copy()
else:  # Filtrar pelas USINAS selecionadas
    df_filtrado = df_principal[df_principal['USI'].isin(usina_selecionada)]
# Filtro 2: Período (dependente do filtro anterior)
periodo_opcoes = ["Todos"] + df_filtrado['Período'].dropna().unique().tolist()
periodo_selecionado = st.sidebar.selectbox("Selecione o Período:", periodo_opcoes)
# Filtrar o DataFrame com base no Período
if periodo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Período'] == periodo_selecionado]
# Filtro 3: Centro cst (dependente dos filtros anteriores)
centro_cst_opcoes = ["Todos"] + df_filtrado['Centro cst'].dropna().unique().tolist()
centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)
# Filtrar o DataFrame com base no Centro cst
if centro_cst_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Centro cst'] == centro_cst_selecionado]
# Filtro 4: Conta contabil (dependente dos filtros anteriores)
conta_contabil_opcoes = df_filtrado['Nº conta'].dropna().unique().tolist()
conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contabil:", conta_contabil_opcoes)
# Filtrar o DataFrame com base na Conta contabil
if conta_contabil_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Nº conta'].isin(conta_contabil_selecionadas)]







##################################################################################################

# Título da nova página
st.title("Total SAP KE5Z - Todas as USINAS")
# Criar uma tabela dinâmica (pivot table) para somar os valores por 'USI', incluindo campos desta coluna vazio ou NAN, a coluna por 'Período' e uma linha total
tabela_somada = df_filtrado.pivot_table(index='USI', columns='Período', values='Valor', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')
# Exibir a tabela somada na página com os numeros formatados como moeda brasileira
tabela_somada = tabela_somada.style.format("R$ {:,.2f}", decimal=",",thousands=".")
st.dataframe(tabela_somada)


##################################################################################################
# Título da nova página
st.title("Total SAP KE5Z - Todas as contas")
# Criar uma tabela dinâmica (pivot table) para somar os valores por 'Nº conta' incluindo a coluna por 'Período'
tabela_somada = df_filtrado.pivot_table(index='Nº conta', columns='Período', values='Valor', aggfunc='sum', fill_value=0, margins=True, margins_name='Total')

# Exibir a tabela somada na página com os numeros formatados como moeda brasileira
tabela_somada = tabela_somada.style.format("R$ {:,.2f}", decimal=",",thousands=".")
st.dataframe(tabela_somada)
# Exibir o número de linhas e colunas do DataFrame filtrado e a soma do valor total
st.sidebar.write(f"Número de linhas: {df_filtrado.shape[0]}")
st.sidebar.write(f"Número de colunas: {df_filtrado.shape[1]}")
st.sidebar.write(f"Soma do Valor total: R$ {df_filtrado['Valor'].sum():,.2f}")


