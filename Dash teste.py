# %%
import streamlit as st
import pandas as pd
import os
import altair as alt
import hashlib
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar usuários do arquivo JSON
def carregar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

# Função para criar hash da senha
def criar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para verificar credenciais
def verificar_login(username, senha):
    usuarios = carregar_usuarios()
    if username in usuarios:
        senha_hash = criar_hash_senha(senha)
        return senha_hash == usuarios[username]['senha']
    return False

# Função para verificar se o usuário está logado
def verificar_sessao():
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = False
    if 'usuario_nome' not in st.session_state:
        st.session_state.usuario_nome = None
    return st.session_state.usuario_logado

# Função para fazer logout
def fazer_logout():
    st.session_state.usuario_logado = False
    st.session_state.usuario_nome = None
    st.rerun()

# Função para tela de login
def tela_login():
    st.title("🔐 Login - Dashboard KE5Z")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Acesso ao Sistema")
        username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
        senha = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        
        if submitted:
            if verificar_login(username, senha):
                st.session_state.usuario_logado = True
                st.session_state.usuario_nome = username
                st.success(f"Bem-vindo, {username}!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos!")
    
    # Seção para administrador adicionar usuários
    st.markdown("---")
    st.subheader("👨‍💼 Área Administrativa")
    
    with st.expander("Adicionar Novo Usuário"):
        with st.form("add_user_form"):
            st.write("**Cadastrar novo usuário:**")
            novo_usuario = st.text_input("Usuário:", key="novo_usuario")
            nova_senha = st.text_input("Senha:", type="password", key="nova_senha")
            confirmar_senha = st.text_input("Confirmar Senha:", type="password", key="confirmar_senha")
            
            if st.form_submit_button("Cadastrar Usuário"):
                if nova_senha == confirmar_senha and novo_usuario and nova_senha:
                    usuarios = carregar_usuarios()
                    if novo_usuario not in usuarios:
                        usuarios[novo_usuario] = {
                            'senha': criar_hash_senha(nova_senha),
                            'data_criacao': datetime.now().isoformat()
                        }
                        salvar_usuarios(usuarios)
                        st.success(f"✅ Usuário '{novo_usuario}' cadastrado com sucesso!")
                    else:
                        st.error("❌ Usuário já existe!")
                else:
                    st.error("❌ Preencha todos os campos e confirme a senha corretamente!")

# Função principal do dashboard
def dashboard_principal():
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
    with col3:
        st.write(f"👤 Usuário: **{st.session_state.usuario_nome}**")
        if st.button("🚪 Logout", type="secondary"):
            fazer_logout()

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

# Função para criar usuário administrador inicial
def criar_admin_inicial():
    usuarios = carregar_usuarios()
    if not usuarios:  # Se não há usuários, criar admin padrão
        usuarios['admin'] = {
            'senha': criar_hash_senha('admin123'),
            'data_criacao': datetime.now().isoformat()
        }
        salvar_usuarios(usuarios)
        st.info("👤 Usuário administrador criado: **admin** | Senha: **admin123**")
        st.warning("⚠️ **IMPORTANTE**: Altere a senha padrão após o primeiro login!")

# Programa principal
def main():
    # Criar usuário admin inicial se necessário
    criar_admin_inicial()
    
    # Verificar se o usuário está logado
    if not verificar_sessao():
        tela_login()
    else:
        dashboard_principal()

if __name__ == "__main__":
    main()