# 🔐 Sistema de Login - Dashboard KE5Z

## Como usar o sistema de login

### Primeiro acesso
1. Execute o arquivo `Dash.py` com o comando: `streamlit run Dash.py`
2. Na primeira execução, será criado automaticamente um usuário administrador:
   - **Usuário**: `admin`
   - **Senha**: `admin123`
3. **IMPORTANTE**: Altere a senha padrão após o primeiro login!

### Cadastrar novos usuários
1. Faça login com o usuário administrador
2. Na tela de login, expanda a seção "👨‍💼 Área Administrativa"
3. Clique em "Adicionar Novo Usuário"
4. Preencha:
   - **Usuário**: Nome do usuário (único)
   - **Senha**: Senha desejada
   - **Confirmar Senha**: Confirme a senha
5. Clique em "Cadastrar Usuário"

### Fazer login
1. Na tela de login, digite seu usuário e senha
2. Clique em "Entrar"
3. Se as credenciais estiverem corretas, você será redirecionado para o dashboard

### Fazer logout
1. No dashboard, clique no botão "🚪 Logout" no canto superior direito
2. Você será redirecionado para a tela de login

## Segurança
- As senhas são armazenadas com hash SHA-256 (não em texto plano)
- Os dados dos usuários são salvos no arquivo `usuarios.json`
- Cada usuário tem uma data de criação registrada
- A sessão é mantida durante a navegação no dashboard

## Arquivos criados
- `usuarios.json`: Arquivo que contém os dados dos usuários cadastrados
- `LOGIN_README.md`: Este arquivo de instruções

## Funcionalidades do Dashboard
Após o login, você terá acesso a todas as funcionalidades originais:
- Filtros por USINA, Período, Centro cst e Conta contabil
- Gráficos interativos
- Tabelas dinâmicas
- Exportação para Excel
- Visualização de dados do arquivo KE5Z.parquet
