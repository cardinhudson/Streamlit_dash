import streamlit as st
import pandas as pd
import os
import altair as alt
import plotly.graph_objects as go
from datetime import datetime
import re

# Configuração da página
st.set_page_config(
    page_title="IA Unificada - KE5Z",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
from auth import verificar_autenticacao, verificar_status_aprovado, exibir_header_usuario
verificar_autenticacao()

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Título da página
st.title("🤖 IA Unificada - Assistente & Análise Waterfall")
st.markdown("---")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Carregar dados
@st.cache_data
def load_data():
    """Carrega os dados do arquivo parquet"""
    try:
        arquivo_parquet = os.path.join("KE5Z", "KE5Z.parquet")
        df = pd.read_parquet(arquivo_parquet)
        # Incluir todos os dados (incluindo Others)
        df = df[df['USI'].notna()]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

# Carregar dados
df_total = load_data()

if df_total.empty:
    st.error("❌ Não foi possível carregar os dados. Verifique se o arquivo KE5Z.parquet existe.")
    st.stop()

# Aplicar filtros padrão do projeto
st.sidebar.title("Filtros")

# Filtro 1: USINA
usina_opcoes = ["Todos"] + sorted(df_total['USI'].dropna().astype(str).unique().tolist()) if 'USI' in df_total.columns else ["Todos"]
default_usina = ["Veículos"] if "Veículos" in usina_opcoes else ["Todos"]
usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=default_usina)

# Filtrar o DataFrame com base na USI
if "Todos" in usina_selecionada or not usina_selecionada:
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total['USI'].astype(str).isin(usina_selecionada)]

# Filtro 2: Período
periodo_opcoes = ["Todos"] + sorted(df_filtrado['Período'].dropna().astype(str).unique().tolist()) if 'Período' in df_filtrado.columns else ["Todos"]
periodo_selecionado = st.sidebar.selectbox("Selecione o Período:", periodo_opcoes)
if periodo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Período'].astype(str) == str(periodo_selecionado)]

# Filtro 3: Centro cst
if 'Centro cst' in df_filtrado.columns:
    centro_cst_opcoes = ["Todos"] + sorted(df_filtrado['Centro cst'].dropna().astype(str).unique().tolist())
    centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)
    if centro_cst_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Centro cst'].astype(str) == str(centro_cst_selecionado)]

# Filtro 4: Conta contábil
if 'Nº conta' in df_filtrado.columns:
    conta_contabil_opcoes = sorted(df_filtrado['Nº conta'].dropna().astype(str).unique().tolist())
    conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contábil:", conta_contabil_opcoes)
    if conta_contabil_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['Nº conta'].astype(str).isin(conta_contabil_selecionadas)]

# Filtros adicionais
for col_name, label in [("Fornecedor", "Fornecedor"), ("Type 05", "Type 05"), ("Type 06", "Type 06"), ("Type 07", "Type 07")]:
    if col_name in df_filtrado.columns:
        opcoes = ["Todos"] + sorted(df_filtrado[col_name].dropna().astype(str).unique().tolist())
        selecionadas = st.sidebar.multiselect(f"Selecione o {label}:", opcoes, default=["Todos"])
        if selecionadas and "Todos" not in selecionadas:
            df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]

# Exibir informações dos filtros
st.sidebar.write(f"Número de linhas: {df_filtrado.shape[0]}")
st.sidebar.write(f"Número de colunas: {df_filtrado.shape[1]}")
st.sidebar.write(f"Soma do Valor total: R$ {df_filtrado['Valor'].sum():,.2f}")

# Usar df_filtrado em vez de df_total no restante da página

# Classe do Assistente IA Unificado
class UnifiedAIAssistant:
    def __init__(self, df_data):
        self.df = df_data
        
    def analyze_question(self, question):
        """Analisa a pergunta usando regras locais simples"""
        question_lower = question.lower()
        
        analysis_type = "ranking"
        entities = {}
        limit = 10  # padrão
        confidence = 0.8
        
        # Detectar limite (top 10, top 20, etc.)
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
        if any(phrase in question_lower for phrase in ['temporal', 'tempo', 'evolução', 'mensal', 'mês']):
            analysis_type = "temporal"
            entities['periodo'] = True
        
        # Detectar waterfall
        if any(word in question_lower for word in ['waterfall', 'cascata', 'variação']):
            analysis_type = "waterfall"
        
        # Detectar entidades específicas
        if any(word in question_lower for word in ['type 07', 'type07']):
            entities['type_07'] = True
        if any(word in question_lower for word in ['type 05', 'type05']):
            entities['type_05'] = True
        if any(word in question_lower for word in ['type 06', 'type06']):
            entities['type_06'] = True
        if any(word in question_lower for word in ['usi', 'usina']):
            entities['usi'] = True
        if any(word in question_lower for word in ['fornecedor', 'supplier']):
            entities['fornecedor'] = True
            
        return {
            'type': analysis_type,
            'entities': entities,
            'original_question': question,
            'limit': limit,
            'confidence': confidence
        }
    
    def execute_analysis(self, analysis):
        """Executa a análise baseada no tipo detectado"""
        try:
            if analysis['type'] == 'ranking':
                return self._ranking_analysis(analysis)
            elif analysis['type'] == 'temporal':
                return self._temporal_analysis(analysis)
            elif analysis['type'] == 'waterfall':
                return self._waterfall_analysis(analysis)
            else:
                return self._default_analysis(analysis)
        except Exception as e:
            st.error(f"Erro na análise: {str(e)}")
            return None
    
    def _ranking_analysis(self, analysis):
        """Análise de ranking"""
        entities = analysis['entities']
        limit = analysis.get('limit', 10)
        
        if entities.get('type_07'):
            data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 07"
        elif entities.get('type_05'):
            data = self.df.groupby('Type 05')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 05"
        elif entities.get('type_06'):
            data = self.df.groupby('Type 06')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 06"
        elif entities.get('usi'):
            data = self.df.groupby('USI')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} USIs"
        elif entities.get('fornecedor'):
            data = self.df.groupby('Fornecedor')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Fornecedores"
        else:
            # Padrão: Type 07
            data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
            data = data.sort_values('Valor', ascending=False).head(limit)
            title = f"Top {limit} Type 07"
        
        # Criar gráfico
        if len(data.columns) >= 2:
            col1, col2 = data.columns[0], data.columns[1]
            chart = alt.Chart(data).mark_bar().encode(
                x=alt.X(f'{col1}:N', sort='-y', title=col1),
                y=alt.Y(f'{col2}:Q', title='Valor (R$)'),
                color=alt.Color(f'{col2}:Q', scale=alt.Scale(range=['#27ae60', '#e74c3c']))
            ).properties(title=title, width=600, height=400)
        else:
            chart = None
        
        return {
            'data': data,
            'chart': chart,
            'title': title,
            'response': f"📊 {title}\\n💰 Valor total: R$ {data[data.columns[1]].sum():,.2f}"
        }
    
    def _temporal_analysis(self, analysis):
        """Análise temporal"""
        data = self.df.groupby('Período')['Valor'].sum().reset_index()
        data = data.sort_values('Período')
        
        chart = alt.Chart(data).mark_line(point=True, color='#3498db').encode(
            x=alt.X('Período:O', title='Período'),
            y=alt.Y('Valor:Q', title='Valor (R$)'),
        ).properties(title="Evolução Temporal", width=600, height=400)
        
        return {
            'data': data,
            'chart': chart,
            'title': "Evolução Temporal",
            'response': f"📈 Evolução temporal\\n📅 Períodos: {len(data)}\\n💰 Valor total: R$ {data['Valor'].sum():,.2f}"
        }
    
    def _waterfall_analysis(self, analysis):
        """Análise waterfall"""
        data = self.df.groupby('Período')['Valor'].sum().reset_index()
        data = data.sort_values('Período')
        
        if len(data) >= 2:
            fig = go.Figure(go.Waterfall(
                name="Waterfall",
                orientation="v",
                measure=["absolute"] + ["relative"] * (len(data) - 2) + ["absolute"],
                x=data['Período'].tolist(),
                y=data['Valor'].tolist(),
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
                decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
                totals={"marker": {"color": "#3498db"}}       # Azul para totais
            ))
            fig.update_layout(
                title="Análise Waterfall - Variações por Período",
                xaxis_title="Período",
                yaxis_title="Valor (R$)",
                height=500
            )
        else:
            fig = None
        
        return {
            'data': data,
            'chart': fig,
            'title': "Análise Waterfall",
            'response': f"🌊 Análise Waterfall\\n📅 Períodos: {len(data)}\\n💰 Variação total: R$ {data['Valor'].sum():,.2f}"
        }
    
    def _default_analysis(self, analysis):
        """Análise padrão"""
        data = self.df.groupby('Type 07')['Valor'].sum().reset_index()
        data = data.sort_values('Valor', ascending=False).head(10)
        
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('Type 07:N', sort='-y', title='Type 07'),
            y=alt.Y('Valor:Q', title='Valor (R$)'),
            color=alt.Color('Valor:Q', scale=alt.Scale(range=['#27ae60', '#e74c3c']))
        ).properties(title="Top 10 Type 07", width=600, height=400)
        
        return {
            'data': data,
            'chart': chart,
            'title': "Top 10 Type 07",
            'response': f"📊 Top 10 Type 07\\n💰 Valor total: R$ {data['Valor'].sum():,.2f}"
        }

# Função para criar gráfico waterfall configurável
def create_waterfall_chart(data, x_col, y_col, title):
    """Cria um gráfico waterfall"""
    if len(data) < 2:
        st.warning("⚠️ Dados insuficientes para criar gráfico waterfall.")
        return None
    
    # Preparar dados para waterfall
    values = data[y_col].tolist()
    labels = data[x_col].tolist()
    
    # Criar medidas (primeiro é absoluto, intermediários são relativos, último é total)
    measures = ["absolute"]
    for i in range(1, len(values) - 1):
        measures.append("relative")
    if len(values) > 1:
        measures.append("total")
    
    fig = go.Figure(go.Waterfall(
        name="Waterfall Analysis",
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
        decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
        totals={"marker": {"color": "#3498db"}}       # Azul para totais
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="Valor (R$)",
        height=500,
        showlegend=False
    )
    
    return fig

# Inicializar assistente
assistant = UnifiedAIAssistant(df_filtrado)

# Tabs para organizar as funcionalidades
tab1, tab2 = st.tabs(["🤖 Assistente IA", "🌊 Análise Waterfall"])

# TAB 1: Assistente IA
with tab1:
    st.subheader("💬 Chat com IA Local")
    
    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Exibir gráfico se existir
            if "chart" in message and message["chart"] is not None:
                if hasattr(message["chart"], 'update_layout'):  # Plotly
                    st.plotly_chart(message["chart"], use_container_width=True)
                else:  # Altair
                    st.altair_chart(message["chart"], use_container_width=True)
            
            # Exibir dados se existir
            if "data" in message and message["data"] is not None:
                with st.expander("📊 Ver dados detalhados"):
                    st.dataframe(message["data"], use_container_width=True)

    # Input do usuário
    if prompt := st.chat_input("Faça uma pergunta sobre os dados..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar pergunta
        with st.chat_message("assistant"):
            with st.spinner("Analisando..."):
                # Analisar pergunta
                analysis = assistant.analyze_question(prompt)
                
                # Executar análise
                result = assistant.execute_analysis(analysis)
                
                if result:
                    # Exibir resposta
                    st.markdown(result['response'])
                    
                    # Exibir gráfico
                    if result['chart'] is not None:
                        if hasattr(result['chart'], 'update_layout'):  # Plotly
                            st.plotly_chart(result['chart'], use_container_width=True)
                        else:  # Altair
                            st.altair_chart(result['chart'], use_container_width=True)
                    
                    # Exibir dados
                    if not result['data'].empty:
                        with st.expander("📊 Ver dados detalhados"):
                            st.dataframe(result['data'], use_container_width=True)
                    
                    # Adicionar ao histórico
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result['response'],
                        "chart": result['chart'],
                        "data": result['data']
                    })
                else:
                    error_msg = "❌ Não foi possível processar sua pergunta. Tente reformular."
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# TAB 2: Análise Waterfall
with tab2:
    st.subheader("🌊 Análise Waterfall Configurável")

    # Configurações (mesmo padrão do Waterfall_Analysis)
    st.markdown("### ⚙️ Configurações")

    # Detectar tema do Streamlit para aplicar no gráfico (dark/light)
    theme_base = st.get_option("theme.base") or "light"
    bg_color = st.get_option("theme.backgroundColor") or ("#0e1117" if theme_base == "dark" else "#FFFFFF")
    sec_bg_color = st.get_option("theme.secondaryBackgroundColor") or ("#262730" if theme_base == "dark" else "#F5F5F5")
    text_color = st.get_option("theme.textColor") or ("#FAFAFA" if theme_base == "dark" else "#000000")
    grid_color = "rgba(255,255,255,0.12)" if theme_base == "dark" else "rgba(0,0,0,0.12)"
    connector_color = "rgba(255,255,255,0.35)" if theme_base == "dark" else "rgba(0,0,0,0.35)"

    # Meses disponíveis a partir de 'Período'
    meses_disponiveis = sorted(df_filtrado['Período'].dropna().astype(str).unique().tolist())
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        mes_inicial = st.selectbox("Mês inicial:", meses_disponiveis, index=0)
    with col_b:
        mes_final = st.selectbox("Mês final:", meses_disponiveis, index=len(meses_disponiveis) - 1)

    # Dimensão de categoria
    dims_cat = [c for c in ['Type 05', 'Type 06', 'Type 07', 'Fornecedor', 'USI'] if c in df_filtrado.columns]
    if not dims_cat:
        st.warning("Não há colunas de categoria compatíveis (Type 05/06/07, Fornecedor, USI).")
        st.stop()
    chosen_dim = st.selectbox("Dimensão da categoria:", dims_cat, index=0)

    # Categorias disponíveis e multiselect com 'Todos'
    cats_all = sorted(df_filtrado[chosen_dim].dropna().astype(str).unique().tolist())
    vol_mf = (df_filtrado[df_filtrado['Período'].astype(str) == str(mes_final)]
              .groupby(chosen_dim)['Valor'].sum().sort_values(ascending=False))
    # Slider com máximo e padrão iguais ao total de categorias
    total_cats = max(1, len(cats_all))
    with col_c:
        max_cats = st.slider(f"Top N categorias (Total: {total_cats}):", 1, total_cats, total_cats)
    default_cats = [c for c in vol_mf.index[:max_cats]] if len(vol_mf) else cats_all[:max_cats]
    cats_options = ['Todos'] + cats_all
    cats_sel_raw = st.multiselect("Categorias (uma ou mais):", cats_options, default=default_cats)
    if (not cats_sel_raw) or ('Todos' in cats_sel_raw):
        cats_sel = cats_all
    else:
        cats_sel = cats_sel_raw

    if mes_inicial == mes_final:
        st.info("Selecione meses diferentes para comparar.")
        st.stop()

    # Totais de mês (todas as categorias)
    total_m1_all = float(df_filtrado[df_filtrado['Período'].astype(str) == str(mes_inicial)]['Valor'].sum())
    total_m2_all = float(df_filtrado[df_filtrado['Período'].astype(str) == str(mes_final)]['Valor'].sum())
    change_all = total_m2_all - total_m1_all

    # Filtrar pelas categorias escolhidas
    dff = df_filtrado[df_filtrado[chosen_dim].astype(str).isin(cats_sel)].copy()
    g1 = (dff[dff['Período'].astype(str) == str(mes_inicial)]
          .groupby(chosen_dim)['Valor'].sum())
    g2 = (dff[dff['Período'].astype(str) == str(mes_final)]
          .groupby(chosen_dim)['Valor'].sum())

    labels_cats, values_cats = [], []
    for cat in sorted(set(g1.index).union(set(g2.index))):
        delta = float(g2.get(cat, 0.0)) - float(g1.get(cat, 0.0))
        if abs(delta) > 1e-9:
            labels_cats.append(str(cat))
            values_cats.append(delta)

    # Aplicar Top N por impacto absoluto
    original_len = len(labels_cats)
    if len(labels_cats) > max_cats:
        idx = sorted(range(len(values_cats)), key=lambda i: abs(values_cats[i]), reverse=True)[:max_cats]
        labels_cats = [labels_cats[i] for i in idx]
        values_cats = [values_cats[i] for i in idx]
    cropped = len(labels_cats) < original_len

    # Remainder para fechar (com arredondamento)
    remainder = round(change_all - sum(values_cats), 2)
    all_selected = set(cats_sel) == set(cats_all)
    show_outros = (abs(remainder) >= 0.01) and (not all_selected or cropped)
    if show_outros:
        labels_cats.append('Outros')
        values_cats.append(remainder)

    labels = [f"Mês {mes_inicial}"] + labels_cats + [f"Mês {mes_final}"]
    values = [total_m1_all] + values_cats + [total_m2_all]
    measures = ['absolute'] + ['relative'] * len(values_cats) + ['total']

    # Gráfico principal com cores do tema
    fig = go.Figure(go.Waterfall(
        name='Variação',
        orientation='v',
        measure=measures,
        x=labels,
        y=values,
        text=[f"R$ {v:,.2f}" for v in values],
        textposition='outside',
        connector={'line': {'color': connector_color}},
        increasing={'marker': {'color': '#27ae60'}},
        decreasing={'marker': {'color': '#e74c3c'}},
        totals={'marker': {'color': '#4e79a7'}},
    ))
    # Rótulos de dados: branco no dark, preto no light
    fig.update_traces(textfont=dict(color=text_color))

    # Overlay "Outros" preto com base correta
    if show_outros:
        prev_sum = sum(v for lab, v in zip(labels_cats, values_cats) if lab != 'Outros')
        cum_before = total_m1_all + prev_sum
        base_val = cum_before if remainder >= 0 else cum_before + remainder
        height = abs(remainder)
        fig.add_trace(go.Bar(x=['Outros'], y=[height], base=[base_val], marker_color='#ff9800', opacity=1.0, hoverinfo='skip', showlegend=False))
        fig.update_layout(barmode='overlay')

    # Apply theme-aware template and transparent backgrounds to inherit app colors
    if theme_base == "dark":
        fig.update_layout(template="plotly_dark")
    else:
        fig.update_layout(template="plotly_white")

    fig.update_layout(
        title={'text': f"Variação Financeira - Mês {mes_inicial} para Mês {mes_final}", 'x': 0.5},
        xaxis_title='Mês / Categoria',
        yaxis_title='Valor (R$)',
        height=560,
        showlegend=False,
        # Transparente para herdar fundo da página (funciona em dark/light)
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_color),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, linecolor=grid_color),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color, linecolor=grid_color),
    )
    fig.update_yaxes(tickformat=",.0f", tickprefix="R$ ")

    st.plotly_chart(fig, use_container_width=True)

# Sidebar com exemplos
st.sidebar.title("🤖 IA Unificada")

# Exemplos de perguntas
st.sidebar.markdown("### 💡 Exemplos de Perguntas")
st.sidebar.markdown("""
**📊 Rankings:**
- Top 10 maiores Type 07
- 20 maiores fornecedores
- Top 5 USIs

**📈 Temporal:**
- Evolução temporal
- Valor por mês
- Tendência mensal

**🌊 Waterfall:**
- Gráfico waterfall
- Variações por período
- Análise de cascata
""")

# Botão para limpar histórico
if st.sidebar.button("🗑️ Limpar Histórico do Chat"):
    st.session_state.messages = []
    st.rerun()

# Informações sobre cores
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Legenda de Cores")
st.sidebar.markdown("""
- 🟢 **Verde**: Valores menores/diminuições
- 🔴 **Vermelho**: Valores maiores/aumentos
- 🔵 **Azul**: Totais e linhas temporais
""")

# Status
st.sidebar.markdown("---")
st.sidebar.write("**🤖 Status:**")
st.sidebar.success("✅ IA Local Ativa")
st.sidebar.info("📊 Análise baseada em regras locais")
st.sidebar.write(f"**📈 Registros:** {len(df_filtrado):,}")
st.sidebar.write(f"**💰 Valor Total:** R$ {df_filtrado['Valor'].sum():,.2f}")
