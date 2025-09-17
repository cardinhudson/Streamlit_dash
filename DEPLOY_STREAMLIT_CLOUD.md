# 🚀 Deploy no Streamlit Cloud

## ⚠️ Arquivos Criados para Resolver Erro de Versão Python

### 1. `runtime.txt`
- Especifica Python 3.11.5 (versão compatível com Streamlit Cloud)
- **IMPORTANTE**: Este arquivo deve estar na raiz do repositório

### 2. `requirements_streamlit_cloud.txt`
- Versão simplificada das dependências
- Remove pacotes problemáticos para o cloud
- **USE ESTE ARQUIVO** ao fazer deploy no Streamlit Cloud

### 3. `.streamlit/config.toml`
- Configurações específicas para o Streamlit Cloud
- Desabilita modo de desenvolvimento
- Configurações de segurança para produção

### 4. `packages.txt`
- Para dependências do sistema (se necessário)
- Atualmente vazio

## 📋 Passos para Deploy

### Opção A: Renomear arquivos
```bash
# Backup do requirements original
mv requirements.txt requirements_local.txt

# Usar versão para cloud
mv requirements_streamlit_cloud.txt requirements.txt
```

### Opção B: Especificar no Streamlit Cloud
1. No painel do Streamlit Cloud
2. Em "Advanced settings"
3. Python version: `3.11.5`
4. Requirements file: `requirements_streamlit_cloud.txt`

## 🔧 Configurações Recomendadas no Streamlit Cloud

- **Python version**: `3.11.5`
- **Main file path**: `Dash.py`
- **Requirements file**: `requirements_streamlit_cloud.txt` (ou `requirements.txt` se renomeou)

## 🚨 Problemas Comuns e Soluções

### Erro "Unsupported major version"
- ✅ **Solução**: Arquivo `runtime.txt` criado
- Especifica Python 3.11.5 compatível

### Erro de dependências
- ✅ **Solução**: `requirements_streamlit_cloud.txt` criado
- Remove dependências problemáticas como `ollama`, `langchain`, etc.

### Erro de autenticação
- ⚠️ **Atenção**: O sistema de login pode não funcionar no cloud
- Considere desabilitar autenticação para versão pública
- Ou implementar autenticação via Streamlit Cloud

## 🔒 Segurança para Produção

Se for versão pública, considere:
1. Remover sistema de autenticação local
2. Usar dados de exemplo (não dados reais)
3. Limitar funcionalidades sensíveis

## 📁 Estrutura Final para Deploy
```
projeto/
├── runtime.txt                    # ✅ Versão Python
├── requirements.txt               # ✅ Dependências (renomeado)
├── packages.txt                   # ✅ Dependências sistema
├── .streamlit/config.toml         # ✅ Configurações
├── Dash.py                        # ✅ App principal
├── auth.py                        # ⚠️  Pode precisar ajustes
├── pages/                         # ✅ Páginas
└── KE5Z/                          # ✅ Dados (se públicos)
```
