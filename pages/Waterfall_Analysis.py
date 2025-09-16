import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Análise Waterfall - KE5Z",
    page_icon="🌊",
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
st.title("🌊 Análise Waterfall - Variações Temporais")
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

# Filtros na lateral
st.sidebar.title("🔍 Filtros")

# Filtro 1: USINA
usina_opcoes = ["Todas"] + sorted(df_total['USI'].dropna().unique().tolist())
usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=["Todas"])

# Aplicar filtro de USI
if "Todas" in usina_selecionada or not usina_selecionada:
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total['USI'].isin(usina_selecionada)]

# NOVO: Seleção de Período (intervalo ou específicos)
periodos_disponiveis = sorted(df_filtrado['Período'].dropna().unique().tolist())
selected_periods_specific = []
if periodos_disponiveis:
    modo_periodo = st.sidebar.radio(
        "Modo de seleção de Período:",
        options=["Intervalo", "Períodos específicos"],
        index=0
    )
    if modo_periodo == "Intervalo":
        p_ini, p_fim = st.sidebar.select_slider(
            "Intervalo de Período (início, fim)",
            options=periodos_disponiveis,
            value=(periodos_disponiveis[0], periodos_disponiveis[-1])
        )
        # Tentar filtrar numericamente; se der erro, filtrar por posição/ordem
        try:
            df_filtrado = df_filtrado[(df_filtrado['Período'] >= p_ini) & (df_filtrado['Período'] <= p_fim)]
        except Exception:
            ordem = {v: i for i, v in enumerate(periodos_disponiveis)}
            df_filtrado = df_filtrado[df_filtrado['Período'].map(ordem).between(ordem[p_ini], ordem[p_fim])]
    else:
        colp1, colp2 = st.sidebar.columns(2)
        with colp1:
            p1 = st.selectbox("Período origem", periodos_disponiveis)
        with colp2:
            p2 = st.selectbox("Período destino", [p for p in periodos_disponiveis if p != p1])
        # Manter ordem temporal
        ordem = {v: i for i, v in enumerate(periodos_disponiveis)}
        selected_periods_specific = sorted([p1, p2], key=lambda x: ordem[x])
        df_filtrado = df_filtrado[df_filtrado['Período'].isin(selected_periods_specific)]

# Filtro 3: Centro cst
centro_cst_opcoes = ["Todos"] + sorted(df_filtrado['Centro cst'].dropna().unique().tolist())
centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)
if centro_cst_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Centro cst'] == centro_cst_selecionado]

# Filtro 4: Conta contabil
conta_contabil_opcoes = ["Todas"] + sorted(df_filtrado['Nº conta'].dropna().unique().tolist())
conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contabil:", conta_contabil_opcoes)
if conta_contabil_selecionadas and "Todas" not in conta_contabil_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Nº conta'].isin(conta_contabil_selecionadas)]

# NOVOS FILTROS DE CATEGORIAS PARA CONSIDERAR NOS VALORES
# Type 07
if 'Type 07' in df_filtrado.columns:
    type07_ops = ["Todas"] + sorted(df_filtrado['Type 07'].dropna().unique().tolist())
    type07_sel = st.sidebar.multiselect("Type 07:", type07_ops)
    if type07_sel and "Todas" not in type07_sel:
        df_filtrado = df_filtrado[df_filtrado['Type 07'].isin(type07_sel)]

# Type 06
if 'Type 06' in df_filtrado.columns:
    type06_ops = ["Todas"] + sorted(df_filtrado['Type 06'].dropna().unique().tolist())
    type06_sel = st.sidebar.multiselect("Type 06:", type06_ops)
    if type06_sel and "Todas" not in type06_sel:
        df_filtrado = df_filtrado[df_filtrado['Type 06'].isin(type06_sel)]

# Type 05
if 'Type 05' in df_filtrado.columns:
    type05_ops = ["Todas"] + sorted(df_filtrado['Type 05'].dropna().unique().tolist())
    type05_sel = st.sidebar.multiselect("Type 05:", type05_ops)
    if type05_sel and "Todas" not in type05_sel:
        df_filtrado = df_filtrado[df_filtrado['Type 05'].isin(type05_sel)]

# Oficina
if 'Oficina' in df_filtrado.columns:
    oficina_ops = ["Todas"] + sorted(df_filtrado['Oficina'].dropna().unique().tolist())
    oficina_sel = st.sidebar.multiselect("Oficina:", oficina_ops)
    if oficina_sel and "Todas" not in oficina_sel:
        df_filtrado = df_filtrado[df_filtrado['Oficina'].isin(oficina_sel)]

# Fornecedor
if 'Nome do fornecedor' in df_filtrado.columns:
    forn_ops = ["Todos"] + sorted(df_filtrado['Nome do fornecedor'].dropna().unique().tolist())
    forn_sel = st.sidebar.multiselect("Fornecedores:", forn_ops)
    if forn_sel and "Todos" not in forn_sel:
        df_filtrado = df_filtrado[df_filtrado['Nome do fornecedor'].isin(forn_sel)]

# Mostrar estatísticas dos filtros
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Estatísticas")
st.sidebar.write(f"**Registros:** {len(df_filtrado):,}")
st.sidebar.write(f"**Valor Total:** R$ {df_filtrado['Valor'].sum():,.2f}")
st.sidebar.write(f"**USIs:** {df_filtrado['USI'].nunique()}")
st.sidebar.write(f"**Períodos:** {df_filtrado['Período'].nunique()}")

# Classe para Análise Waterfall
class WaterfallAnalyzer:
    def __init__(self, df_data):
        self.df = df_data
        
    def create_temporal_waterfall(self, period_df: pd.DataFrame, mode: str = "contribuicao"):
        """Cria um gráfico waterfall temporal baseado no modo escolhido.
        mode: "contribuicao" | "delta_absoluto" | "delta_percentual"
        """
        if period_df.empty or len(period_df) < 2:
            st.warning("⚠️ Dados insuficientes para criar gráfico waterfall")
            return None
        
        # Garantir ordenação temporal
        period_df = period_df.sort_values('Período').reset_index(drop=True)
        labels_periodos = period_df['Período'].tolist()
        valores = period_df['Valor'].tolist()
        
        if mode == "contribuicao":
            # Começa do zero; cada período contribui para o total final
            labels = ["Inicial"] + labels_periodos + ["Total"]
            y_vals = [0] + valores + [sum(valores)]
            measures = ["absolute"] + ["relative"] * len(valores) + ["total"]
            tick_kwargs = {"tickformat": ",.0f", "tickprefix": "R$ "}
            title = "Contribuição por Período (Acumulado)"
        elif mode == "delta_absoluto":
            # Variação em relação ao período anterior
            deltas = pd.Series(valores).diff().iloc[1:].fillna(0).tolist()
            labels = ["Inicial"] + labels_periodos[1:] + ["Final"]
            y_vals = [valores[0]] + deltas + [valores[-1]]
            measures = ["absolute"] + ["relative"] * len(deltas) + ["total"]
            tick_kwargs = {"tickformat": ",.0f", "tickprefix": "R$ "}
            title = "Variação Absoluta Mês a Mês"
        else:  # delta_percentual
            pct = (pd.Series(valores).pct_change().iloc[1:] * 100).fillna(0).tolist()
            labels = ["Inicial (0%)"] + labels_periodos[1:] + ["Total"]
            y_vals = [0] + pct + [sum(pct)]
            measures = ["absolute"] + ["relative"] * len(pct) + ["total"]
            tick_kwargs = {"tickformat": ",.1f", "ticksuffix": "%"}
            title = "Variação Percentual Mês a Mês"
        
        fig = go.Figure(go.Waterfall(
            name="Waterfall",
            orientation="v",
            measure=measures,
            x=labels,
            y=y_vals,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
            decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
            totals={"marker": {"color": "#4682B4"}}
        ))
        
        fig.update_layout(
            title={
                'text': f"<b>Variações Temporais</b><br><sub>{title}</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            xaxis_title="Período",
            yaxis_title="Valor",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        
        # Formatação do eixo Y
        fig.update_yaxes(**tick_kwargs)
        
        return fig
    
    def analyze_period_variations(self):
        """Analisa variações por período"""
        # Agrupar por período
        period_data = self.df.groupby('Período')['Valor'].sum().reset_index()
        period_data = period_data.sort_values('Período')
        
        if len(period_data) < 2:
            return None, "Dados insuficientes para análise temporal"
            
        # Calcular variações
        period_data['Variacao'] = period_data['Valor'].diff()
        period_data['Variacao_Percentual'] = (period_data['Variacao'] / period_data['Valor'].shift(1)) * 100
        
        return period_data, None
    
    def analyze_usi_variations(self):
        """Analisa variações por USI"""
        # Agrupar por USI
        usi_data = self.df.groupby('USI')['Valor'].sum().reset_index()
        usi_data = usi_data.sort_values('Valor', ascending=False)
        
        return usi_data, None
    
    def analyze_type_variations(self, type_column):
        """Analisa variações por tipo (Type 05, 06, 07)"""
        if type_column not in self.df.columns:
            return None, f"Coluna {type_column} não encontrada"
            
        # Agrupar por tipo
        type_data = self.df.groupby(type_column)['Valor'].sum().reset_index()
        type_data = type_data.sort_values('Valor', ascending=False)
        
        return type_data, None
    
    def analyze_supplier_variations(self):
        """Analisa variações por fornecedor"""
        # Agrupar por fornecedor
        supplier_data = self.df.groupby('Nome do fornecedor')['Valor'].sum().reset_index()
        supplier_data = supplier_data.sort_values('Valor', ascending=False)
        
        return supplier_data, None

# Inicializar analisador
analyzer = WaterfallAnalyzer(df_filtrado)

# Interface principal
st.subheader("🌊 Análise Waterfall - Variações Temporais")

# ==========================
# Controles de Modo do Gráfico
# ==========================
modo_grafico = st.radio(
    "Modo do gráfico:",
    options=[
        "Simples por período",
        "Finanças (cadeia com categorias)"
    ],
    index=0,
    horizontal=True
)

# Sempre temporal: seletor do modo de variação (apenas para modo simples)
if modo_grafico == "Simples por período":
    col_a, col_b = st.columns([1, 2])
    with col_a:
        mode = st.radio(
            "Como mostrar as variações:",
            options=[
                "Contribuição (valor do período)",
                "Δ Absoluto (mês a mês)",
                "Δ Percentual (mês a mês)"
            ],
            index=0
        )

    # Mapear para chaves internas
    mode_key = {
        "Contribuição (valor do período)": "contribuicao",
        "Δ Absoluto (mês a mês)": "delta_absoluto",
        "Δ Percentual (mês a mês)": "delta_percentual",
    }[mode]

    # Executar análise temporal única
    st.markdown("### 📅 Análise Temporal - Variações por Período")
    period_data = df_filtrado.groupby('Período')['Valor'].sum().reset_index()

    fig = analyzer.create_temporal_waterfall(period_data, mode_key)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # Mostrar dados detalhados e métricas
    if not period_data.empty:
        st.subheader("📊 Dados Detalhados")
        show_df = period_data.copy()
        show_df['Valor'] = show_df['Valor'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(show_df, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Valor Total", f"R$ {period_data['Valor'].sum():,.2f}")
        with col2:
            st.metric("📈 Máximo Período", f"R$ {period_data['Valor'].max():,.2f}")
        with col3:
            st.metric("📉 Mínimo Período", f"R$ {period_data['Valor'].min():,.2f}")
        with col4:
            st.metric("📊 Média por Período", f"R$ {period_data['Valor'].mean():,.2f}")

else:
    # ==========================
    # MODO FINANÇAS (cadeia com categorias) - apenas 2 períodos
    # ==========================
    st.markdown("### 💼 Waterfall de Finanças - Cadeia por Categorias (2 períodos)")

    # Seleção de categoria de variação
    categorias_possiveis = [
        ('USI', 'USI'),
        ('Type 07', 'Type 07'),
        ('Type 06', 'Type 06'),
        ('Type 05', 'Type 05'),
        ('Oficina', 'Oficina') if 'Oficina' in df_filtrado.columns else None,
        ('Fornecedor', 'Nome do fornecedor') if 'Nome do fornecedor' in df_filtrado.columns else None,
    ]
    categorias_possiveis = [c for c in categorias_possiveis if c]

    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col1:
        cat_label_to_col = {label: col for label, col in categorias_possiveis}
        cat_label = st.selectbox("Categoria para decompor a variação:", list(cat_label_to_col.keys()))
        cat_col = cat_label_to_col[cat_label]
    with col2:
        top_k = st.slider("Top categorias (limite de barras)", min_value=3, max_value=20, value=8, step=1)

    uniq_periods = int(df_filtrado['Período'].nunique())
    if uniq_periods < 2:
        with col3:
            st.warning("Selecione ao menos 2 períodos no filtro lateral para usar o modo Finanças.")
        st.stop()
    with col3:
        incluir_outros = st.checkbox("Incluir 'Outros'", value=True)

    # Preparar dados por período e categoria
    df_base = df_filtrado.copy()
    # Garantir que categorias nulas não sejam descartadas na agregação
    if cat_col in df_base.columns:
        df_base[cat_col] = df_base[cat_col].fillna('Sem categoria')
    base = df_base.groupby(['Período', cat_col])['Valor'].sum().reset_index()
    periodos_ordenados = sorted(base['Período'].unique())
    # Pegar períodos conforme seleção: específicos (se houver) ou os dois últimos
    if selected_periods_specific:
        periodos_usados = selected_periods_specific
    else:
        periodos_usados = periodos_ordenados[-2:]

    # Construir sequência para o gráfico waterfall encadeado
    labels_seq = []
    values_seq = []
    measures_seq = []
    text_seq = []

    def add_total(periodo, total_val, is_first=False):
        labels_seq.append(f"Total {periodo}")
        if is_first:
            values_seq.append(total_val)
            measures_seq.append("absolute")
        else:
            # Para barras 'total' o y deve ser 0; o valor real fica no texto
            values_seq.append(0)
            measures_seq.append("total")
        text_seq.append(f"R$ {total_val:,.0f}")

    def add_deltas(delta_df):
        # delta_df: DataFrame com colunas [categoria, delta]
        for _, row in delta_df.iterrows():
            labels_seq.append(str(row[cat_col]))
            values_seq.append(row['delta'])
            measures_seq.append("relative")
            text_seq.append(f"R$ {row['delta']:,.0f}")

    # Iterar na transição entre os 2 períodos selecionados
    for i in range(len(periodos_usados) - 1):
        p1, p2 = periodos_usados[i], periodos_usados[i + 1]
        df_p1 = base[base['Período'] == p1].set_index(cat_col)['Valor']
        df_p2 = base[base['Período'] == p2].set_index(cat_col)['Valor']
        # alinhar categorias
        all_cats = df_p1.index.union(df_p2.index)
        v1 = df_p1.reindex(all_cats, fill_value=0)
        v2 = df_p2.reindex(all_cats, fill_value=0)
        delta = (v2 - v1).to_frame('delta').reset_index().rename(columns={cat_col: cat_col})
        # ordenar por |delta|
        delta['abs'] = delta['delta'].abs()
        delta_sorted = delta.sort_values('abs', ascending=False)
        principais = delta_sorted.head(top_k)
        if incluir_outros and len(delta_sorted) > top_k:
            outros_val = delta_sorted.iloc[top_k:]['delta'].sum()
            if outros_val != 0:
                principais = pd.concat([principais, pd.DataFrame({cat_col: ['Outros (agr.)'], 'delta': [outros_val], 'abs': [abs(outros_val)]})], ignore_index=True)
        # Adicionar total inicial (p1)
        if i == 0:
            add_total(p1, v1.sum(), is_first=True)
        # Adicionar deltas
        add_deltas(principais[[cat_col, 'delta']])
        # Adicionar total destino (p2)
        add_total(p2, v2.sum(), is_first=False)

    # Construir figura
    fig_fin = go.Figure(go.Waterfall(
        name="Cadeia",
        orientation="v",
        measure=measures_seq,
        x=labels_seq,
        y=values_seq,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#e74c3c"}},  # Vermelho para aumentos
        decreasing={"marker": {"color": "#27ae60"}},  # Verde para diminuições
        totals={"marker": {"color": "#4682B4"}},
        text=text_seq,
        textposition="outside"
    ))
    fig_fin.update_layout(
        title={
            'text': f"<b>Cadeia Mensal</b><br><sub>Decomposição por {cat_label} | Top {top_k} | Períodos: {periodos_usados[0]} → {periodos_usados[1]}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title="Período / Categorias",
        yaxis_title="Valor",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=550
    )
    fig_fin.update_yaxes(tickformat=",.0f", tickprefix="R$ ")

    st.plotly_chart(fig_fin, use_container_width=True)

    # Conferência de totais por período (para facilitar validação com a tabela)
    st.subheader("🧮 Conferência de Totais por Período (após filtros)")
    conf = df_filtrado.groupby('Período')['Valor'].sum().reset_index().sort_values('Período')
    st.dataframe(conf.rename(columns={'Valor': 'Total do Período'}).style.format({'Total do Período': 'R$ {:,.2f}'}), use_container_width=True)

# Seção de exportação
st.markdown("---")
st.subheader("📥 Exportar Análise")

def export_to_excel(data, filename):
    """Exporta dados para Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Waterfall_Analysis')
    output.seek(0)
    return output.getvalue()

# Botão para exportar dados atuais
if st.button("📊 Exportar Dados para Excel", use_container_width=True):
    with st.spinner("Gerando arquivo Excel..."):
        if modo_grafico == "Simples por período":
            if mode == "contribuicao":
                export_data = analyzer.create_temporal_waterfall(period_data, mode_key)
            elif mode == "delta_absoluto":
                export_data = analyzer.create_temporal_waterfall(period_data, mode_key)
            elif mode == "delta_percentual":
                export_data = analyzer.create_temporal_waterfall(period_data, mode_key)
            else:
                export_data = pd.DataFrame()
        else: # modo_grafico == "Finanças (cadeia com categorias)"
            # Para o modo de finanças, precisamos passar os dados brutos, não o waterfall
            # A lógica de exportação para o modo de finanças ainda precisa ser implementada
            # Por enquanto, vamos exportar os dados brutos do DataFrame base
            export_data = base

        if export_data.empty:
            st.error("❌ Nenhum dado disponível para exportação.")
        else:
            excel_data = export_to_excel(export_data, 'waterfall_analysis.xlsx')
            
            # Forçar download
            b64 = base64.b64encode(excel_data).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="waterfall_analysis.xlsx">💾 Clique aqui para baixar</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Arquivo gerado! Clique no link acima para baixar.")

# Informações sobre Waterfall
st.markdown("---")
st.subheader("ℹ️ Sobre a Análise Waterfall")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🌊 O que é Waterfall?**
    - Visualização de variações sequenciais
    - Mostra aumentos e diminuições
    - Ideal para análise temporal
    - Facilita identificação de tendências
    """)

with col2:
    st.markdown("""
    **📊 Como interpretar:**
    - 🟢 **Verde**: Diminuições nos valores
    - 🔴 **Vermelho**: Aumentos nos valores
    - 🔵 **Azul**: Valores totais/finais
    - 📈 **Conectores**: Mostram a progressão
    """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌊 Dashboard KE5Z - Análise Waterfall | Análise de Variações Temporais</p>
</div>
""", unsafe_allow_html=True)
