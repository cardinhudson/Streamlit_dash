"""
Módulo de autenticação compartilhado para todas as páginas do Streamlit
"""
import streamlit as st
import hashlib
import json
from datetime import datetime

# Função para carregar usuários do arquivo JSON
def carregar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

# Função para criar hash da senha
def criar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para verificar credenciais
def verificar_login(username, senha):
    usuarios = carregar_usuarios()
    if username in usuarios:
        senha_hash = criar_hash_senha(senha)
        return senha_hash == usuarios[username]['senha']
    return False

# Função para verificar se o usuário está logado
def verificar_sessao():
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = False
    if 'usuario_nome' not in st.session_state:
        st.session_state.usuario_nome = None
    return st.session_state.usuario_logado

# Função para fazer logout
def fazer_logout():
    st.session_state.usuario_logado = False
    st.session_state.usuario_nome = None
    st.rerun()

# Função para tela de login
def tela_login():
    st.title("🔐 Login - Dashboard KE5Z")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Acesso ao Sistema")
        username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
        senha = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        
        if submitted:
            if verificar_login(username, senha):
                st.session_state.usuario_logado = True
                st.session_state.usuario_nome = username
                st.success(f"Bem-vindo, {username}!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos!")
    
    # Seção para administrador adicionar usuários
    st.markdown("---")
    st.subheader("👨‍💼 Área Administrativa")
    
    with st.expander("Adicionar Novo Usuário"):
        with st.form("add_user_form"):
            st.write("**Cadastrar novo usuário:**")
            novo_usuario = st.text_input("Usuário:", key="novo_usuario")
            nova_senha = st.text_input("Senha:", type="password", key="nova_senha")
            confirmar_senha = st.text_input("Confirmar Senha:", type="password", key="confirmar_senha")
            
            if st.form_submit_button("Cadastrar Usuário"):
                if nova_senha == confirmar_senha and novo_usuario and nova_senha:
                    usuarios = carregar_usuarios()
                    if novo_usuario not in usuarios:
                        usuarios[novo_usuario] = {
                            'senha': criar_hash_senha(nova_senha),
                            'data_criacao': datetime.now().isoformat()
                        }
                        salvar_usuarios(usuarios)
                        st.success(f"✅ Usuário '{novo_usuario}' cadastrado com sucesso!")
                    else:
                        st.error("❌ Usuário já existe!")
                else:
                    st.error("❌ Preencha todos os campos e confirme a senha corretamente!")

# Função para criar usuário administrador inicial
def criar_admin_inicial():
    usuarios = carregar_usuarios()
    if not usuarios:  # Se não há usuários, criar admin padrão
        usuarios['admin'] = {
            'senha': criar_hash_senha('admin123'),
            'data_criacao': datetime.now().isoformat()
        }
        salvar_usuarios(usuarios)
        st.info("👤 Usuário administrador criado: **admin** | Senha: **admin123**")
        st.warning("⚠️ **IMPORTANTE**: Altere a senha padrão após o primeiro login!")

# Função principal de autenticação - deve ser chamada no início de cada página
def verificar_autenticacao():
    """
    Função principal que deve ser chamada no início de cada página.
    Se o usuário não estiver logado, exibe a tela de login e para a execução.
    """
    # Criar usuário admin inicial se necessário
    criar_admin_inicial()
    
    # Verificar se o usuário está logado
    if not verificar_sessao():
        tela_login()
        st.stop()  # Para a execução da página se não estiver logado
    
    # Se chegou até aqui, o usuário está logado
    return True

# Função para exibir header com informações do usuário
def exibir_header_usuario():
    """
    Exibe o header com informações do usuário e botão de logout.
    Deve ser chamada após verificar_autenticacao().
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        st.write(f"👤 Usuário: **{st.session_state.usuario_nome}**")
        if st.button("🚪 Logout", type="secondary"):
            fazer_logout()
