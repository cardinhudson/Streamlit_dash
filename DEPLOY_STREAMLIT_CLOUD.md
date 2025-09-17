# 🚀 Deploy no Streamlit Cloud

## Arquivos Preparados para Deploy

✅ **requirements.txt** - Dependências mínimas e compatíveis
✅ **runtime.txt** - Python 3.11.5
✅ **packages.txt** - Dependências do sistema (vazio)
✅ **.streamlit/config.toml** - Configurações do app

## Passos para Deploy

### 1. Preparar Repositório
```bash
git add .
git commit -m "Preparar para deploy Streamlit Cloud"
git push origin main
```

### 2. Acessar Streamlit Cloud
1. Vá para https://share.streamlit.io/
2. Faça login com GitHub
3. Clique em "New app"

### 3. Configurar App
- **Repository**: Seu repositório GitHub
- **Branch**: main
- **Main file path**: Dash.py
- **App URL**: escolha um nome único

### 4. Deploy
- Clique em "Deploy!"
- Aguarde o processo de build (2-5 minutos)

## ⚠️ Limitações no Streamlit Cloud

### Dados
- O arquivo `KE5Z/KE5Z.parquet` deve estar no repositório
- Não é possível executar `Extração.py` no cloud
- Faça o upload dos dados processados

### Funcionalidades Limitadas
- ❌ Extração automática de dados
- ❌ Salvamento permanente de usuários
- ✅ Visualizações e filtros funcionam normalmente
- ✅ IA local funciona perfeitamente

## 📁 Estrutura Necessária no Repositório

```
/
├── Dash.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── runtime.txt               # Versão Python
├── packages.txt              # Dependências sistema
├── .streamlit/config.toml    # Configurações
├── auth.py                   # Autenticação
├── usuarios.json             # Dados de usuários
├── KE5Z/
│   └── KE5Z.parquet         # DADOS OBRIGATÓRIOS
└── pages/
    ├── IA_Unificada.py
    ├── Waterfall_Analysis.py
    └── Total accounts.py
```

## 🔧 Troubleshooting

### Erro de Dependências
- Use apenas as dependências listadas em `requirements.txt`
- Evite versões específicas (>=x.x.x)

### Erro de Python
- Mantenha `runtime.txt` com `python-3.11.5`

### Dados Não Carregam
- Verifique se `KE5Z/KE5Z.parquet` está no repositório
- Arquivo deve ter menos de 100MB

### App Não Inicia
- Verifique se `Dash.py` está na raiz
- Confirme se todas as importações estão corretas

## 📊 Status do Deploy

Após deploy bem-sucedido:
- ✅ Dashboard principal funcional
- ✅ Todas as páginas acessíveis
- ✅ Filtros funcionando
- ✅ Gráficos renderizando
- ✅ IA local operacional
- ⚠️ Usuários temporários (reset a cada deploy)