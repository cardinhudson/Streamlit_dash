import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import requests
import json
import glob
import re
from typing import List, Tuple
import difflib

# Configuração da página
st.set_page_config(
    page_title="IUD - KE5Z",
    page_icon="🤖",
    layout="wide"
)

# Verificar autenticação
from auth import verificar_autenticacao, verificar_status_aprovado
verificar_autenticacao()

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Título da página
st.title("🤖 IUD - Inteligência Unificada de Dados")
st.markdown("---")
# Breve apresentação
st.markdown(
    """
    **Bem-vindo ao IUD (Inteligência Unificada de Dados)** — seu assistente para analisar os dados do KE5Z.
    - Faça perguntas em linguagem natural, gere gráficos (incluindo waterfall) e exporte resultados.
    - Digite sua pergunta no chat e veja a resposta com gráficos e tabelas.
    - Use os filtros laterais para direcionar a análise (USI, Período, Centro cst, etc.).
    """
)

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

# Inicializar session state para o chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Classe do Assistente IA
class AIAssistant:
    def __init__(self, df_data=None):
        self.df = df_data if df_data is not None else df_total
        self.huggingface_token = self.load_token()
        # Modelos gratuitos recomendados para instruções
        self.hf_models = [
            "google/flan-t5-base",
            "google/flan-t5-small",
        ]
        
    def load_token(self):
        """Carrega o token do Hugging Face do arquivo .env"""
        try:
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        if line.startswith('HUGGINGFACE_TOKEN='):
                            return line.split('=')[1].strip()
        except:
            pass
        return None
    
    @st.cache_data(show_spinner=False, ttl=300)
    def _hf_cached_call(model: str, token: str, prompt: str, params: dict):
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {"inputs": prompt, "parameters": params}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            return resp.status_code, resp.json()
        except Exception as e:
            return 599, {"error": str(e)}
    
    def retrieve_local_context(self, question: str, max_chars: int = 1200) -> str:
        """Busca trechos relevantes em arquivos .md do projeto (RAG simples sem custo)."""
        try:
            paths = glob.glob("*.md") + glob.glob("pages/*.md")
            question_l = question.lower()
            tokens = [t for t in re.split(r"[^\wáéíóúãõç]+", question_l) if len(t) > 2]
            if not tokens:
                return ""
            snippets: List[Tuple[int, str]] = []
            for p in paths:
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # Pontuar por ocorrência de palavras da pergunta
                    score = sum(content.lower().count(tok) for tok in tokens)
                    if score > 0:
                        # Limitar tamanho
                        snippets.append((score, content[:max_chars]))
                except Exception:
                    continue
            snippets.sort(reverse=True, key=lambda x: x[0])
            joined = "\n\n".join(s for _, s in snippets[:2])
            return joined
        except Exception:
            return ""
    
    def build_prompt(self, question: str) -> str:
        context = self.retrieve_local_context(question)
        sys_instr = (
            "Você é um assistente conciso e factual. Se a pergunta for sobre os dados locais, "
            "explique que a resposta foi calculada com base nos dados carregados. Não invente fatos."
        )
        base = f"Instruções: {sys_instr}\n\nPergunta: {question}\n"
        if context:
            base += f"\nContexto útil (documentação local):\n{context}\n"
        base += "\nResponda em português, em até 6 linhas."
        return base
    
    # =======================
    # Fuzzy matching utilitários (sem custo)
    # =======================
    @staticmethod
    def _normalize_text(s: str) -> str:
        txt = (s or "").strip().lower()
        # remover espaços extras e caracteres não alfanuméricos para facilitar match (ex.: 'Type 06' -> 'type06')
        txt = re.sub(r"[^a-z0-9]+", "", txt)
        return txt

    def _fuzzy_match_value(self, series: pd.Series, query_text: str) -> Tuple[str, float]:
        """Retorna (melhor_valor, score) usando contains e difflib. Score 0..1"""
        q = self._normalize_text(query_text)
        if not q:
            return "", 0.0
        # contains rápido
        values = series.dropna().astype(str).unique().tolist()
        norm_vals = [self._normalize_text(v) for v in values]
        best = ("", 0.0)
        for orig, norm in zip(values, norm_vals):
            if q in norm:
                score = 1.0 if q == norm else 0.85
                if score > best[1]:
                    best = (orig, score)
        # difflib fallback
        if best[1] < 0.8:
            candidates = difflib.get_close_matches(q, norm_vals, n=3, cutoff=0.55)
            for cand in candidates:
                idx = norm_vals.index(cand)
                score = difflib.SequenceMatcher(a=q, b=cand).ratio()
                if score > best[1]:
                    best = (values[idx], score)
        return best

    def _extract_free_text(self, question: str, hint_keywords: List[str]) -> str:
        """Extrai um possível valor (entre aspas ou após a keyword)."""
        # 1) trecho entre aspas
        m = re.findall(r'"([^"]+)"|\'([^\']+)\'', question)
        if m:
            for a, b in m:
                val = a or b
                if len(val.strip()) >= 3:
                    return val.strip()
        # 2) após a keyword
        ql = question.lower()
        for kw in hint_keywords:
            pos = ql.rfind(kw)
            if pos != -1:
                tail = question[pos+len(kw):].strip(" :.-\n\t")
                # pegar 1 a 5 palavras
                words = tail.split()
                val = " ".join(words[:5])
                if len(val) >= 3:
                    return val
        return ""

    def apply_fuzzy_filters(self, question: str) -> Tuple[pd.DataFrame, List[str]]:
        """Aplica filtros fuzzy com base no texto. Retorna df_filtrado e notas."""
        df_q = self.df.copy()
        notas: List[str] = []
        col_map = {
            'fornecedor': 'Nome do fornecedor',
            'supplier': 'Nome do fornecedor',
            'empresa': 'Nome do fornecedor',
            'usi': 'USI', 'usina': 'USI', 'planta': 'USI',
            'type 07': 'Type 07', 'type07': 'Type 07', 'tipo 07': 'Type 07',
            'type 06': 'Type 06', 'type06': 'Type 06', 'tipo 06': 'Type 06',
            'type 05': 'Type 05', 'type05': 'Type 05', 'tipo 05': 'Type 05',
            'oficina': 'Oficina',
            'conta': 'Nº conta', 'nº conta': 'Nº conta',
            'centro cst': 'Centro cst',
        }
        # detectar coluna alvo a partir da pergunta
        ql = question.lower()
        for kw, col in col_map.items():
            if col in df_q.columns and kw in ql:
                free = self._extract_free_text(question, [kw])
                if not free:
                    # se não houver nome, não filtra
                    continue
                best, score = self._fuzzy_match_value(df_q[col].astype(str), free)
                if score >= 0.55 and best:
                    df_q = df_q[df_q[col].astype(str).str.lower() == str(best).lower()]
                    notas.append(f"Filtro aproximado em `{col}` = '{best}' (similaridade {score:.0%})")
        return df_q, notas

    # =======================
    # Resolução de colunas por similaridade
    # =======================
    def resolve_column(self, preferred_names: List[str]) -> Tuple[str, float]:
        """Encontra a coluna mais próxima dentre preferred_names e nomes do df. Retorna (coluna, score)."""
        cols = [str(c) for c in self.df.columns]
        # 1) match direto/contains
        for pref in preferred_names:
            for c in cols:
                if self._normalize_text(pref) == self._normalize_text(c):
                    return c, 1.0
        for pref in preferred_names:
            for c in cols:
                if self._normalize_text(pref) in self._normalize_text(c):
                    return c, 0.9
        # 2) difflib
        best = ("", 0.0)
        for pref in preferred_names:
            matches = difflib.get_close_matches(self._normalize_text(pref), [self._normalize_text(c) for c in cols], n=1, cutoff=0.55)
            if matches:
                m = matches[0]
                # encontra original
                for c in cols:
                    if self._normalize_text(c) == m:
                        score = difflib.SequenceMatcher(a=self._normalize_text(pref), b=m).ratio()
                        if score > best[1]:
                            best = (c, score)
        return best

    # =======================
    # Ajuste automático das configs do Waterfall a partir da pergunta
    # =======================
    def _closest_period(self, val_str: str, periods_available: list):
        try:
            target = float(str(val_str).replace(',', '.').strip())
            pairs = []
            for p in periods_available:
                try:
                    pairs.append((abs(float(str(p)) - target), p))
                except Exception:
                    continue
            if pairs:
                pairs.sort(key=lambda x: x[0])
                return pairs[0][1]
        except Exception:
            pass
        # fallback: string exata se existir
        for p in periods_available:
            if str(p) == str(val_str):
                return p
        return None

    def update_waterfall_config_from_question(self, question: str):
        ql = question.lower()
        changed_msgs = []
        # Categoria
        cat_map = {
            'type 07': 'Type 07', 'type07': 'Type 07', 'tipo 07': 'Type 07',
            'type 06': 'Type 06', 'type06': 'Type 06', 'tipo 06': 'Type 06',
            'type 05': 'Type 05', 'type05': 'Type 05', 'tipo 05': 'Type 05',
            'fornecedor': 'Nome do fornecedor', 'fornecedores': 'Nome do fornecedor',
            'usi': 'USI', 'usina': 'USI', 'planta': 'USI',
            'oficina': 'Oficina'
        }
        for k, lbl in [('type 07','Type 07'), ('type 06','Type 06'), ('type 05','Type 05'), ('fornecedor','Fornecedor'), ('usi','USI'), ('oficina','Oficina')]:
            if k in ql:
                # map para label da sidebar
                label_sidebar = lbl if lbl in ['Type 07','Type 06','Type 05','USI','Oficina'] else 'Fornecedor'
                st.session_state['ia_wf_cat_label'] = label_sidebar
                changed_msgs.append(f"categoria={label_sidebar}")
                break
        # Top K
        m = re.search(r'top\s+(\d+)', ql)
        if not m:
            m = re.search(r'(\d+)\s+maiores', ql)
        if m:
            try:
                topk = max(3, min(20, int(m.group(1))))
                st.session_state['ia_wf_topk'] = topk
                changed_msgs.append(f"top={topk}")
            except Exception:
                pass
        # Outros
        if 'sem outros' in ql or 'sem “outros”' in ql or 'sem "outros"' in ql:
            st.session_state['ia_wf_outros'] = False
            changed_msgs.append("outros=off")
        elif 'com outros' in ql or 'incluir outros' in ql:
            st.session_state['ia_wf_outros'] = True
            changed_msgs.append("outros=on")
        # Períodos
        periods_available = sorted(self.df['Período'].dropna().unique().tolist())
        pm = re.search(r'entre\s+([0-9.,]+)\s+e\s+([0-9.,]+)', ql)
        if not pm:
            pm = re.search(r'([0-9.,]+)\s*(?:->|→|a|até|para)\s*([0-9.,]+)', ql)
        if pm and len(periods_available) >= 2:
            p1_c = self._closest_period(pm.group(1), periods_available)
            p2_c = self._closest_period(pm.group(2), periods_available)
            if p1_c is not None and p2_c is not None and str(p1_c) != str(p2_c):
                st.session_state['ia_wf_p1'] = p1_c
                st.session_state['ia_wf_p2'] = p2_c
                changed_msgs.append(f"períodos={p1_c}→{p2_c}")
        if changed_msgs:
            st.info("⚙️ Config. Waterfall ajustada: " + ", ".join(changed_msgs))
    
    def query_huggingface(self, text):
        """Consulta a API do Hugging Face para análise de texto (com fallback e cache)"""
        if not self.huggingface_token:
            return None
        prompt = self.build_prompt(text)
        params = {"max_new_tokens": 256, "temperature": 0.3}
        for model in self.hf_models:
            status, data = self._hf_cached_call(model, self.huggingface_token, prompt, params)
            if status == 200 and isinstance(data, list) and data:
                # Respostas de text2text vêm como lista de dicts com 'generated_text'
                generated = data[0].get('generated_text') or data[0].get('summary_text')
                if generated:
                    return generated
            # Retentativa rápida se 429/5xx: tentar fallback
            continue
        return None
    
    def analyze_question(self, question):
        """Analisa a pergunta do usuário"""
        question_lower = question.lower()
        
        # Detectar tipo de análise
        analysis_type = "ranking"
        entities = {}
        limit = None
        
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
        
        # Detectar períodos em forma de faixa (sinaliza intenção de variação)
        faixa_match = re.search(r'entre\s*([0-9.,]+)\s*(?:e|a|até|para)\s*([0-9.,]+)', question_lower)
        seta_match = re.search(r'([0-9.,]+)\s*(?:->|→)\s*([0-9.,]+)', question_lower)
        if faixa_match or seta_match:
            entities['waterfall_intent'] = True
        
        # PRIORIDADE 1: Detectar análise temporal (prioridade MÁXIMA)
        temporal_phrases = ['cada mês', 'por mês', 'valor total de cada mês', 'total de cada mês', 'mensal', 'mês a mês', 'mes a mes', 'valor total mes a mes', 'valor total por período', 'por período', 'total por período', 'evolução temporal', 'crescimento temporal']
        if any(phrase in question_lower for phrase in temporal_phrases):
            analysis_type = "temporal"
            entities['periodo'] = True
        elif any(word in question_lower for word in ['temporal', 'tempo', 'evolução', 'crescimento', 'tendência']):
            analysis_type = "temporal"
            entities['periodo'] = True
            
        # Detectar Type 07 (prioridade alta)
        if any(word in question_lower for word in ['type 07', 'type07', 'type_07', 'tipo 07', 'tipo07', 'type7', 'tipo 7']):
            entities['type_07'] = True
            
        # Detectar Type 05
        if any(word in question_lower for word in ['type 05', 'type05', 'type_05', 'tipo 05', 'tipo05', 'type5', 'tipo 5']):
            entities['type_05'] = True
            
        # Detectar Type 06
        if any(word in question_lower for word in ['type 06', 'type06', 'type_06', 'tipo 06', 'tipo06', 'type6', 'tipo 6']):
            entities['type_06'] = True
            
        # Detectar USI
        if any(word in question_lower for word in ['usi', 'usina', 'planta']):
            entities['usi'] = True
            
        # Detectar fornecedor
        if any(word in question_lower for word in ['fornecedor', 'fornecedores', 'supplier', 'empresa', 'nome do fornecedor']):
            entities['fornecedor'] = True
            
        # Detectar conta
        if any(word in question_lower for word in ['conta', 'account', 'número', 'nº conta']):
            entities['conta'] = True
            
        # Detectar valor
        if any(word in question_lower for word in ['valor', 'value', 'total', 'soma', 'somar']):
            entities['valor'] = True
            
        # Detectar oficina
        if any(word in question_lower for word in ['oficina', 'workshop']):
            entities['oficina'] = True
            
        # Detectar centro cst
        if any(word in question_lower for word in ['centro cst', 'centro', 'cst']):
            entities['centro_cst'] = True
            
        # Detectar agregação média
        if any(word in question_lower for word in ['média', 'media', 'average', 'avg']):
            entities['agg'] = 'mean'
            
        # PRIORIDADE 3: Detectar outros tipos de análise
        # Detectar comparação
        if any(word in question_lower for word in ['comparar', 'comparação', 'diferença', 'vs', 'versus']):
            analysis_type = "comparison"
            
        # Detectar waterfall (ou intenção de variação entre períodos)
        if any(word in question_lower for word in ['waterfall', 'cascata', 'variação', 'variacao']):
            analysis_type = "waterfall"
        if entities.get('waterfall_intent'):
            analysis_type = "waterfall"
            
        return {
            'type': analysis_type,
            'entities': entities,
            'original_question': question,
            'limit': limit
        }
    
    def generate_sql_query(self, analysis):
        """Gera query SQL baseada na análise"""
        query = "SELECT "
        
        # Verificação adicional: se a pergunta contém frases temporais, forçar temporal
        question_lower = analysis['original_question'].lower()
        temporal_phrases = ['cada mês', 'por mês', 'valor total de cada mês', 'mes a mes', 'valor total mes a mes', 'mensal', 'valor total por período', 'por período', 'total por período']
        
        if any(phrase in question_lower for phrase in temporal_phrases):
            analysis['type'] = 'temporal'
            analysis['entities']['periodo'] = True
        
        if analysis['type'] == 'ranking':
            # Priorizar colunas específicas detectadas
            if 'type_07' in analysis['entities']:
                col, sc = self.resolve_column(['Type 07','Type07','Tipo 07'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Type 07, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'type_05' in analysis['entities']:
                col, sc = self.resolve_column(['Type 05','Type05','Tipo 05','Type5','Tipo 5','type 05','type05'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Type 05, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'type_06' in analysis['entities']:
                col, sc = self.resolve_column(['Type 06','Type06','Tipo 06','Type6','Tipo 6','type 06','type06'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Type 06, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'oficina' in analysis['entities']:
                col, sc = self.resolve_column(['Oficina'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Oficina, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'centro_cst' in analysis['entities']:
                col, sc = self.resolve_column(['Centro cst','Centro','CST'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Centro cst, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'fornecedor' in analysis['entities']:
                col, sc = self.resolve_column(['Nome do fornecedor','Fornecedor'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Fornecedor, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'conta' in analysis['entities']:
                col, sc = self.resolve_column(['Nº conta','Conta','Numero conta'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (Conta, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'usi' in analysis['entities']:
                col, sc = self.resolve_column(['USI','Usina','Planta'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (USI, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
            elif 'periodo' in analysis['entities']:
                query += "`Período`, SUM(Valor) as total_valor FROM df GROUP BY `Período` ORDER BY total_valor DESC"
            else:
                # fallback
                col, sc = self.resolve_column(['USI','Nome do fornecedor','Type 07','Type 06','Type 05'])
                if col:
                    col_sql = f"`{col}`" if (" " in col or not col.isidentifier()) else col
                    query += f"{col_sql}, SUM(Valor) as total_valor FROM df GROUP BY {col_sql} ORDER BY total_valor DESC"
                    st.info(f"📎 Coluna escolhida: `{col}` (fallback, similaridade {sc:.0%})")
                else:
                    query += "USI, SUM(Valor) as total_valor FROM df GROUP BY USI ORDER BY total_valor DESC"
                
        elif analysis['type'] == 'temporal':
            # Para análise temporal, SEMPRE usar Período - não importa outras entidades
            query += "`Período`, SUM(Valor) as total_valor FROM df GROUP BY `Período` ORDER BY `Período`"
            
        elif analysis['type'] == 'waterfall':
            query += "`Período`, SUM(Valor) as total_valor FROM df GROUP BY `Período` ORDER BY `Período`"
            
        else:
            # agregação padrão
            if analysis.get('agg') == 'mean':
                query += "AVG(Valor) as total_valor FROM df"
            else:
                query += "SUM(Valor) as total_valor FROM df"
            
        return query
    
    def execute_query(self, query, limit=None):
        """Executa a query SQL"""
        try:
            # Substituir 'df' por 'self.df' na query
            query = query.replace('FROM df', 'FROM self.df')
            
            # Executar query usando pandas
            if 'GROUP BY' in query:
                # Caminho genérico: detectar coluna após SELECT ... GROUP BY <col>
                m = re.search(r"SELECT\s+([^,]+),\s*SUM\(Valor\).*GROUP BY\s+([^\s]+)", query, flags=re.IGNORECASE)
                if m:
                    col = m.group(2).strip()
                    col = col.strip('`')
                    if col in self.df.columns:
                        result = self.df.groupby(col)['Valor'].sum().reset_index()
                        result.columns = [col, 'total_valor']
                        result = result.sort_values('total_valor', ascending=False).reset_index(drop=True)
                        if limit and not result.empty:
                            result = result.head(limit)
                        return result
                if 'SUM(Valor)' in query:
                    # Query de agregação conhecida
                    if '`Type 07`' in query:
                        result = self.df.groupby('Type 07')['Valor'].sum().reset_index()
                        result.columns = ['Type 07', 'total_valor']
                    elif '`Type 05`' in query:
                        result = self.df.groupby('Type 05')['Valor'].sum().reset_index()
                        result.columns = ['Type 05', 'total_valor']
                    elif '`Type 06`' in query:
                        result = self.df.groupby('Type 06')['Valor'].sum().reset_index()
                        result.columns = ['Type 06', 'total_valor']
                    elif 'Oficina' in query:
                        result = self.df.groupby('Oficina')['Valor'].sum().reset_index()
                        result.columns = ['Oficina', 'total_valor']
                    elif '`Centro cst`' in query:
                        result = self.df.groupby('Centro cst')['Valor'].sum().reset_index()
                        result.columns = ['Centro cst', 'total_valor']
                    elif '`Nome do fornecedor`' in query:
                        result = self.df.groupby('Nome do fornecedor')['Valor'].sum().reset_index()
                        result.columns = ['Nome do fornecedor', 'total_valor']
                    elif '`Nº conta`' in query:
                        result = self.df.groupby('Nº conta')['Valor'].sum().reset_index()
                        result.columns = ['Nº conta', 'total_valor']
                    elif 'USI' in query:
                        result = self.df.groupby('USI')['Valor'].sum().reset_index()
                        result.columns = ['USI', 'total_valor']
                    elif 'Período' in query:
                        result = self.df.groupby('Período')['Valor'].sum().reset_index()
                        result.columns = ['Período', 'total_valor']
                    else:
                        result = pd.DataFrame()
                    
                    # Ordenar por valor decrescente
                    if not result.empty:
                        result = result.sort_values('total_valor', ascending=False).reset_index(drop=True)
                    
                    # Aplicar limite se especificado
                    if limit and not result.empty:
                        result = result.head(limit)
                else:
                    result = pd.DataFrame()
            else:
                # Query simples
                if 'SUM(Valor)' in query:
                    total = self.df['Valor'].sum()
                    result = pd.DataFrame({'total_valor': [total]})
                elif 'AVG(Valor)' in query:
                    avg = self.df['Valor'].mean()
                    result = pd.DataFrame({'total_valor': [avg]})
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
                # Fallback: garantir até 20 barras para visualização
                dfv = data.copy()
                try:
                    # garantir ordenação decrescente pelo valor
                    dfv = dfv.sort_values(col2, ascending=False).head(20)
                except Exception:
                    pass
                # ordenar e usar barras verticais em ordem decrescente
                dfv[col1] = dfv[col1].astype(str)
                ordered_labels = dfv[col1].tolist()
                dfv[col2] = pd.to_numeric(dfv[col2], errors='coerce').fillna(0)
                fig = px.bar(dfv, x=col1, y=col2, title=f"Ranking por {col1}")
                # forçar a ordem do eixo X conforme o DataFrame ordenado (maiores à esquerda)
                fig.update_xaxes(categoryorder='array', categoryarray=list(ordered_labels))
                fig.update_layout(
                    xaxis_tickangle=-45,
                    xaxis_title=col1,
                    yaxis_title="Valor Total (R$)",
                    showlegend=False
                )
                fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
                return fig
                
        elif analysis['type'] == 'temporal':
            if len(data.columns) >= 2:
                col1 = data.columns[0]
                col2 = data.columns[1]
                fig = px.line(data, x=col1, y=col2, title="Evolução Temporal")
                fig.update_layout(
                    xaxis_title=col1,
                    yaxis_title="Valor Total (R$)"
                )
                return fig
                
        elif analysis['type'] == 'waterfall':
            # Implementação: waterfall de finanças (2 períodos) usando configurações da sidebar
            try:
                df_ref = self.df.copy()
                # Categoria da sidebar
                cat_label = st.session_state.get('ia_wf_cat_label')
                label_to_col_map = {
                    'Type 07': 'Type 07',
                    'Type 06': 'Type 06',
                    'Type 05': 'Type 05',
                    'Fornecedor': 'Nome do fornecedor',
                    'USI': 'USI',
                    'Oficina': 'Oficina'
                }
                cat_col = label_to_col_map.get(cat_label)
                if not cat_col or cat_col not in df_ref.columns:
                    # fallback automático
                    for lbl, col in label_to_col_map.items():
                        if col in df_ref.columns:
                            cat_col, cat_label = col, lbl
                            break
                df_ref[cat_col] = df_ref[cat_col].fillna('Sem categoria')

                # Períodos selecionados
                periods_available = sorted(df_ref['Período'].dropna().unique().tolist())
                if len(periods_available) < 2:
                    return None
                p1 = st.session_state.get('ia_wf_p1', periods_available[-2])
                p2 = st.session_state.get('ia_wf_p2', periods_available[-1])
                # Garantir ordem temporal
                ordem = {v: i for i, v in enumerate(periods_available)}
                if ordem[p1] > ordem[p2]:
                    p1, p2 = p2, p1

                # TopK e Outros
                top_k = int(st.session_state.get('ia_wf_topk', 10))
                incluir_outros = bool(st.session_state.get('ia_wf_outros', True))

                base = df_ref.groupby(['Período', cat_col])['Valor'].sum().reset_index()
                df_p1 = base[base['Período'] == p1].set_index(cat_col)['Valor']
                df_p2 = base[base['Período'] == p2].set_index(cat_col)['Valor']
                all_cats = df_p1.index.union(df_p2.index)
                v1 = df_p1.reindex(all_cats, fill_value=0)
                v2 = df_p2.reindex(all_cats, fill_value=0)
                delta = (v2 - v1).to_frame('delta').reset_index().rename(columns={cat_col: cat_col})
                delta['abs'] = delta['delta'].abs()

                principais = delta.sort_values('abs', ascending=False).head(top_k)
                if incluir_outros and len(delta) > top_k:
                    outros_val = delta.sort_values('abs', ascending=False).iloc[top_k:]['delta'].sum()
                    if outros_val != 0:
                        principais = pd.concat([principais, pd.DataFrame({cat_col: ['Outros (agr.)'], 'delta': [outros_val], 'abs': [abs(outros_val)]})], ignore_index=True)

                # Estatísticas para narrativa
                total_p1 = float(v1.sum())
                total_p2 = float(v2.sum())
                delta_total = total_p2 - total_p1
                pos = principais.sort_values('delta', ascending=False).iloc[0]
                neg = principais.sort_values('delta', ascending=True).iloc[0]
                st.session_state['ia_wf_stats'] = {
                    'cat_label': cat_label,
                    'p1': p1,
                    'p2': p2,
                    'total_p1': total_p1,
                    'total_p2': total_p2,
                    'delta_total': float(delta_total),
                    'top_pos_name': str(pos[cat_col]),
                    'top_pos_value': float(pos['delta']),
                    'top_neg_name': str(neg[cat_col]),
                    'top_neg_value': float(neg['delta'])
                }

                labels = [f'Total {p1}'] + principais[cat_col].astype(str).tolist() + [f'Total {p2}']
                measures = ['absolute'] + ['relative'] * len(principais) + ['total']
                values = [v1.sum()] + principais['delta'].tolist() + [0]
                texts = [f"R$ {v1.sum():,.0f}"] + [f"R$ {x:,.0f}" for x in principais['delta'].tolist()] + [f"R$ {v2.sum():,.0f}"]

                fig = go.Figure(go.Waterfall(
                    name="Waterfall",
                    orientation="v",
                    measure=measures,
                    x=labels,
                    y=values,
                    text=texts,
                    textposition='outside',
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "#2E8B57"}},
                    decreasing={"marker": {"color": "#DC143C"}},
                    totals={"marker": {"color": "#4682B4"}}
                ))
                fig.update_layout(
                    title=f"Análise Waterfall - {cat_label} | Períodos: {p1} → {p2}",
                    xaxis_title="Período / Categorias",
                    yaxis_title="Valor (R$)"
                )
                fig.update_yaxes(tickformat=",.0f", tickprefix="R$ ")
                return fig
            except Exception:
                return None
                
        return None
    
    def generate_response(self, analysis, data):
        """Gera resposta textual"""
        if data.empty and analysis['type'] not in {'waterfall'}:
            return "❌ Não foi possível encontrar dados para sua pergunta. Tente reformular sua pergunta ou verifique se os dados estão carregados."
            
        # Cabeçalho
        response = f"📊 **Análise: {analysis['type'].title()}**\n\n"
        
        # Adicionar informação sobre limite se aplicável
        if analysis.get('limit'):
            response += f"🔢 **Mostrando:** Top {analysis['limit']} resultados\n\n"
        
        if analysis['type'] == 'ranking':
            if len(data) > 0:
                value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                top_item = data.iloc[0]
                total_sum = data[value_col].sum()
                share = (top_item[value_col] / total_sum) if total_sum != 0 else 0
                response += (
                    f"🏆 Top 1: **{top_item.iloc[0]}** — R$ {top_item[value_col]:,.2f} "
                    f"({share:,.1%} do total mostrado).\n"
                    f"💰 Total dos itens: **R$ {total_sum:,.2f}**\n"
                    f"🧭 Sugestão: explore os itens 2 a 10 ou filtre por período/categoria para entender concentrações."
                )
        elif analysis['type'] == 'temporal':
            if len(data) > 1:
                value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                first = data.iloc[0]
                last = data.iloc[-1]
                delta = last[value_col] - first[value_col]
                pct = (delta / first[value_col]) if first[value_col] != 0 else 0
                response += (
                    f"📅 Períodos analisados: {len(data)} | Primeiro: **{first.iloc[0]}**, Último: **{last.iloc[0]}**\n"
                    f"🔄 Variação acumulada: **R$ {delta:,.2f}** ({pct:,.1%})\n"
                    f"💡 Sugestão: gere um waterfall entre {first.iloc[0]} e {last.iloc[0]} ou detalhe por Type 07/Fornecedor."
                )
        elif analysis['type'] == 'waterfall':
            # Usar estatísticas calculadas na criação do gráfico
            stats = st.session_state.get('ia_wf_stats')
            if stats:
                total_p1 = stats['total_p1']
                total_p2 = stats['total_p2']
                delta_total = stats['delta_total']
                pct = (delta_total / total_p1) if total_p1 != 0 else 0
                response += (
                    f"🧮 Total {stats['p1']}: **R$ {total_p1:,.2f}** → Total {stats['p2']}: **R$ {total_p2:,.2f}**\n"
                    f"🔀 Variação líquida: **R$ {delta_total:,.2f}** ({pct:,.1%})\n"
                    f"📈 Maior alta: **{stats['top_pos_name']}** (+R$ {stats['top_pos_value']:,.2f}) | "
                    f"📉 Maior queda: **{stats['top_neg_name']}** (R$ {stats['top_neg_value']:,.2f})\n"
                    f"💡 Sugestões: aumente/diminua o Top K, troque a categoria (Type 07/Fornecedor/USI) ou altere os dois períodos para isolar eventos."
                )
            else:
                # Fallback com totals da consulta por período
                if len(data) > 1:
                    value_col = 'total_valor' if 'total_valor' in data.columns else data.columns[1]
                    first = data.iloc[0]
                    last = data.iloc[-1]
                    delta = last[value_col] - first[value_col]
                    pct = (delta / first[value_col]) if first[value_col] != 0 else 0
                    response += (
                        f"🧮 Total inicial: **R$ {first[value_col]:,.2f}** → Total final: **R$ {last[value_col]:,.2f}**\n"
                        f"🔀 Variação líquida: **R$ {delta:,.2f}** ({pct:,.1%})\n"
                    )
        else:
            # Para respostas puramente IA, só garantir concisão
            pass
                
        return response
    
    def process_question(self, question):
        """Processa a pergunta completa"""
        # Analisar pergunta
        analysis = self.analyze_question(question)
        
        # Debug: mostrar análise detectada
        st.info(f"🔍 **Análise detectada:** {analysis['type']} | **Entidades:** {list(analysis['entities'].keys())}")
        if analysis.get('limit'):
            st.info(f"🔢 **Limite detectado:** Top {analysis['limit']}")
        
        notas = []
        # Filtros fuzzy por valor de coluna (ex.: fornecedor parecido)
        df_backup = self.df
        try:
            df_fuzzy, notas = self.apply_fuzzy_filters(question)
            if not df_fuzzy.empty and len(df_fuzzy) < len(self.df):
                self.df = df_fuzzy
                if notas:
                    for n in notas:
                        st.info(f"🔎 {n}")
        except Exception:
            pass
        
        # Ajuste Waterfall (se houver pistas mesmo fora do tipo)
        try:
            self.update_waterfall_config_from_question(question)
        except Exception:
            pass
        
        # Rotear
        if analysis['type'] in {"ranking", "temporal", "waterfall"}:
            query = self.generate_sql_query(analysis)
            st.info(f"📝 **Query gerada:** {query}")
            data = self.execute_query(query, analysis.get('limit'))
            viz = self.create_visualization(data, analysis)
            response = self.generate_response(analysis, data)
        else:
            generated = self.query_huggingface(question)
            if not generated:
                generated = "❌ Não consegui gerar uma resposta agora. Tente reformular a pergunta."
            data = pd.DataFrame()
            viz = None
            response = generated
        
        # Restaurar df completo
        self.df = df_backup
        
        return {
            'response': response,
            'visualization': viz,
            'data': data,
            'analysis': analysis
        }

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

# Filtro 2: Período
periodo_opcoes = ["Todos"] + sorted(df_filtrado['Período'].dropna().unique().tolist())
periodo_selecionado = st.sidebar.selectbox("Selecione o Período:", periodo_opcoes)

# Aplicar filtro de Período
if periodo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Período'] == periodo_selecionado]

# Filtro 3: Centro cst
centro_cst_opcoes = ["Todos"] + sorted(df_filtrado['Centro cst'].dropna().unique().tolist())
centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)

# Aplicar filtro de Centro cst
if centro_cst_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Centro cst'] == centro_cst_selecionado]

# Filtro 4: Conta contabil
conta_contabil_opcoes = ["Todas"] + sorted(df_filtrado['Nº conta'].dropna().unique().tolist())
conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contabil:", conta_contabil_opcoes)

# Aplicar filtro de Conta contabil
if conta_contabil_selecionadas and "Todas" not in conta_contabil_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Nº conta'].isin(conta_contabil_selecionadas)]

# Mostrar estatísticas dos filtros
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Estatísticas")
st.sidebar.write(f"**Registros:** {len(df_filtrado):,}")
st.sidebar.write(f"**Valor Total:** R$ {df_filtrado['Valor'].sum():,.2f}")
st.sidebar.write(f"**USIs:** {df_filtrado['USI'].nunique()}")
st.sidebar.write(f"**Períodos:** {df_filtrado['Período'].nunique()}")

# Configurações específicas para o Waterfall (IUD)
with st.sidebar.expander("⚙️ Configuração Waterfall (IUD)"):
    # Categoria disponível
    cat_options = []
    if 'Type 07' in df_filtrado.columns:
        cat_options.append(('Type 07', 'Type 07'))
    if 'Type 06' in df_filtrado.columns:
        cat_options.append(('Type 06', 'Type 06'))
    if 'Type 05' in df_filtrado.columns:
        cat_options.append(('Type 05', 'Type 05'))
    if 'Nome do fornecedor' in df_filtrado.columns:
        cat_options.append(('Fornecedor', 'Nome do fornecedor'))
    if 'USI' in df_filtrado.columns:
        cat_options.append(('USI', 'USI'))
    if 'Oficina' in df_filtrado.columns:
        cat_options.append(('Oficina', 'Oficina'))

    if cat_options:
        label_to_col = {label: col for label, col in cat_options}
        default_label = list(label_to_col.keys())[0]
        default_idx = list(label_to_col.keys()).index(st.session_state.get('ia_wf_cat_label', default_label)) if st.session_state.get('ia_wf_cat_label') in label_to_col else 0
        st.selectbox(
            "Categoria para decompor:",
            options=list(label_to_col.keys()),
            index=default_idx,
            key='ia_wf_cat_label'
        )
        st.slider("Top categorias", 3, 20, st.session_state.get('ia_wf_topk', 10), 1, key='ia_wf_topk')
        st.checkbox("Incluir 'Outros'", value=st.session_state.get('ia_wf_outros', True), key='ia_wf_outros')
        # Seleção de dois períodos
        periods_available = sorted(df_filtrado['Período'].dropna().unique().tolist())
        if len(periods_available) >= 2:
            default_p1 = st.session_state.get('ia_wf_p1', periods_available[-2])
            default_p2 = st.session_state.get('ia_wf_p2', periods_available[-1])
            cols_p = st.columns(2)
            with cols_p[0]:
                st.selectbox("Período origem", periods_available, index=periods_available.index(default_p1) if default_p1 in periods_available else len(periods_available)-2, key='ia_wf_p1')
            with cols_p[1]:
                # evitar mesmo período
                p1_current = st.session_state.get('ia_wf_p1', default_p1)
                options_p2 = [p for p in periods_available if p != p1_current]
                default_idx_p2 = options_p2.index(default_p2) if default_p2 in options_p2 else len(options_p2)-1
                st.selectbox("Período destino", options_p2, index=default_idx_p2, key='ia_wf_p2')

# Inicializar assistente com dados filtrados
assistant = AIAssistant(df_filtrado)

# Interface do chat
st.subheader("💬 Chat com IUD")


# Sugestões rápidas (chips)
with st.container():
    cols = st.columns(4)
    if cols[0].button("Waterfall Type 07 (últimos 2)"):
        prompt = "Crie um gráfico waterfall por Type 07"
        st.session_state.chat_history.append(prompt)
        with st.spinner("🤖 Analisando sua pergunta..."):
            result = assistant.process_question(prompt)
        st.session_state.chat_history.append(result['response'])
        st.session_state['last_result'] = result
        st.rerun()
    if cols[1].button("Top 10 Fornecedores"):
        prompt = "Top 10 maiores fornecedores"
        st.session_state.chat_history.append(prompt)
        with st.spinner("🤖 Analisando sua pergunta..."):
            result = assistant.process_question(prompt)
        st.session_state.chat_history.append(result['response'])
        st.session_state['last_result'] = result
        st.rerun()
    if cols[2].button("Evolução por Período"):
        prompt = "Mostrar evolução temporal dos valores por período"
        st.session_state.chat_history.append(prompt)
        with st.spinner("🤖 Analisando sua pergunta..."):
            result = assistant.process_question(prompt)
        st.session_state.chat_history.append(result['response'])
        st.session_state['last_result'] = result
        st.rerun()
    if cols[3].button("Resumo dos dados"):
        prompt = "Faça um resumo dos dados carregados"
        st.session_state.chat_history.append(prompt)
        with st.spinner("🤖 Analisando sua pergunta..."):
            result = assistant.process_question(prompt)
        st.session_state.chat_history.append(result['response'])
        st.session_state['last_result'] = result
        st.rerun()

# Exibir histórico do chat
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message("user" if i % 2 == 0 else "assistant"):
        if i % 2 == 0:
            st.write(message)
        else:
            st.write(message)

# Exibir último resultado gerado por botão, se existir
if st.session_state.get('last_result') is not None:
    lr = st.session_state.get('last_result')
    with st.chat_message("assistant"):
        st.write(lr['response'])
        if lr['visualization'] is not None:
            st.subheader("📊 Gráfico")
            st.plotly_chart(lr['visualization'], use_container_width=True)
        elif hasattr(lr, 'get') and lr.get('visualization') is None:
            st.warning("⚠️ Não foi possível gerar visualização para estes dados")
        if 'data' in lr and isinstance(lr['data'], pd.DataFrame) and not lr['data'].empty:
            st.subheader("📊 Dados Detalhados")
            st.dataframe(lr['data'], use_container_width=True)
    # limpar para evitar repetição em novos reruns
    st.session_state.pop('last_result', None)

# Input para nova pergunta
if prompt := st.chat_input("Digite sua pergunta sobre os dados..."):
    # Adicionar pergunta ao histórico
    st.session_state.chat_history.append(prompt)
    
    # Processar pergunta
    with st.spinner("🤖 Analisando sua pergunta..."):
        result = assistant.process_question(prompt)
    
    # Adicionar resposta ao histórico
    st.session_state.chat_history.append(result['response'])
    
    # Exibir resposta
    with st.chat_message("assistant"):
        st.write(result['response'])
        
        # Exibir visualização se disponível
        if result['visualization'] is not None:
            st.subheader("📊 Gráfico")
            st.plotly_chart(result['visualization'], use_container_width=True)
        else:
            st.warning("⚠️ Não foi possível gerar visualização para estes dados")
        
        # Exibir dados se disponíveis
        if not result['data'].empty:
            st.subheader("📊 Dados Detalhados")
            st.dataframe(result['data'], use_container_width=True)

# Botão para limpar chat
if st.button("🗑️ Limpar Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Informações sobre o assistente
st.markdown("---")
st.subheader("ℹ️ Sobre o IUD")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🎯 Funcionalidades:**
    - Análise de Type 07, Type 05, Type 06
    - Análise de fornecedores
    - Análise de contas
    - Análise temporal
    - Gráficos waterfall
    - Ranking de dados
    """)

with col2:
    st.markdown("""
    **💡 Exemplos de perguntas:**
    - "Top 10 maiores Type 07"
    - "20 maiores fornecedores"
    - "Top 5 contas"
    - "Evolução temporal dos valores"
    - "Crie um gráfico waterfall"
    - "15 maiores USIs"
    """)

# Status da API
if assistant.huggingface_token:
    st.success("✅ API Hugging Face configurada")
else:
    st.warning("⚠️ API Hugging Face não configurada")
    st.info("Configure o token na página 'Configurar IA'")

# Mostrar colunas disponíveis
st.markdown("---")
st.subheader("📊 Colunas Disponíveis para Análise")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🏷️ Tipos:**
    - Type 07
    - Type 05  
    - Type 06
    - Oficina
    """)

with col2:
    st.markdown("""
    **🏢 Organizacional:**
    - USI
    - Centro cst
    - Nome do fornecedor
    - Nº conta
    """)

with col3:
    st.markdown("""
    **📅 Temporal:**
    - Período
    - Ano
    - Valor
    """)
