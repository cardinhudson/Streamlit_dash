# 👋 Para Novos Usuários - Dashboard KE5Z

## 🚀 Início Rápido (3 Passos)

### 1️⃣ **Download e Configuração**
```bash
# Baixe o projeto completo (pasta inteira)
# Execute um destes arquivos:
CONFIGURAR_RAPIDO.bat    # ← RECOMENDADO
# OU
abrir_dash.bat          # Abre diretamente
```

### 2️⃣ **Aguarde a Instalação**
- O script instalará tudo automaticamente
- Primeira vez pode demorar 2-3 minutos
- Mantenha a janela do terminal aberta

### 3️⃣ **Use o Dashboard**
- Dashboard abrirá automaticamente no navegador
- Login: Use qualquer usuário/senha (sistema local)
- Explore as páginas e funcionalidades

## 🧹 Projeto Limpo - O que mudou?

### ✅ **Sem APIs Externas**
- **OpenAI**: ❌ Removido
- **Hugging Face**: ❌ Removido  
- **LangChain**: ❌ Removido
- **IA Local**: ✅ Funciona offline

### 🎯 **Vantagens**
- ⚡ **Deploy mais rápido** (menos dependências)
- 🔒 **Sem problemas de VPN** (tudo local)
- 💰 **Gratuito** (sem custos de API)
- 🌐 **Offline first** (funciona sem internet)
- 🛡️ **Mais seguro** (dados ficam locais)

## 🤖 IA Assistente Local

### 💬 **Como Usar**
1. Acesse a página "Assistente IA"
2. Digite perguntas em linguagem natural
3. Receba análises automáticas

### 📊 **Exemplos de Perguntas**
```
• "Top 10 maiores Type 07"
• "20 maiores fornecedores" 
• "Evolução temporal"
• "Gráfico waterfall"
• "Top 5 USIs"
• "Valor por período"
```

### 🎨 **Tipos de Análise**
- **Ranking**: Top N maiores valores
- **Temporal**: Evolução no tempo
- **Waterfall**: Variações em cascata

## 📊 Funcionalidades Principais

### 🏠 **Dashboard Principal**
- Filtros dinâmicos (USI, Período, Centro cst, etc.)
- Tabelas interativas com cores
- Gráficos Altair (barras, linhas)
- Exportação para Excel

### 🌊 **Análise Waterfall**
- Gráficos de cascata avançados
- Modo simples e financeiro
- **Cores corretas**:
  - 🟢 **Verde** = Diminuições (melhor)
  - 🔴 **Vermelho** = Aumentos (pior)
  - 🔵 **Azul** = Totais

### 📈 **Outras Páginas**
- **Total Accounts**: Tabelas de contas
- **Outside TC**: Análise externa

## 🛠️ Resolução de Problemas

### ❌ **Python não encontrado**
```bash
1. Acesse: https://python.org/downloads
2. Baixe Python 3.8 ou superior
3. Durante instalação: marque "Add Python to PATH"
4. Reinicie o terminal
5. Execute CONFIGURAR_RAPIDO.bat novamente
```

### ❌ **Erro de porta ocupada**
```bash
1. Feche outros programas
2. Execute novamente abrir_dash.bat
3. O script encontrará uma porta disponível
```

### ❌ **Erro de dados**
```bash
1. Certifique-se que a pasta KE5Z/ existe
2. Execute Extração.py se necessário
3. Verifique se há arquivos .parquet
```

### ❌ **Dashboard não abre**
```bash
1. Verifique se o terminal mostra "Running on http://..."
2. Copie o endereço e cole no navegador
3. Ou acesse: http://localhost:8501
```

## 🌐 Deploy no Streamlit Cloud

### 📁 **Arquivos Prontos**
- `runtime.txt` - Python 3.11.5
- `requirements_minimal.txt` - Dependências mínimas
- `requirements.txt` - Dependências completas
- `.streamlit/config.toml` - Configurações

### 🚀 **Como Fazer Deploy**
1. **Fork/Clone** o repositório
2. **Conecte** ao Streamlit Cloud
3. **Configure**:
   - Python version: `3.11.5`
   - Main file: `Dash.py`
   - Requirements: `requirements_minimal.txt`
4. **Deploy** automaticamente

### 💡 **Dica de Deploy**
- Comece com `requirements_minimal.txt`
- Se funcionar, use `requirements.txt` completo
- Sem problemas de APIs ou tokens

## 🔐 Sistema de Autenticação

### 👤 **Login Local**
- Sistema baseado em arquivo `usuarios.json`
- Para desenvolvimento/teste local
- **Não funciona no Streamlit Cloud**

### 🌐 **Para Produção**
- Considere desabilitar autenticação
- Ou usar autenticação do Streamlit Cloud
- Ou implementar sistema próprio

## 📋 Estrutura do Projeto

```
Dashboard_KE5Z/
├── 📄 Dash.py                    # App principal
├── 📁 pages/                     # Páginas do dashboard
│   ├── Assistente_IA.py         # IA Local
│   ├── Waterfall_Analysis.py    # Análise Waterfall
│   └── ...
├── 📁 KE5Z/                      # Dados
├── 🔧 abrir_dash.bat            # Executar dashboard
├── ⚡ CONFIGURAR_RAPIDO.bat      # Setup automático
├── 📦 requirements.txt           # Dependências
├── 🐍 runtime.txt               # Versão Python
└── 📚 documentação/
```

## 🎓 Próximos Passos

1. **Execute** `CONFIGURAR_RAPIDO.bat`
2. **Explore** o dashboard
3. **Teste** o Assistente IA
4. **Experimente** diferentes filtros
5. **Faça** deploy no Streamlit Cloud (opcional)

## 💬 Suporte

- **Documentação**: Leia os arquivos `.md`
- **Problemas**: Execute `COMO_USAR.bat`
- **Deploy**: Veja `DEPLOY_STREAMLIT_CLOUD.md`

---

## ✨ Resumo Final

**Dashboard KE5Z agora é:**
- 🧹 **Limpo** (sem APIs externas)
- 🚀 **Rápido** (deploy simplificado)  
- 🤖 **Inteligente** (IA Local)
- 🎨 **Bonito** (gráficos corretos)
- 🔒 **Seguro** (dados locais)

**Basta executar `CONFIGURAR_RAPIDO.bat` e começar a usar!** 🎉





