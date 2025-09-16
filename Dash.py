# %%
import streamlit as st
import pandas as pd
import os
import altair as alt
import subprocess
import sys
import plotly.graph_objects as go
from auth import (verificar_autenticacao, exibir_header_usuario,
                  eh_administrador, verificar_status_aprovado,
                  carregar_usuarios, salvar_usuarios, criar_hash_senha)
from datetime import datetime


def executar_extracao():
    """Executa o script de extração e retorna o status"""
    try:
        # Verificar se o arquivo de extração existe
        arquivo_extracao = "Extração.py"
        if not os.path.exists(arquivo_extracao):
            return False, f"Arquivo '{arquivo_extracao}' não encontrado!"
        
        # Executar o script de extração
        result = subprocess.run([sys.executable, arquivo_extracao],
                                capture_output=True, text=True,
                                cwd=os.getcwd(),
                                timeout=300)  # Timeout de 5 minutos
        
        if result.returncode == 0:
            return True, "SUCESSO: Extração executada com sucesso!"
        else:
            error_msg = result.stderr if result.stderr else "Erro desconhecido"
            return False, f"ERRO: Erro na extração: {error_msg}"
    except subprocess.TimeoutExpired:
        return False, "ERRO: Timeout - A extração demorou mais de 5 minutos"
    except FileNotFoundError:
        return False, "ERRO: Python não encontrado no sistema"
    except Exception as e:
        return False, f"ERRO: Erro ao executar extração: {str(e)}"


# Configuração da página
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação - OBRIGATÓRIO no início de cada página
verificar_autenticacao()

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação. "
               "Aguarde o administrador aprovar seu acesso.")
    st.info("📧 Você receberá uma notificação quando sua conta for "
            "aprovada.")
    st.stop()

# Caminho do arquivo parquet
arquivo_parquet = os.path.join("KE5Z", "KE5Z.parquet")

# Ler o arquivo parquet
df_total = pd.read_parquet(arquivo_parquet)

# Exibir as primeiras linhas do DataFrame para verificar os dados
print(df_total.head())

# Filtrar o df_total com a coluna 'USI' que não seja 'Others' e que não seja nula
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

# Seção administrativa (apenas para admin)
if eh_administrador():
    st.sidebar.markdown("---")
    st.sidebar.subheader("👑 Área Administrativa")

    # Inicializar usuários no session_state se não existir
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = carregar_usuarios()

    usuarios = st.session_state.usuarios

    # Aviso sobre armazenamento temporário no Streamlit Cloud
    st.sidebar.info(
        "ℹ️ **Nota:** No Streamlit Cloud, as mudanças de usuários são "
        "temporárias e serão perdidas ao recarregar a página."
    )

    # Status de salvamento
    try:
        # Tentar salvar para verificar se funciona
        salvar_usuarios(usuarios)
        st.sidebar.success("💾 Salvamento: ✅ Funcionando")
    except Exception as e:
        st.sidebar.warning("💾 Salvamento: ❌ Não disponível")
        st.sidebar.caption(f"Erro: {str(e)[:50]}...")

    # Status atual dos usuários
    total_usuarios = len(usuarios)
    usuarios_aprovados = len([u for u in usuarios.values()
                              if u.get('status') == 'aprovado'])
    usuarios_pendentes = len([u for u in usuarios.values()
                              if u.get('status') == 'pendente'])

    st.sidebar.metric("👥 Total", total_usuarios)
    st.sidebar.metric("✅ Aprovados", usuarios_aprovados)
    st.sidebar.metric("⏳ Pendentes", usuarios_pendentes)

    with st.sidebar.expander("Gerenciar Usuários"):
        st.write("**Adicionar novo usuário:**")

        with st.form("admin_add_user_form"):
            novo_usuario = st.text_input("Usuário:", key="admin_novo_usuario")
            nova_senha = st.text_input("Senha:", type="password", key="admin_nova_senha")
            confirmar_senha = st.text_input("Confirmar Senha:", 
                                             type="password",
                                             key="admin_confirmar_senha")

            if st.form_submit_button("Cadastrar Usuário", use_container_width=True):
                if nova_senha == confirmar_senha and novo_usuario and nova_senha:
                    try:
                        if novo_usuario not in usuarios:
                            # Adicionar usuário ao session_state
                            usuarios[novo_usuario] = {
                                'senha': criar_hash_senha(nova_senha),
                                'data_criacao': datetime.now().isoformat(),
                                'status': 'pendente'
                            }

                            # Atualizar session_state
                            st.session_state.usuarios = usuarios

                            # Salvar dados
                            try:
                                salvar_usuarios(usuarios)
                                st.success("💾 Dados salvos com sucesso!")
                            except Exception as save_error:
                                st.warning(f"⚠️ Erro ao salvar: {str(save_error)}")

                            st.success(f"✅ Usuário '{novo_usuario}' cadastrado "
                                       f"com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Usuário já existe!")
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar usuário: {str(e)}")
                else:
                        st.error("❌ Preencha todos os campos e confirme a "
                                  "senha corretamente!")

    # Seção de atualização de dados
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Atualizar Dados")
    
    # Aviso sobre ambiente local
    st.sidebar.info("💻 **Atenção:** A extração de dados só funciona em "
                    "ambiente local (não funciona no Streamlit Cloud).")
    
    # Extração local
    if st.sidebar.button("📊 Executar Extração Local", 
                         use_container_width=True):
        with st.spinner("Executando extração de dados..."):
            sucesso, mensagem = executar_extracao()
            
            if sucesso:
                st.sidebar.success(mensagem)
                st.sidebar.info("🔄 Recarregue a página para ver os dados "
                                "atualizados.")
            else:
                st.sidebar.error(mensagem)

    # Gerenciar usuários pendentes (fora do expander)
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 Usuários Pendentes")

    usuarios_pendentes = {k: v for k, v in usuarios.items()
                          if v.get('status') == 'pendente'}

    if usuarios_pendentes:
        for usuario, dados in usuarios_pendentes.items():
            with st.sidebar.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"👤 **{usuario}**")
                    if dados.get('email'):
                        st.write(f"📧 {dados['email']}")
                    st.write(f"📅 {dados.get('data_criacao', 'N/A')[:10]}")

                with col2:
                    if st.button("✅", key=f"aprovar_{usuario}",
                                help="Aprovar usuário"):
                        usuarios[usuario]['status'] = 'aprovado'
                        usuarios[usuario]['aprovado_em'] = (
                            datetime.now().isoformat())
                        st.session_state.usuarios = usuarios

                        # Salvar dados
                        try:
                            salvar_usuarios(usuarios)
                            st.success("💾 Dados salvos com sucesso!")
                        except Exception as save_error:
                            st.warning(f"⚠️ Erro ao salvar: {str(save_error)}")

                        st.success(f"✅ Usuário '{usuario}' aprovado!")
                        st.rerun()

                with col3:
                    if st.button("❌", key=f"rejeitar_{usuario}",
                                help="Rejeitar usuário"):
                        del usuarios[usuario]
                        st.session_state.usuarios = usuarios

                        # Salvar dados
                        try:
                            salvar_usuarios(usuarios)
                            st.success("💾 Dados salvos com sucesso!")
                        except Exception as save_error:
                            st.warning(f"⚠️ Erro ao salvar: {str(save_error)}")

                        st.success(f"❌ Usuário '{usuario}' removido!")
                        st.rerun()

                st.sidebar.markdown("---")
    else:
        st.sidebar.info("✅ Nenhum usuário pendente de aprovação.")

    # Listar todos os usuários (fora do expander)
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Todos os Usuários")

    for usuario, dados in usuarios.items():
        with st.sidebar.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                if usuario == 'admin':
                    st.write("👑 **admin** (Administrador)")
                else:
                    status_icon = ("✅" if dados.get('status') == 'aprovado' 
                                   else "⏳")
                    status_text = ("Aprovado" if dados.get('status') == 'aprovado' 
                                   else "Pendente")
                    st.write(f"{status_icon} **{usuario}** - {status_text}")
                    if dados.get('email'):
                        st.write(f"📧 {dados['email']}")

            with col2:
                if usuario != 'admin':
                    if st.button("🗑️", key=f"excluir_{usuario}",
                                help="Excluir usuário"):
                        del usuarios[usuario]
                        st.session_state.usuarios = usuarios

                        # Salvar dados
                        try:
                            salvar_usuarios(usuarios)
                            st.success("💾 Dados salvos com sucesso!")
                        except Exception as save_error:
                            st.warning(f"⚠️ Erro ao salvar: {str(save_error)}")

                        st.success(f"✅ Usuário '{usuario}' excluído!")
                        st.rerun()
else:
    st.sidebar.markdown("---")
    st.sidebar.info("🔒 Apenas o administrador pode gerenciar usuários.")

# Seção de alterar senha removida do dashboard
# Agora está disponível na tela de login

# %%

# Criar um gráfico de barras para a soma dos valores por 'Período' com uma única cor
grafico_barras = alt.Chart(df_filtrado).mark_bar(color='steelblue').encode(
    x=alt.X('Período:N', title='Período'),
    y=alt.Y('sum(Valor):Q', title='Soma do Valor'),
    tooltip=['Período:N', 'sum(Valor):Q']
).properties(
    title='Soma do Valor por Período'
)

# Adicionar os rótulos com os valores nas barras
rotulos = grafico_barras.mark_text(
    align='center',
    baseline='middle',
    dy=-10,  # Ajuste vertical
    color='white',
    fontSize=12
).encode(
    text=alt.Text('sum(Valor):Q', format=',.2f')
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

# Função para exportar uma única tabela para Excel
def exportar_excel(df, nome_arquivo):
    """Exporta DataFrame para Excel e retorna bytes para download"""
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    output.seek(0)
    return output.getvalue()


# Exibir o DataFrame filtrado
st.subheader("Tabela Filtrada")
st.dataframe(df_filtrado)

# Botão para download da tabela filtrada
if st.button("📥 Baixar Tabela Filtrada (Excel)", use_container_width=True):
    with st.spinner("Gerando arquivo..."):
        excel_data_filtrada = exportar_excel(df_filtrado, 'KE5Z_tabela_filtrada.xlsx')
        
        # Forçar download usando JavaScript
        import base64
        b64 = base64.b64encode(excel_data_filtrada).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="KE5Z_tabela_filtrada.xlsx">💾 Clique aqui para baixar</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ Arquivo gerado! Clique no link acima para baixar.")


# Criar uma tabela com a soma dos valores por Type 05, Type 06 e Type 07
soma_por_type = (df_filtrado.groupby(['Type 05', 'Type 06', 'Type 07'])['Valor']
                 .sum().reset_index())

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
# Formatar dataframe com cores
def colorir_valores(val):
    if isinstance(val, (int, float)) and val < 0:
        return 'color: red;'
    elif isinstance(val, (int, float)) and val > 0:
        return 'color: green;' 
    return '' 


styled_df = soma_por_type.style.format({'Valor': 'R$ {:,.2f}'}).applymap(
    colorir_valores, subset=['Valor'])
st.dataframe(styled_df)

# Botão para download da tabela de soma
if st.button("📥 Baixar Soma por Type (Excel)", use_container_width=True):
    with st.spinner("Gerando arquivo..."):
        excel_data_soma = exportar_excel(soma_por_type, 'KE5Z_soma_por_type.xlsx')
        
        # Forçar download usando JavaScriptrro
        import base64
        b64 = base64.b64encode(excel_data_soma).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="KE5Z_soma_por_type.xlsx">💾 Clique aqui para baixar</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ Arquivo gerado! Clique no link acima para baixar.")

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
    dy=-10,  # Ajuste vertical
    color='white',
    fontSize=12
).encode(
    text=alt.Text('sum(Valor):Q', format=',.2f')
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
    dy=-10,  # Ajuste vertical
    color='white',
    fontSize=12
).encode(
    text=alt.Text('Valor:Q', format=',.2f')  # Formatar os valores com duas casas decimais
)

# Combinar o gráfico de barras com os rótulos
grafico_completo = grafico_barras + rotulos

# Exibir o gráfico no Streamlit
st.altair_chart(grafico_completo, use_container_width=True)

# %%
# Seção de IA Integrada
st.markdown("---")
st.subheader("🤖 Assistente IA - Análise Inteligente")

# Classe do Assistente IA com integração Hugging Face
class AIAssistant:
    def __init__(self, df_data):
        self.df = df_data
        self.huggingface_token = self.load_token()
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
    def load_token(self):
        """Carrega o token do Hugging Face do arquivo .env"""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('HUGGINGFACE_TOKEN='):
                            return line.split('=')[1].strip()
        except Exception as e:
            print(f"Erro ao carregar token: {e}")
        return None
    
    def query_huggingface(self, text):
        """Consulta a API do Hugging Face para análise de texto"""
        if not self.huggingface_token:
            return None
            
        try:
            import requests
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            payload = {
                "inputs": text,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro na consulta Hugging Face: {e}")
            return None
        
    def analyze_question(self, question):
        """Analisa a pergunta do usuário usando IA e regras locais"""
        question_lower = question.lower()
        
        analysis_type = "ranking"
        entities = {}
        limit = None
        confidence = 0.5
        
        # Detectar limite (top 10, top 20, etc.)
        import re
        top_match = re.search(r'top\s+(\d+)', question_lower)
        if top_match:
            limit = int(top_match.group(1))
            entities['limit'] = limit
        
        # Detectar "X maiores"
        maiores_match = re.search(r'(\d+)\s+maiores', question_lower)
        if maiores_match:
            limit = int(maiores_match.group(1))
            entities['limit'] = limit
        
        # Detectar análise temporal
        temporal_phrases = ['cada mês', 'por mês', 'valor total de cada mês', 'mensal', 'mês a mês', 'evolução temporal', 'crescimento temporal']
        if any(phrase in question_lower for phrase in temporal_phrases):
            analysis_type = "temporal"
            entities['periodo'] = True
            confidence += 0.3
        elif any(word in question_lower for word in ['temporal', 'tempo', 'evolução', 'crescimento', 'tendência']):
            analysis_type = "temporal"
            entities['periodo'] = True
            confidence += 0.2
        
        # Detectar Type 07
        if any(word in question_lower for word in ['type 07', 'type07', 'tipo 07']):
            entities['type_07'] = True
            confidence += 0.2
            
        # Detectar Type 05
        if any(word in question_lower for word in ['type 05', 'type05', 'tipo 05']):
            entities['type_05'] = True
            confidence += 0.2
            
        # Detectar Type 06
        if any(word in question_lower for word in ['type 06', 'type06', 'tipo 06']):
            entities['type_06'] = True
            confidence += 0.2
            
        # Detectar USI
        if any(word in question_lower for word in ['usi', 'usina', 'planta']):
            entities['usi'] = True
            confidence += 0.2
            
        # Detectar fornecedor
        if any(word in question_lower for word in ['fornecedor', 'supplier', 'empresa']):
            entities['fornecedor'] = True
            confidence += 0.2
            
        # Detectar waterfall
        if any(word in question_lower for word in ['waterfall', 'cascata', 'variação', 'variações']):
            analysis_type = "waterfall"
            confidence += 0.3
            
        # Detectar ranking/top
        if any(word in question_lower for word in ['maior', 'menor', 'top', 'ranking', 'melhor', 'pior']):
            analysis_type = "ranking"
            confidence += 0.3
        
        # Consultar Hugging Face se disponível
        ai_response = None
        if self.huggingface_token:
            try:
                hf_response = self.query_huggingface(question)
                if hf_response and isinstance(hf_response, list) and len(hf_response) > 0:
                    ai_response = hf_response[0].get('generated_text', '')
                    confidence += 0.1
            except:
                pass
            
        return {
            'type': analysis_type,
            'entities': entities,
            'original_question': question,
            'limit': limit,
            'confidence': confidence,
            'ai_response': ai_response
        }
    
    def generate_sql_query(self, analysis):
        """Gera query SQL baseada na análise"""
        query = "SELECT "
        
        if analysis['type'] == 'ranking':
            if 'type_07' in analysis['entities']:
                query += "`Type 07`, SUM(Valor) as total_valor FROM df GROUP BY `Type 07` ORDER BY total_valor DESC"
            elif 'type_05' in analysis['entities']:
                query += "`Type 05`, SUM(Valor) as total_valor FROM df GROUP BY `Type 05` ORDER BY total_valor DESC"
            elif 'type_06' in analysis['entities']:
                query += "`Type 06`, SUM(Valor) as total_valor FROM df GROUP BY `Type 06` ORDER BY total_valor DESC"
            elif 'fornecedor' in analysis['entities']:
                query += "`Nome do fornecedor`, SUM(Valor) as total_valor FROM df GROUP BY `Nome do fornecedor` ORDER BY total_valor DESC"
            elif 'usi' in analysis['entities']:
                query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'periodo' in analysis['entities']:
                query += "Período, SUM(Valor) as total_valor FROM df GROUP BY Período ORDER BY total_valor DESC"
            else:
                query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
                
        elif analysis['type'] == 'temporal':
            query += "Período, SUM(Valor) as total_valor FROM df GROUP BY Período ORDER BY Período"
            
        elif analysis['type'] == 'waterfall':
            query += "Período, SUM(Valor) as total_valor FROM df GROUP BY Período ORDER BY Período"
            
        else:
            query += "SUM(Valor) as total_valor FROM df"
            
        return query
    
    def execute_query(self, query, limit=None):
        """Executa a query SQL"""
        try:
            if 'GROUP BY' in query:
                if '`Type 07`' in query:
                    result = self.df.groupby('Type 07')['Valor'].sum().reset_index()
                    result.columns = ['Type 07', 'total_valor']
                elif '`Type 05`' in query:
                    result = self.df.groupby('Type 05')['Valor'].sum().reset_index()
                    result.columns = ['Type 05', 'total_valor']
                elif '`Type 06`' in query:
                    result = self.df.groupby('Type 06')['Valor'].sum().reset_index()
                    result.columns = ['Type 06', 'total_valor']
                elif '`Nome do fornecedor`' in query:
                    result = self.df.groupby('Nome do fornecedor')['Valor'].sum().reset_index()
                    result.columns = ['Nome do fornecedor', 'total_valor']
                elif 'USI' in query:
                    result = self.df.groupby('USI')['Valor'].sum().reset_index()
                    result.columns = ['USI', 'total_valor']
                elif 'Período' in query:
                    result = self.df.groupby('Período')['Valor'].sum().reset_index()
                    result.columns = ['Período', 'total_valor']
                else:
                    result = pd.DataFrame()
                
                if not result.empty:
                    result = result.sort_values('total_valor', ascending=False).reset_index(drop=True)
                
                if limit and not result.empty:
                    result = result.head(limit)
            else:
                if 'SUM(Valor)' in query:
                    total = self.df['Valor'].sum()
                    result = pd.DataFrame({'total_valor': [total]})
                else:
                    result = pd.DataFrame()
            
            return result
        except Exception as e:
            st.error(f"Erro na query: {str(e)}")
            return pd.DataFrame()
    
    def create_visualization(self, data, analysis):
        """Cria visualização baseada nos dados"""
        if data.empty:
            return None
            
        if analysis['type'] == 'ranking':
            if len(data.columns) >= 2:
                col1 = data.columns[0]
                col2 = data.columns[1]
                
                # Criar gráfico de barras com Altair
                chart = alt.Chart(data).mark_bar(color='steelblue').encode(
                    x=alt.X(f'{col1}:N', title=col1, sort=alt.SortField(field=col2, order='descending')),
                    y=alt.Y(f'{col2}:Q', title='Valor Total (R$)'),
                    tooltip=[f'{col1}:N', f'{col2}:Q']
                ).properties(
                    title=f"Ranking por {col1}"
                )
                
                # Adicionar rótulos
                labels = chart.mark_text(
                    align='center',
                    baseline='bottom',
                    dy=-5,
                    color='white',
                    fontSize=12,
                    fontWeight='bold'
                ).encode(
                    text=alt.Text(f'{col2}:Q', format='R$ ,.2f')
                )
                
                return chart + labels
                
        elif analysis['type'] == 'temporal':
            if len(data.columns) >= 2:
                col1 = data.columns[0]
                col2 = data.columns[1]
                chart = alt.Chart(data).mark_line(point=True, color='steelblue').encode(
                    x=alt.X(f'{col1}:N', title=col1),
                    y=alt.Y(f'{col2}:Q', title='Valor Total (R$)'),
                    tooltip=[f'{col1}:N', f'{col2}:Q']
                ).properties(
                    title="Evolução Temporal"
                )
                return chart
                
        elif analysis['type'] == 'waterfall':
            if len(data.columns) >= 2:
                col1 = data.columns[0]
                col2 = data.columns[1]
                
                # Criar gráfico waterfall com Plotly
                fig = go.Figure(go.Waterfall(
                    name="Waterfall",
                    orientation="v",
                    measure=["absolute"] + ["relative"] * (len(data) - 2) + ["absolute"],
                    x=data[col1].tolist(),
                    y=data[col2].tolist(),
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                ))
                fig.update_layout(
                    title="Análise Waterfall - Variações por Período",
                    xaxis_title=col1,
                    yaxis_title="Valor (R$)"
                )
                return fig
                
        return None
    
    def generate_response(self, analysis, data):
        """Gera resposta textual"""
        if data.empty:
            return "❌ Não foi possível encontrar dados para sua pergunta."
            
        response = f"📊 **Análise: {analysis['type'].title()}**\n\n"
        
        if analysis.get('limit'):
            response += f"🔢 **Mostrando:** Top {analysis['limit']} resultados\n\n"
        
        if analysis['type'] == 'ranking':
            if len(data) > 0:
                value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                top_item = data.iloc[0]
                response += f"🏆 **Top 1:** {top_item.iloc[0]} - R$ {top_item[value_col]:,.2f}\n\n"
                response += f"📈 **Total de itens:** {len(data)}"
                if analysis.get('limit'):
                    response += f" (limitado a {analysis['limit']})"
                response += f"\n💰 **Valor total:** R$ {data[value_col].sum():,.2f}"
                
        elif analysis['type'] == 'temporal':
            if len(data) > 0:
                value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                response += f"📅 **Períodos analisados:** {len(data)}\n"
                response += f"💰 **Valor total:** R$ {data[value_col].sum():,.2f}\n"
                response += f"📊 **Média por período:** R$ {data[value_col].mean():,.2f}"
                
        elif analysis['type'] == 'waterfall':
            if len(data) > 0:
                value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                response += f"🌊 **Análise Waterfall:**\n"
                response += f"📅 **Períodos:** {len(data)}\n"
                response += f"💰 **Variação total:** R$ {data[value_col].sum():,.2f}"
        
        # Adicionar resposta da IA se disponível
        if 'ai_response' in analysis and analysis['ai_response']:
            response += f"\n\n🤖 **IA Hugging Face:** {analysis['ai_response']}"
        
        # Adicionar nível de confiança
        if 'confidence' in analysis:
            response += f"\n\n🎯 **Confiança da análise:** {analysis['confidence']:.1%}"
                
        return response
    
    def process_question(self, question):
        """Processa a pergunta completa"""
        analysis = self.analyze_question(question)
        query = self.generate_sql_query(analysis)
        data = self.execute_query(query, analysis.get('limit'))
        viz = self.create_visualization(data, analysis)
        response = self.generate_response(analysis, data)
        
        return {
            'response': response,
            'visualization': viz,
            'data': data,
            'analysis': analysis
        }

# Inicializar assistente com dados filtrados
assistant = AIAssistant(df_filtrado)

# Interface do chat IA
col1, col2 = st.columns([2, 1])

with col1:
    st.write("**💬 Faça perguntas sobre os dados:**")
    
    # Input para pergunta
    if prompt := st.text_input("Digite sua pergunta...", placeholder="Ex: Top 10 maiores Type 07"):
        # Processar pergunta
        with st.spinner("🤖 Analisando..."):
            result = assistant.process_question(prompt)
        
        # Exibir resposta
        st.write(result['response'])
        
        # Exibir visualização se disponível
        if result['visualization'] is not None:
            if result['analysis']['type'] == 'waterfall':
                # Para waterfall, usar Plotly
                st.plotly_chart(result['visualization'], use_container_width=True)
            else:
                # Para outros gráficos, usar Altair
                st.altair_chart(result['visualization'], use_container_width=True)
        
        # Exibir dados se disponíveis
        if not result['data'].empty:
            st.subheader("📊 Dados Detalhados")
            st.dataframe(result['data'], use_container_width=True)

with col2:
    st.write("**💡 Exemplos de perguntas:**")
    st.write("• Top 10 maiores Type 07")
    st.write("• 20 maiores fornecedores")
    st.write("• Top 5 USIs")
    st.write("• Evolução temporal")
    st.write("• Gráfico waterfall")
    st.write("• Valor total por período")
    
    st.write("**🎯 Tipos de análise:**")
    st.write("• **Ranking:** Top N maiores")
    st.write("• **Temporal:** Evolução no tempo")
    st.write("• **Waterfall:** Variações")
    
    # Status da API Hugging Face
    st.markdown("---")
    st.write("**🤖 Status da IA:**")
    if assistant.huggingface_token:
        st.success("✅ Hugging Face configurado")
        st.info("🤖 IA ativa para análise avançada")
    else:
        st.warning("⚠️ Hugging Face não configurado")
        st.info("💡 Configure na página 'Configurar IA'")