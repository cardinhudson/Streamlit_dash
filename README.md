# 📊 Dashboard KE5Z - Streamlit

Dashboard interativo para visualização de dados TC - KE5Z com sistema de autenticação.

## 🚀 Configuração do Ambiente

### Pré-requisitos
- Python 3.8 ou superior
- Git (opcional)

### Instalação Rápida

1. **Clone ou baixe o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd Streamlit_dash
   ```

2. **Instale as dependências automaticamente**
   - **Windows**: Execute `instalar_dependencias.bat`
   - **Linux/Mac**: Execute os comandos abaixo:
     ```bash
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Ative o ambiente virtual**
   - **Windows**: Execute `ativar_venv.bat`
   - **Linux/Mac**: Execute `source venv/bin/activate`

4. **Execute o dashboard**
   ```bash
   streamlit run Dash.py
   ```

### Instalação Manual

1. **Crie o ambiente virtual**
   ```bash
   python -m venv venv
   ```

2. **Ative o ambiente virtual**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o dashboard**
   ```bash
   streamlit run Dash.py
   ```

## 🔐 Sistema de Login - PROTEÇÃO COMPLETA

### 🛡️ Proteção Total
- **TODAS as páginas** são protegidas por autenticação
- **Nenhuma página** pode ser acessada sem login
- **Sistema centralizado** de autenticação em `auth.py`
- **Proteção automática** em todas as páginas do Streamlit

### Primeiro Acesso
- **Usuário**: `admin`
- **Senha**: `admin123`
- **IMPORTANTE**: Altere a senha padrão após o primeiro login!

### Cadastrar Usuários
1. Faça login com o usuário administrador
2. Na tela de login, expanda "👨‍💼 Área Administrativa"
3. Adicione novos usuários conforme necessário

### Páginas Protegidas
- ✅ **Dashboard Principal** (`Dash.py`)
- ✅ **Outside TC** (`pages/Outside TC.py`)
- ✅ **Total Accounts** (`pages/Total accounts.py`)
- ✅ **Todas as futuras páginas** (se seguirem o padrão)

## 📁 Estrutura do Projeto

```
Streamlit_dash/
├── Dash.py                 # Dashboard principal com sistema de login
├── requirements.txt        # Dependências do projeto
├── usuarios.json          # Dados dos usuários (criado automaticamente)
├── venv/                  # Ambiente virtual (não versionado)
├── KE5Z/                  # Dados do dashboard
│   └── KE5Z.parquet
├── pages/                 # Páginas adicionais
├── ativar_venv.bat        # Script de ativação (Windows)
├── instalar_dependencias.bat # Script de instalação (Windows)
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## 🛠️ Dependências

- **streamlit**: Framework web para Python
- **pandas**: Manipulação de dados
- **altair**: Visualizações interativas
- **openpyxl**: Leitura/escrita de arquivos Excel
- **pyarrow**: Leitura de arquivos Parquet

## 📊 Funcionalidades

- ✅ Sistema de autenticação seguro
- ✅ Filtros interativos (USINA, Período, Centro cst, Conta contabil)
- ✅ Gráficos dinâmicos com Altair
- ✅ Tabelas pivot interativas
- ✅ Exportação para Excel
- ✅ Interface responsiva

## 🔧 Comandos Úteis

### Ativar ambiente virtual
```bash
# Windows
ativar_venv.bat

# Linux/Mac
source venv/bin/activate
```

### Desativar ambiente virtual
```bash
deactivate
```

### Instalar novas dependências
```bash
pip install nome-do-pacote
pip freeze > requirements.txt  # Atualizar requirements.txt
```

### Executar dashboard
```bash
streamlit run Dash.py
```

## 🆘 Solução de Problemas

### Erro de dependências
```bash
# Opção 1: Script automático
python corrigir_venv.py

# Opção 2: Manual
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt --force-reinstall
```

### Erro de permissão (Windows)
Execute o PowerShell como administrador

### Porta já em uso
```bash
streamlit run Dash.py --server.port 8502
```

### Erro de codificação de caracteres
Execute: `python corrigir_venv.py`

### Testar se está funcionando
```bash
python testar_dashboard.py
```

## 📝 Como Criar Novas Páginas Protegidas

Para criar uma nova página que seja automaticamente protegida, use este template:

```python
import streamlit as st
from auth import verificar_autenticacao, exibir_header_usuario

# Configuração da página
st.set_page_config(
    page_title="Nova Página - Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OBRIGATÓRIO: Verificar autenticação no início
verificar_autenticacao()

# Header com informações do usuário
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Título da Nova Página")
    st.subheader("Subtítulo da página")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Seu conteúdo aqui...
st.write("Conteúdo da nova página protegida")
```

## 📝 Notas

- O arquivo `usuarios.json` contém dados sensíveis e não deve ser versionado
- O ambiente virtual (`venv/`) não deve ser versionado
- Use sempre o ambiente virtual para evitar conflitos de dependências
- **IMPORTANTE**: Sempre chame `verificar_autenticacao()` no início de cada página