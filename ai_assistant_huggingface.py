import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import os
from datetime import datetime

class AIAssistantHuggingFace:
    """Assistente IA integrado com Hugging Face para análise de dados"""
    
    def __init__(self, df):
        self.df = df
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
        
        # Análise local com palavras-chave
        analysis = {
            'type': 'ranking',
            'entities': {},
            'confidence': 0.5,
            'original_question': question
        }
        
        # Detectar fornecedor
        if any(word in question_lower for word in ['fornecedor', 'supplier', 'empresa', 'nome']):
            analysis['entities']['fornecedor'] = True
            analysis['confidence'] += 0.2
            
        # Detectar conta
        if any(word in question_lower for word in ['conta', 'account', 'número', 'nº']):
            analysis['entities']['conta'] = True
            analysis['confidence'] += 0.2
            
        # Detectar período
        if any(word in question_lower for word in ['período', 'period', 'mês', 'ano', 'temporal']):
            analysis['entities']['periodo'] = True
            analysis['confidence'] += 0.2
            
        # Detectar valor
        if any(word in question_lower for word in ['valor', 'value', 'total', 'soma', 'somar']):
            analysis['entities']['valor'] = True
            analysis['confidence'] += 0.2
            
        # Detectar análise temporal
        if any(word in question_lower for word in ['temporal', 'tempo', 'evolução', 'crescimento', 'tendência']):
            analysis['type'] = 'temporal'
            analysis['confidence'] += 0.3
            
        # Detectar comparação
        if any(word in question_lower for word in ['comparar', 'comparação', 'diferença', 'vs', 'versus']):
            analysis['type'] = 'comparison'
            analysis['confidence'] += 0.3
            
        # Detectar waterfall
        if any(word in question_lower for word in ['waterfall', 'cascata', 'variação', 'variações']):
            analysis['type'] = 'waterfall'
            analysis['confidence'] += 0.3
            
        # Detectar ranking/top
        if any(word in question_lower for word in ['maior', 'menor', 'top', 'ranking', 'melhor', 'pior']):
            analysis['type'] = 'ranking'
            analysis['confidence'] += 0.3
            
        # Consultar Hugging Face se disponível
        if self.huggingface_token:
            try:
                hf_response = self.query_huggingface(question)
                if hf_response and isinstance(hf_response, list) and len(hf_response) > 0:
                    # Usar resposta da IA para melhorar análise
                    analysis['ai_response'] = hf_response[0].get('generated_text', '')
                    analysis['confidence'] += 0.1
            except:
                pass
        
        return analysis
    
    def generate_sql_query(self, analysis):
        """Gera query SQL baseada na análise"""
        query_parts = ["SELECT "]
        
        if analysis['type'] == 'ranking':
            if 'fornecedor' in analysis['entities']:
                query_parts.append("`Nome do fornecedor`, SUM(Valor) as total_valor")
                query_parts.append("FROM df GROUP BY `Nome do fornecedor` ORDER BY total_valor DESC")
            elif 'conta' in analysis['entities']:
                query_parts.append("`Nº conta`, SUM(Valor) as total_valor")
                query_parts.append("FROM df GROUP BY `Nº conta` ORDER BY total_valor DESC")
            else:
                query_parts.append("USI, SUM(Valor) as total_valor")
                query_parts.append("FROM df GROUP BY USI ORDER BY total_valor DESC")
                
        elif analysis['type'] == 'temporal':
            query_parts.append("Período, SUM(Valor) as total_valor")
            query_parts.append("FROM df GROUP BY Período ORDER BY Período")
            
        elif analysis['type'] == 'waterfall':
            query_parts.append("Período, SUM(Valor) as total_valor")
            query_parts.append("FROM df GROUP BY Período ORDER BY Período")
            
        elif analysis['type'] == 'comparison':
            if 'fornecedor' in analysis['entities']:
                query_parts.append("`Nome do fornecedor`, Período, SUM(Valor) as total_valor")
                query_parts.append("FROM df GROUP BY `Nome do fornecedor`, Período ORDER BY Período, total_valor DESC")
            else:
                query_parts.append("Período, SUM(Valor) as total_valor")
                query_parts.append("FROM df GROUP BY Período ORDER BY Período")
        else:
            query_parts.append("SUM(Valor) as total_valor")
            query_parts.append("FROM df")
            
        return " ".join(query_parts)
    
    def execute_query(self, query):
        """Executa a query SQL"""
        try:
            # Substituir 'df' por 'self.df' na query
            query = query.replace('FROM df', 'FROM self.df')
            result = eval(query)
            return result
        except Exception as e:
            print(f"Erro na query: {e}")
            return pd.DataFrame()
    
    def create_waterfall_chart(self, data, title="Waterfall Chart"):
        """Cria um gráfico waterfall"""
        if data.empty or len(data) < 2:
            return None
            
        # Preparar dados para waterfall
        categories = data.iloc[:, 0].tolist()
        values = data.iloc[:, 1].tolist()
        
        # Calcular medidas para waterfall
        measures = ["absolute"] + ["relative"] * (len(values) - 1)
        
        # Criar figura waterfall
        fig = go.Figure(go.Waterfall(
            name="Waterfall",
            orientation="v",
            measure=measures,
            x=categories,
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "green"}},
            decreasing={"marker": {"color": "red"}},
            totals={"marker": {"color": "blue"}}
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=data.columns[0],
            yaxis_title=f"Soma de {data.columns[1]}",
            showlegend=False
        )
        
        return fig
    
    def create_visualization(self, data, analysis):
        """Cria visualização baseada nos dados e análise"""
        if data.empty:
            return None
            
        if analysis['type'] == 'ranking':
            if len(data.columns) == 2:
                col1, col2 = data.columns
                fig = px.bar(data, x=col1, y=col2, title=f"Ranking por {col1}")
                fig.update_layout(xaxis_tickangle=-45)
                return fig
                
        elif analysis['type'] == 'temporal':
            if len(data.columns) == 2:
                col1, col2 = data.columns
                fig = px.line(data, x=col1, y=col2, title="Evolução Temporal")
                return fig
                
        elif analysis['type'] == 'waterfall':
            return self.create_waterfall_chart(data, "Análise Waterfall")
            
        elif analysis['type'] == 'comparison':
            if len(data.columns) == 3:
                col1, col2, col3 = data.columns
                fig = px.bar(data, x=col1, y=col3, color=col2, title="Comparação")
                fig.update_layout(xaxis_tickangle=-45)
                return fig
            elif len(data.columns) == 2:
                col1, col2 = data.columns
                fig = px.bar(data, x=col1, y=col2, title="Comparação")
                fig.update_layout(xaxis_tickangle=-45)
                return fig
                
        return None
    
    def generate_response(self, analysis, data):
        """Gera resposta textual baseada na análise"""
        if data.empty:
            return "❌ Não foi possível encontrar dados para sua pergunta."
            
        response = f"📊 **Análise: {analysis['type'].title()}**\n\n"
        
        if analysis['type'] == 'ranking':
            if len(data) > 0:
                top_item = data.iloc[0]
                response += f"🏆 **Top 1:** {top_item.iloc[0]} - R$ {top_item.iloc[1]:,.2f}\n\n"
                response += f"📈 **Total de itens:** {len(data)}\n"
                response += f"💰 **Valor total:** R$ {data.iloc[:, 1].sum():,.2f}"
                
        elif analysis['type'] == 'temporal':
            if len(data) > 0:
                response += f"📅 **Períodos analisados:** {len(data)}\n"
                response += f"💰 **Valor total:** R$ {data.iloc[:, 1].sum():,.2f}\n"
                response += f"📊 **Média por período:** R$ {data.iloc[:, 1].mean():,.2f}"
                
        elif analysis['type'] == 'waterfall':
            if len(data) > 0:
                response += f"🌊 **Análise Waterfall:**\n"
                response += f"📅 **Períodos:** {len(data)}\n"
                response += f"💰 **Variação total:** R$ {data.iloc[:, 1].sum():,.2f}"
                
        elif analysis['type'] == 'comparison':
            if len(data) > 0:
                response += f"🔄 **Comparação:**\n"
                response += f"📊 **Itens comparados:** {len(data)}\n"
                response += f"💰 **Valor total:** R$ {data.iloc[:, -1].sum():,.2f}"
                
        # Adicionar resposta da IA se disponível
        if 'ai_response' in analysis and analysis['ai_response']:
            response += f"\n\n🤖 **IA:** {analysis['ai_response']}"
            
        return response
    
    def process_question(self, question):
        """Processa a pergunta completa"""
        try:
            # Analisar pergunta
            analysis = self.analyze_question(question)
            
            # Gerar query
            query = self.generate_sql_query(analysis)
            
            # Executar query
            data = self.execute_query(query)
            
            # Criar visualização
            viz = self.create_visualization(data, analysis)
            
            # Gerar resposta
            response = self.generate_response(analysis, data)
            
            return {
                'response': response,
                'visualization': viz,
                'data': data,
                'analysis': analysis,
                'query': query
            }
            
        except Exception as e:
            return {
                'response': f"❌ Erro ao processar pergunta: {str(e)}",
                'visualization': None,
                'data': pd.DataFrame(),
                'analysis': None,
                'query': None
            }

