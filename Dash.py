# %%
import streamlit as st
import pandas as pd
import os
import altair as alt
from auth import verificar_autenticacao, exibir_header_usuario

# Configuração da página
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação - OBRIGATÓRIO no início de cada página
verificar_autenticacao()

# Caminho do arquivo parquet
arquivo_parquet = os.path.join("KE5Z", "KE5Z.parquet")

# Ler o arquivo parquet
df_total = pd.read_parquet(arquivo_parquet)

# Exibir as primeiras linhas do DataFrame para verificar os dados
print(df_total.head())

# filtrar o df_total com a coluna 'USI" que não seja 'Others' e que não seja nula
df_total = df_total[df_total['USI'].notna() & (df_total['USI'] != 'Others')]

# Header com informações do usuário e botão de logout
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Dashboard - Visualização de Dados TC - KE5Z")
    st.subheader("Somente os dados com as contas do Perímetro TC")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Filtros para o DataFrame
st.sidebar.title("Filtros")

# Filtro 1: USINA - Filtrar somente a coluna 'USI' que não são 'Others' e trazer todas as opções inclusive as vazias ou na. Selecione a opção "Todos" para todas as USINAS
usina_opcoes = ["Todos"] + df_total['USI'].dropna().unique().tolist()
usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=["Todos"])

# Filtrar o DataFrame com base na USI
if "Todos" in usina_selecionada or not usina_selecionada:  # Se "Todos" for selecionado ou nada for selecionado
    df_filtrado = df_total.copy()
else:  # Filtrar pelas USINAS selecionadas
    df_filtrado = df_total[df_total['USI'].isin(usina_selecionada)]

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

# Exibir o número de linhas e colunas do DataFrame filtrado e a soma do valor total
st.sidebar.write(f"Número de linhas: {df_filtrado.shape[0]}")
st.sidebar.write(f"Número de colunas: {df_filtrado.shape[1]}")
st.sidebar.write(f"Soma do Valor total: R$ {df_filtrado['Valor'].sum():,.2f}")



#%%

# Criar um gráfico de barras para a soma dos valores por 'Período' com uma única cor
grafico_barras = alt.Chart(df_filtrado).mark_bar(color='steelblue').encode(  # Define uma cor fixa para as barras
    x=alt.X('Período:N', title='Período'),
    y=alt.Y('sum(Valor):Q', title='Soma do Valor'),
    tooltip=['Período:N', 'sum(Valor):Q']  # Tooltip para exibir informações
).properties(
    title='Soma do Valor por Período'
)

# Adicionar os rótulos com os valores nas barras
rotulos = grafico_barras.mark_text(
    align='center',
    baseline='middle',
    dy=-10,  # Ajuste vertical para posicionar o texto acima das barras
    color='white',
    fontSize=12
).encode(
    text=alt.Text('sum(Valor):Q', format=',.2f')  # Formatar os valores com duas casas decimais
)

# Combinar o gráfico de barras com os rótulos
grafico_completo = grafico_barras + rotulos

# Exibir o gráfico no Streamlit
st.altair_chart(grafico_completo, use_container_width=True)

# %%
# Exibir 'tabela filtrada com linhas sendo a USI e as colunas sendo o 'Período' e os valores sendo a soma do 'Valor' e incluir valor do total na última linha e coluna
df_pivot = df_filtrado.pivot_table(index='USI', columns='Período', values='Valor', aggfunc='sum', margins=True, margins_name='Total', fill_value=0)
st.subheader("Tabela Dinâmica - Soma do Valor por USI e Período")
st.dataframe(df_pivot.style.format('R$ {:,.2f}').applymap(lambda x: 'color: red;' if x < 0 else 'color: green;' if x > 0 else '', subset=pd.IndexSlice[:, :]))  # Formatar como moeda e vermelho negativo e azul positivo

# Exibir o DataFrame filtrado
st.subheader("Tabela Filtrada")
st.dataframe(df_filtrado)

# Botão para exportar os dados filtrados para Excel
caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
if st.button("Exportar Tabela Filtrada para Excel"):
    caminho_saida_excel_filtrado = os.path.join(caminho_downloads, 'KE5Z_tabela_filtrada.xlsx')
    df_filtrado.to_excel(caminho_saida_excel_filtrado, index=False)
    st.success(f"Tabela filtrada exportada com sucesso para {caminho_saida_excel_filtrado}")

# Criar uma tabela com a soma dos valores por Type 05, Type 06 e Type 07
soma_por_type = df_filtrado.groupby(['Type 05', 'Type 06', 'Type 07'])['Valor'].sum().reset_index()

# Adicionar uma linha com a soma total na última linha
soma_total = pd.DataFrame({
    'Type 05': ['Total'],
    'Type 06': [''],
    'Type 07': [''],
    'Valor': [soma_por_type['Valor'].sum()]
})
soma_por_type = pd.concat([soma_por_type, soma_total], ignore_index=True)

# Exibir a tabela com a soma total e formatar a coluna de valorres como moeda e vermelho negativo e verde positivo
st.subheader("Soma dos Valores por Type 05, Type 06 e Type 07 (com Total)")
st.dataframe(soma_por_type.style.format({'Valor': 'R$ {:,.2f}'}).applymap(lambda x: 'color: red;' if isinstance(x, (int, float)) and x < 0 else 'color: green;' if isinstance(x, (int, float)) and x > 0 else '', subset=['Valor']))

# Botão para exportar a soma dos valores por Type 05, Type 06 e Type 07 para Excel
caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

if st.button("Exportar Soma por Type para Excel"):
    caminho_saida_excel_soma = os.path.join(caminho_downloads, 'KE5Z_soma_por_type.xlsx')
    soma_por_type.to_excel(caminho_saida_excel_soma, index=False)
    st.success(f"Soma por Type exportada com sucesso para {caminho_saida_excel_soma}")


# %%
# Criar um gráfico de barras para a soma dos valores por 'Type 05', 'Type 06' e 'Type 07'
# classificado em ordem decrescente
grafico_barras = alt.Chart(df_filtrado).mark_bar(color='steelblue').encode(  # Define uma cor fixa para as barras
    x=alt.X('Type 05:N', title='Type 05', sort=alt.SortField(field='sum(Valor):Q', order='descending')),
    y=alt.Y('sum(Valor):Q', title='Soma do Valor'),
    tooltip=['Type 05:N', 'sum(Valor):Q']  # Tooltip para exibir informações
).properties(
    title='Soma do Valor por Type 05'
)

# Adicionar os rótulos com os valores nas barras
rotulos = grafico_barras.mark_text(
    align='center',
    baseline='middle',
    dy=-10,  # Ajuste vertical para posicionar o texto acima das barras
    color='white',
    fontSize=12
).encode(
    text=alt.Text('sum(Valor):Q', format=',.2f')  # Formatar os valores com duas casas decimais
)

# Combinar o gráfico de barras com os rótulos
grafico_completo = grafico_barras + rotulos

# Exibir o gráfico no Streamlit
st.altair_chart(grafico_completo, use_container_width=True)

# Criar dados agregados para Type 06 ordenados por valor decrescente
df_type06_agg = df_filtrado.groupby('Type 06')['Valor'].sum().reset_index()
df_type06_agg = df_type06_agg.sort_values('Valor', ascending=False)

# Gráfico de barras para a soma dos valores por 'Type 06' em ordem decrescente
grafico_barras = alt.Chart(df_type06_agg).mark_bar(color='steelblue').encode(  # Define uma cor fixa para as barras
    x=alt.X('Type 06:N', title='Type 06', sort=None),  # Sem ordenação automática, dados já ordenados
    y=alt.Y('Valor:Q', title='Soma do Valor'),
    tooltip=['Type 06:N', 'Valor:Q']  # Tooltip para exibir informações
).properties(
    title='Soma do Valor por Type 06'
)

# Adicionar os rótulos com os valores nas barras
rotulos = grafico_barras.mark_text(
    align='center',
    baseline='middle',
    dy=-10,  # Ajuste vertical para posicionar o texto acima das barras
    color='white',
    fontSize=12
).encode(
    text=alt.Text('Valor:Q', format=',.2f')  # Formatar os valores com duas casas decimais
)

# Combinar o gráfico de barras com os rótulos
grafico_completo = grafico_barras + rotulos

# Exibir o gráfico no Streamlit
st.altair_chart(grafico_completo, use_container_width=True)

