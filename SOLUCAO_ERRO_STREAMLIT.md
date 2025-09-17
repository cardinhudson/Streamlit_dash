# 🚨 Solução para Erros do Streamlit Cloud

## 📋 Erro Identificado
Os erros mostram que o Streamlit Cloud não consegue localizar alguns pacotes:
- `Unable to locate package #`
- `Unable to locate package Dependências` 
- `Unable to locate package sistema`

**Causa**: Comentários em português no arquivo requirements ou packages.txt

## ✅ Soluções Testadas

### 1. **Use `requirements_minimal.txt`** (RECOMENDADO)
```
streamlit
pandas  
plotly
```

### 2. **Configure no Streamlit Cloud:**
- **Python version**: `3.11.5` (arquivo runtime.txt)
- **Requirements file**: `requirements_minimal.txt`
- **Main file path**: `Dash.py`

### 3. **Limpe o arquivo packages.txt:**
```bash
# Deixe packages.txt completamente vazio
echo "" > packages.txt
```

## 🔧 Passos para Deploy

### Opção A: Renomear arquivo
```bash
cp requirements_minimal.txt requirements.txt
```

### Opção B: Especificar no painel do Streamlit Cloud
1. Vá em "Advanced settings"
2. Requirements file: `requirements_minimal.txt`
3. Python version: `3.11.5`

## ⚠️ Funcionalidades que podem não funcionar no Cloud:

### 1. **Sistema de Autenticação**
- `usuarios.json` não funciona no cloud
- Solução: Desabilitar ou usar auth do Streamlit

### 2. **Exportação para Excel**
- Pode precisar adicionar `openpyxl` depois que o básico funcionar

### 3. **Leitura de arquivos Parquet**
- Pode precisar adicionar `pyarrow` depois

## 🚀 Deploy Incremental (RECOMENDADO)

### Passo 1: Deploy básico
```
# requirements_minimal.txt
streamlit
pandas
plotly
```

### Passo 2: Adicionar funcionalidades gradualmente
```
# Se Passo 1 funcionar, adicione:
streamlit
pandas
plotly
openpyxl
```

### Passo 3: Funcionalidades avançadas
```
# Se Passo 2 funcionar, adicione:
streamlit
pandas
plotly
openpyxl
pyarrow
altair
```

## 🔍 Debug no Streamlit Cloud

1. **Verifique os logs** no painel do Streamlit Cloud
2. **Teste local** antes do deploy:
   ```bash
   pip install -r requirements_minimal.txt
   streamlit run Dash.py
   ```

## 📁 Estrutura Final Mínima
```
projeto/
├── runtime.txt              # python-3.11.5
├── requirements.txt         # ou requirements_minimal.txt  
├── packages.txt             # VAZIO
├── Dash.py                  # App principal
├── auth.py                  # Pode precisar ajustes
└── pages/                   # Páginas
```

## 🎯 Teste Rápido
1. Use `requirements_minimal.txt`
2. Deixe `packages.txt` vazio
3. Configure Python 3.11.5
4. Se funcionar, adicione dependências uma por vez
