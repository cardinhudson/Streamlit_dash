# %%
import streamlit as st
import pandas as pd
import os
import altair as alt

# Caminho do arquivo parquet
arquivo_parquet = os.path.join("KE5Z", "KE5Z.parquet")

# Ler o arquivo parquet
df_total = pd.read_parquet(arquivo_parquet)

# Exibir as primeiras linhas do DataFrame para verificar os dados
print(df_total.head())


# filtrar o df_total com a coluna 'USI" que não seja 'Others' e que não seja nula
df_total = df_total[df_total['USI'].notna() & (df_total['USI'] != 'Others')]





# %%
# Título do dashboard
st.title("Dashboard - Visualização de Dados TC - KE5Z")

# Subtítulo
st.subheader("Somente os dados com as contas do Perímetro TC")


# Formatar a exibição do streamlit para o tamanho da tela grande
st.set_page_config(layout="wide")

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
# Incluir um gráfico de barras que mostre a coluna de 'valor' totais por 'periodo' do df_total
# Agrupar os dados por 'Período' e calcular a soma dos valores
df_grafico = df_filtrado.groupby('Período')['Valor'].sum().reset_index()

#Criar um grafico de barras simples com o eixo y sendo o valor e o x sendo o período
# no eixo x mostrar somente valores existentes no df_grafico
grafico_barras = alt.Chart(df_grafico).mark_bar().encode(
    x=alt.X('Período:N', title='Período', sort=None),
    y=alt.Y('Valor:Q', title='Soma do Valor'),
    tooltip=[alt.Tooltip('Período:N', title='Período'), alt.Tooltip('Valor:Q', title='Soma do Valor', format=',.2f')]
).properties(
    title='Gráfico de Barras - Soma do Valor por Período',
    width=800,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16,
    anchor='start',
    color='black'
)




# Exibir o gráfico no Streamlit
st.altair_chart(grafico_barras, use_container_width=True)

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

print('Lauro é muito lindo')