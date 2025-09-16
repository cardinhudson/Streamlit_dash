# 👨‍💻 Para Desenvolvedores

## 📁 Estrutura do Projeto

```
Streamlit_dash/
├── 📄 Dash.py                    # Dashboard principal
├── 📄 Extração.py               # Script de extração de dados
├── 📁 pages/                    # Páginas do dashboard
│   ├── 📄 Assistente_IA.py      # Assistente IA
│   ├── 📄 Waterfall_Analysis.py # Análise Waterfall
│   ├── 📄 Total accounts.py     # Contas totais
│   └── 📄 Outside TC.py         # Análise externa
├── 📁 KE5Z/                     # Dados processados
├── 📁 KSBB/                     # Dados KSBB
├── 📄 requirements.txt          # Dependências
└── 📄 *.bat                     # Scripts de automação
```

## 🚀 Scripts de Automação

### Para Colaboradores (Usar estes)
- `CONFIGURAR_RAPIDO.bat` - Configuração automática completa
- `abrir_dash.bat` - Abre dashboard (instala automaticamente)
- `COMO_USAR.bat` - Instruções detalhadas
- `testar_instalacao.bat` - Testa se tudo está funcionando

### Para Desenvolvedores
- `setup_ambiente.py` - Script Python de configuração
- `instalar_dependencias.bat` - Instala dependências manualmente
- `ativar_venv.bat` - Ativa ambiente virtual

## 🔧 Modificações no Código

### Adicionar Nova Página
1. Crie arquivo em `pages/nova_pagina.py`
2. Use estrutura básica do Streamlit
3. Teste com `abrir_dash.bat`

### Modificar Dashboard Principal
1. Edite `Dash.py`
2. Teste com `abrir_dash.bat`
3. Verifique se não quebrou outras páginas

### Adicionar Dependência
1. Adicione em `requirements.txt`
2. Teste com `testar_instalacao.bat`
3. Atualize `abrir_dash.bat` se necessário

## 🐛 Solução de Problemas

### Python não encontrado
- Instale Python 3.8+ de python.org
- Marque "Add Python to PATH"
- Reinicie terminal

### Erro de dependências
- Execute `abrir_dash.bat` (instala automaticamente)
- Ou execute `CONFIGURAR_RAPIDO.bat`

### Erro de porta
- Feche outros programas que usam portas 8501-8510
- Ou modifique a porta no script

### Erro de dados
- Execute `Extração.py` primeiro
- Verifique se arquivos de dados estão na pasta correta

## 📝 Notas Técnicas

- **Ambiente Virtual**: Usa `venv` (Python padrão)
- **Dependências**: Gerenciadas via `requirements.txt`
- **Portas**: 8501-8510 (automático)
- **Dados**: Processados em `KE5Z/KE5Z.parquet`
- **Logs**: Salvos em `logs/`

## 🔄 Atualizações

### Para Atualizar o Projeto
1. Faça backup dos dados importantes
2. Atualize o código
3. Teste com `testar_instalacao.bat`
4. Execute `abrir_dash.bat` para verificar

### Para Distribuir para Colaboradores
1. Inclua todos os arquivos `.bat`
2. Inclua `requirements.txt`
3. Inclua `setup_ambiente.py`
4. Teste em PC limpo
