# %%
import streamlit as st
import pandas as pd
import os
import altair as alt
import subprocess
import sys
from auth import (verificar_autenticacao, exibir_header_usuario,
                  eh_administrador, verificar_status_aprovado,
                  carregar_usuarios, salvar_usuarios, criar_hash_senha)
from datetime import datetime

def executar_extracao():
    """Executa o script de extração e retorna o status"""
    try:
        # Verificar se o arquivo de extração existe
        if not os.path.exists("Extração.py"):
            return False, "Arquivo 'Extração.py' não encontrado!"

        # Executar o script de extração
        result = subprocess.run([sys.executable, "Extração.py"],
                                capture_output=True, text=True,
                                cwd=os.getcwd(),
                                timeout=300)  # Timeout de 5 minutos

        if result.returncode == 0:
            return True, "✅ Extração executada com sucesso!"
        else:
            error_msg = result.stderr if result.stderr else "Erro desconhecido"
            return False, f"❌ Erro na extração: {error_msg}"
    except subprocess.TimeoutExpired:
        return False, "⏰ Timeout: A extração demorou mais de 5 minutos"
    except FileNotFoundError:
        return False, "❌ Python não encontrado no sistema"
    except Exception as e:
        return False, f"❌ Erro ao executar extração: {str(e)}"

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

    # Botão para executar extração
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Atualizar Dados")

    if st.sidebar.button("📊 Executar Extração", 
                         use_container_width=True,
                         type="primary"):
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
excel_data_filtrada = exportar_excel(df_filtrado, 'KE5Z_tabela_filtrada.xlsx')
st.download_button(
    label="📥 Baixar Tabela Filtrada (Excel)",
    data=excel_data_filtrada,
    file_name='KE5Z_tabela_filtrada.xlsx',
    mime='application/vnd.openxmlformats-officedocument.'
         'spreadsheetml.sheet',
    use_container_width=True
)


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
excel_data_soma = exportar_excel(soma_por_type, 'KE5Z_soma_por_type.xlsx')
st.download_button(
    label="📥 Baixar Soma por Type (Excel)",
    data=excel_data_soma,
    file_name='KE5Z_soma_por_type.xlsx',
    mime='application/vnd.openxmlformats-officedocument.'
         'spreadsheetml.sheet',
    use_container_width=True
)

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
