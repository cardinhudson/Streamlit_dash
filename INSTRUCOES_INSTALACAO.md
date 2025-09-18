# 📋 Instruções de Instalação - Dashboard KE5Z

## 🎯 Para Usar em Outros Computadores

### ✅ **Pré-requisitos:**

1. **Python 3.8 ou superior**
   - Download: https://python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marcar "Add Python to PATH" durante a instalação

2. **Conexão com Internet** (apenas na primeira execução)
   - Para instalar as dependências automaticamente

### 📁 **Arquivos Necessários:**

Copie estes arquivos para o novo computador:

```
📂 Pasta do Projeto/
├── 📄 Dash.py                    (arquivo principal)
├── 📄 auth.py                    (sistema de login)
├── 📄 requirements.txt           (dependências)
├── 📄 abrir_dashboard.bat        (arquivo NOVO para execução)
├── 📄 usuarios.json              (dados de usuários)
├── 📂 KE5Z/
│   └── 📄 KE5Z.parquet          (dados do dashboard)
└── 📂 pages/                     (páginas adicionais)
    ├── 📄 IA_Unificada.py
    ├── 📄 Total accounts.py
    └── 📄 Waterfall_Analysis.py
```

### 🚀 **Como Executar:**

#### **Método 1: Duplo Clique (Recomendado)**
1. Duplo clique no arquivo `abrir_dashboard.bat`
2. Aguarde a instalação automática das dependências
3. O navegador abrirá automaticamente

#### **Método 2: Linha de Comando**
```bash
# Instalar dependências (primeira vez)
pip install streamlit pandas altair plotly openpyxl pyarrow

# Executar dashboard
streamlit run Dash.py
```

### 🔧 **Solução de Problemas Comuns:**

#### ❌ **"Python não encontrado"**
- **Solução**: Instale Python de https://python.org
- Certifique-se de marcar "Add to PATH" na instalação

#### ❌ **"Erro ao instalar dependências"**
- **Solução**: Execute manualmente:
```bash
python -m pip install --upgrade pip
pip install streamlit pandas altair plotly openpyxl pyarrow
```

#### ❌ **"Arquivo de dados não encontrado"**
- **Solução**: Coloque o arquivo `KE5Z.parquet` na pasta `KE5Z/`
- O dashboard ainda funciona sem dados (para configuração)

#### ❌ **"Porta 8501 ocupada"**
- **Solução**: Use porta diferente:
```bash
streamlit run Dash.py --server.port 8502
```

### 🌐 **URLs de Acesso:**

- **Local**: http://localhost:8501
- **Rede**: http://[IP-DO-PC]:8501

### 👤 **Login Padrão:**

- **Usuário**: admin
- **Senha**: admin123

### 📱 **Compatibilidade:**

- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ Navegadores: Chrome, Firefox, Edge
- ✅ Rede local e internet

### 🔒 **Segurança:**

- Altere a senha padrão do admin
- Configure usuários específicos
- Use em rede confiável

---

## 📞 **Suporte:**

Para problemas ou dúvidas:
1. Verifique este arquivo de instruções
2. Execute o arquivo `abrir_dashboard.bat`
3. Verifique os logs no terminal

**✨ O Dashboard está pronto para ser usado em qualquer PC com Python!**
