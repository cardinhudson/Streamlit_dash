# Configuração do GitHub para Salvamento Automático

## Como configurar o salvamento automático no GitHub

### 1. Criar um Token de Acesso Pessoal

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" > "Generate new token (classic)"
3. Dê um nome para o token (ex: "Streamlit Dashboard")
4. Selecione as permissões:
   - ✅ `repo` (acesso completo ao repositório)
5. Clique em "Generate token"
6. **COPIE O TOKEN** (você só verá ele uma vez!)

### 2. Configurar no Streamlit Cloud

1. Acesse seu app no Streamlit Cloud
2. Vá em "Settings" > "Secrets"
3. Adicione as seguintes configurações:

```toml
GITHUB_TOKEN = "seu_token_aqui"
GITHUB_REPO_OWNER = "U235107"
GITHUB_REPO_NAME = "Streamlit_dash"
```

### 3. Testar a Conexão

1. Faça login como admin no dashboard
2. Clique em "🔗 Testar GitHub" na área administrativa
3. Se aparecer "🚀 GitHub: ✅ Conectado!", está funcionando!

### 4. Como Funciona

- **Cadastro de usuários**: Salva automaticamente no GitHub
- **Aprovação de usuários**: Salva automaticamente no GitHub
- **Rejeição de usuários**: Salva automaticamente no GitHub
- **Exclusão de usuários**: Salva automaticamente no GitHub

### 5. Backup Manual

- Use "📤 Exportar" para baixar os dados
- Use "📥 Importar" para restaurar dados
- Use "🔄 Backup Automático" para criar backups com timestamp

## Segurança

- O token do GitHub tem acesso completo ao repositório
- Mantenha o token seguro e não o compartilhe
- Se necessário, revogue o token e crie um novo

## Troubleshooting

- **"Token do GitHub não configurado"**: Configure o GITHUB_TOKEN nas secrets
- **"Erro ao acessar repositório"**: Verifique se o repositório existe e o token tem permissão
- **"Erro ao salvar no GitHub"**: Verifique se o token não expirou
