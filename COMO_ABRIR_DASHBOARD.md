# 🚀 Como Abrir o Dashboard

## 📋 Métodos Disponíveis

### 1. **Método Rápido (Recomendado)**
```bash
.\abrir_dashboard.bat
```

### 2. **Método Alternativo**
```bash
.\abrir_dashboard.cmd
```

### 3. **Método Manual**
```bash
# Ativar ambiente virtual
.\ativar_venv.bat

# Executar dashboard
venv\Scripts\python.exe -m streamlit run Dash.py
```

## 🌐 URLs do Dashboard

- **Dashboard Principal**: http://localhost:8501
- **Assistente IA Inteligente**: http://localhost:8501/Assistente_IA

## ⚠️ Solução de Problemas

### Erro: "python.exe não encontrado"
- Execute `.\ativar_venv.bat` primeiro
- Verifique se o ambiente virtual está ativo

### Erro: "Módulo não encontrado"
- Execute `.\instalar_dependencias.bat`
- Reinicie o dashboard

### Porta já em uso
- Feche outras instâncias do Streamlit
- Use `Ctrl+C` para parar o servidor

## 🔧 Scripts Disponíveis

- `abrir_dashboard.bat` - Abertura automática com verificações
- `ativar_venv.bat` - Ativação do ambiente virtual
- `instalar_dependencias.bat` - Instalação de dependências
- `criar_atalho_dashboard.bat` - Criação de atalho no desktop
